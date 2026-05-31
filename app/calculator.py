"""Calculadora segura.

A ideia central é nunca usar `eval()`. Em vez disso:

1. Normalizamos o texto do usuário para uma expressão matemática
   (ex.: "quanto é 12 vezes 8?" -> "12*8").
2. Convertemos a expressão em uma árvore de sintaxe com `ast.parse`.
3. Avaliamos essa árvore manualmente, permitindo apenas um conjunto pequeno
   e controlado de operações. Qualquer coisa fora da lista é rejeitada.
"""

import ast
import math
import operator
import re
import unicodedata

# Operadores binários e unários permitidos (mapeados para funções seguras).
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# Funções permitidas dentro da expressão (apenas estas podem ser chamadas).
_ALLOWED_FUNCTIONS = {
    "sqrt": math.sqrt,
}

# Frases que apenas introduzem a conta e podem ser removidas.
_TRIGGER_WORDS = [
    "quanto e o",
    "quanto e",
    "o resultado de",
    "resultado de",
    "o valor de",
    "valor de",
    "qual e o",
    "qual e",
    "calcular",
    "calcule",
]

# Operadores escritos por extenso (frases mais longas primeiro).
_WORD_OPERATORS = [
    ("elevado a", "**"),
    ("multiplicado por", "*"),
    ("dividido por", "/"),
    ("dividido", "/"),
    ("vezes", "*"),
    ("mais", "+"),
    ("menos", "-"),
]


class CalculationError(Exception):
    """Erro levantado quando não é possível calcular a expressão com segurança."""


def _strip_accents(text: str) -> str:
    """Remove acentos para facilitar a comparação de palavras."""
    normalized = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")


def _handle_percentage(text: str) -> str:
    """Converte expressões de porcentagem em contas explícitas."""
    # "X% de Y" ou "X por cento de Y" -> ((X/100)*Y)
    text = re.sub(
        r"(\d+(?:\.\d+)?)\s*(?:%|por cento)\s*de\s*(\d+(?:\.\d+)?)",
        r"((\1/100)*\2)",
        text,
    )
    # "X%" sozinho -> (X/100)
    text = re.sub(r"(\d+(?:\.\d+)?)\s*%", r"(\1/100)", text)
    return text.replace("por cento", " ")


def _handle_root(text: str) -> str:
    """Converte 'raiz de N' (ou 'raiz quadrada de N') em sqrt(N)."""
    text = re.sub(r"raiz(?:\s+quadrada)?\s+de\s+(\d+(?:\.\d+)?)", r"sqrt(\1)", text)
    # Caso a raiz seja de uma expressão entre parênteses: "raiz de (2+2)".
    text = re.sub(r"raiz(?:\s+quadrada)?\s+de\s*", "sqrt", text)
    return text.replace("raiz", " ")


def _to_expression(message: str) -> str:
    """Transforma o texto do usuário em uma expressão matemática limpa."""
    text = _strip_accents(message.lower())

    # Vírgula decimal -> ponto (ex.: "2,5" -> "2.5").
    text = re.sub(r"(\d),(\d)", r"\1.\2", text)

    # Símbolos unicode comuns.
    text = text.replace("×", "*").replace("÷", "/").replace("^", "**")

    # Remove frases que só introduzem a conta.
    for word in _TRIGGER_WORDS:
        text = text.replace(word, " ")

    text = _handle_percentage(text)
    text = _handle_root(text)

    # Operadores por extenso.
    for word, symbol in _WORD_OPERATORS:
        text = text.replace(word, symbol)

    # "x" como multiplicação entre números (ex.: "3 x 4").
    text = re.sub(r"(\d)\s*x\s*(\d)", r"\1*\2", text)

    # Remove quaisquer palavras restantes, exceto "sqrt".
    text = re.sub(r"\b(?!sqrt\b)[a-z]+\b", " ", text)

    # Mantém apenas caracteres válidos para uma expressão.
    text = re.sub(r"[^0-9a-z+\-*/%().\s]", " ", text)

    return re.sub(r"\s+", " ", text).strip()


def _eval_node(node: ast.AST) -> float:
    """Avalia recursivamente um nó da árvore, permitindo só o que é seguro."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise CalculationError("Apenas números são permitidos.")
        return node.value

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise CalculationError("Operador não permitido.")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        # Trava simples contra expoentes absurdos (evita travar o servidor).
        if op_type is ast.Pow and abs(right) > 100:
            raise CalculationError("Expoente muito grande.")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise CalculationError("Operador não permitido.")
        return _ALLOWED_OPERATORS[op_type](_eval_node(node.operand))

    if isinstance(node, ast.Call):
        is_simple_call = isinstance(node.func, ast.Name) and not node.keywords
        if is_simple_call and node.func.id in _ALLOWED_FUNCTIONS:
            args = [_eval_node(arg) for arg in node.args]
            return _ALLOWED_FUNCTIONS[node.func.id](*args)
        raise CalculationError("Função não permitida.")

    raise CalculationError("Expressão não permitida.")


def _format_number(value: float) -> str:
    """Mostra inteiros sem casas decimais e arredonda floats longos."""
    if isinstance(value, int):
        return str(value)
    if value == int(value):
        return str(int(value))
    return str(round(value, 10))


def evaluate(message: str):
    """Calcula a expressão contida em `message`.

    Retorna uma tupla (resultado_formatado, expressao_normalizada).
    Levanta CalculationError quando não é possível calcular com segurança.
    """
    expression = _to_expression(message)
    if not expression:
        raise CalculationError("Não encontrei uma expressão matemática para calcular.")

    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval_node(tree)
    except CalculationError:
        raise
    except ZeroDivisionError:
        raise CalculationError("Não é possível dividir por zero.")
    except (SyntaxError, ValueError, TypeError, OverflowError):
        raise CalculationError("Não consegui interpretar a expressão matemática.")

    return _format_number(result), expression

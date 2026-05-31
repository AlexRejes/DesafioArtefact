"""Lógica de decisão: a pergunta é matemática ou deve ir para o LLM?

A regra é propositalmente simples e fácil de auditar:
uma pergunta é considerada matemática quando contém **um número** E
(**um operador** OU **uma palavra-chave de matemática**).

Exigir um número evita falsos positivos como "quanto custa um carro?",
que tem palavra-chave mas nada para calcular.
"""

import re
import unicodedata

# Palavras que sugerem uma operação matemática (sem acentos, em minúsculas).
_MATH_KEYWORDS = [
    "quanto e",
    "calcule",
    "calcular",
    "soma",
    "somar",
    "subtracao",
    "subtrair",
    "multiplicacao",
    "multiplicado",
    "divisao",
    "dividido",
    "vezes",
    "mais",
    "menos",
    "porcentagem",
    "por cento",
    "raiz",
    "elevado",
]

# Detecta a presença de um dígito.
_NUMBER_RE = re.compile(r"\d")

# Detecta operadores: símbolos comuns ou "x" entre dois números.
_OPERATOR_RE = re.compile(r"[+\-*/×÷^%]|(?<=\d)\s*x\s*(?=\d)")


def _strip_accents(text: str) -> str:
    """Remove acentos para comparar palavras de forma robusta."""
    normalized = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")


def is_math_question(message: str) -> bool:
    """Retorna True quando a mensagem parece ser uma conta a calcular."""
    text = _strip_accents(message.lower())

    has_number = bool(_NUMBER_RE.search(text))
    has_operator = bool(_OPERATOR_RE.search(text))
    has_keyword = any(keyword in text for keyword in _MATH_KEYWORDS)

    return has_number and (has_operator or has_keyword)

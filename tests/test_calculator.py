"""Testes da calculadora segura."""

import pytest

from app.calculator import CalculationError, evaluate


@pytest.mark.parametrize(
    "message, expected",
    [
        ("quanto é 12 * 8?", "96"),
        ("calcule 144 dividido por 12", "12"),
        ("2 elevado a 10", "1024"),
        ("20% de 50", "10"),
        ("raiz de 81", "9"),
        ("2,5 + 1,5", "4"),
    ],
)
def test_calculos_validos(message, expected):
    result, _expression = evaluate(message)
    assert result == expected


@pytest.mark.parametrize(
    "message",
    [
        "10 / 0",         # divisão por zero -> erro controlado
        "__import__(1)",  # tentativa de acessar builtins
        "open('x')",      # função não permitida
        "9 ** 99999",     # expoente muito grande
    ],
)
def test_entradas_invalidas_sao_recusadas(message):
    with pytest.raises(CalculationError):
        evaluate(message)

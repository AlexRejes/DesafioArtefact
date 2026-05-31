"""Testes da lógica de decisão (calculadora vs. LLM)."""

import pytest

from app.decision import is_math_question


@pytest.mark.parametrize(
    "message",
    [
        "quanto é 128 vezes 46?",
        "raiz de 144",
        "20% de 50",
        "2 elevado a 10",
    ],
)
def test_perguntas_matematicas(message):
    assert is_math_question(message) is True


@pytest.mark.parametrize(
    "message",
    [
        "Quem foi Albert Einstein?",
        "Qual é a capital da França?",
        # Tem a palavra "quanto", mas nenhum número nem operação real:
        "quanto custa um carro?",
        "me explique inteligência artificial",
    ],
)
def test_perguntas_nao_matematicas(message):
    assert is_math_question(message) is False

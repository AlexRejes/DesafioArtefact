"""Testes do endpoint principal da API.

Nenhum teste chama o Gemini de verdade: o caminho matemático usa a
calculadora local e o caminho do LLM é testado com mock (monkeypatch).
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_retorna_200():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_pergunta_matematica_usa_calculadora():
    response = client.post("/chat", json={"message": "quanto é 12 * 8?"})
    assert response.status_code == 200

    data = response.json()
    assert data["tool"] == "Calculadora"
    assert "96" in data["answer"]


def test_chat_mensagem_vazia_nao_quebra():
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 200

    data = response.json()
    # Resposta controlada: não chama o LLM e não derruba o servidor.
    assert data["tool"] == "LLM"
    assert "pergunta" in data["answer"].lower()


def test_chat_pergunta_geral_usa_llm_mockado(monkeypatch):
    from app import llm

    # Simula o LLM configurado e respondendo, sem tocar na API real.
    monkeypatch.setattr(llm, "is_configured", lambda: True)
    monkeypatch.setattr(llm, "ask", lambda message: "Resposta simulada do LLM.")

    response = client.post("/chat", json={"message": "Quem foi Albert Einstein?"})
    assert response.status_code == 200

    data = response.json()
    assert data["tool"] == "LLM"
    assert data["answer"] == "Resposta simulada do LLM."


def test_config_status_reporta_provider_e_flag():
    response = client.get("/config/status")
    assert response.status_code == 200

    data = response.json()
    assert data["provider"] == "gemini"
    # Apenas um booleano indicando se há chave; nunca o valor da chave.
    assert isinstance(data["llm_configured"], bool)


def test_config_status_nunca_expoe_a_chave(monkeypatch):
    from app import llm

    # Mesmo com o LLM "configurado", a resposta não deve conter a chave.
    monkeypatch.setattr(llm, "is_configured", lambda: True)

    data = client.get("/config/status").json()
    assert data == {"provider": "gemini", "llm_configured": True}
    assert "key" not in str(data).lower()


@pytest.mark.parametrize(
    "pergunta",
    [
        "Quem criou este projeto?",
        "Qual é a formação do Alexandre?",
        "Como funciona a Lylla?",
        "O que é Legacy of Ashes?",
        "O que é JackFin?",
        "Sobre o que é Eco das Trevas?",
        "O que aborda o livro CIBERSEGURANÇA: Introdução à Guerra Digital?",
    ],
)
def test_chat_perguntas_sobre_o_criador(monkeypatch, pergunta):
    from app import llm

    # Simula o Gemini configurado e respondendo, sem tocar na API real.
    monkeypatch.setattr(llm, "is_configured", lambda: True)
    monkeypatch.setattr(llm, "generate", lambda prompt: "Resposta simulada sobre o criador.")

    response = client.post("/chat", json={"message": pergunta})
    assert response.status_code == 200
    assert response.json()["tool"] == "Sobre o criador"

"""Testes do endpoint principal da API.

Nenhum teste chama o Gemini de verdade: o caminho matemático usa a
calculadora local e o caminho do LLM é testado com mock (monkeypatch).
"""

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

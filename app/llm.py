"""Integração com o LLM (Google Gemini) via API REST.

Usamos a API REST diretamente com `requests` para manter o projeto leve e
fácil de entender, sem depender de um SDK específico. A chave de API vem
sempre do backend (variável de ambiente) e nunca é exposta ao frontend.
"""

import requests

from .config import settings

# Endpoint da API generateContent do Gemini.
_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

# Instrução curta para manter respostas claras e em português.
_SYSTEM_PREAMBLE = (
    "Você é um assistente útil. Responda de forma clara, objetiva e em português. "
    "Pergunta do usuário: "
)

# Tempo máximo de espera pela resposta do LLM (em segundos).
_TIMEOUT = 20


class LLMError(Exception):
    """Erro ao falar com o serviço de LLM."""


def is_configured() -> bool:
    """True quando há chave de API configurada."""
    return settings.llm_enabled


def generate(prompt: str) -> str:
    """Envia um prompt completo ao Gemini e retorna o texto da resposta.

    Usada tanto pela pergunta geral (`ask`) quanto pelo modo "Sobre o criador",
    que monta o seu próprio prompt com os documentos locais como contexto.
    """
    if not is_configured():
        raise LLMError("O LLM não está configurado.")

    url = _API_URL.format(model=settings.gemini_model)
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(
            url,
            params={"key": settings.gemini_api_key},
            json=payload,
            timeout=_TIMEOUT,
        )
    except requests.RequestException:
        raise LLMError("Não foi possível conectar ao serviço de IA. Verifique sua conexão.")

    if response.status_code != 200:
        raise LLMError(f"O serviço de IA retornou um erro (HTTP {response.status_code}).")

    try:
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError, ValueError):
        raise LLMError("A resposta da IA veio em um formato inesperado.")


def ask(message: str) -> str:
    """Pergunta geral: adiciona um preâmbulo padrão e delega ao Gemini."""
    return generate(_SYSTEM_PREAMBLE + message)

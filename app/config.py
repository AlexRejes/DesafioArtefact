"""Configuração da aplicação.

Lê as variáveis de ambiente do arquivo `.env` (quando existir) e as expõe
através de um único objeto `settings`, fácil de importar em outros módulos.
"""

import os

from dotenv import load_dotenv

# Carrega o arquivo .env (se existir) para dentro de os.environ.
load_dotenv()

# Modelo usado por padrão quando GEMINI_MODEL não estiver definido.
DEFAULT_GEMINI_MODEL = "gemini-2.0-flash"


class Settings:
    """Guarda as configurações lidas do ambiente."""

    def __init__(self) -> None:
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.gemini_model = os.getenv("GEMINI_MODEL", "").strip() or DEFAULT_GEMINI_MODEL

    @property
    def llm_enabled(self) -> bool:
        """True somente quando há uma chave de API configurada."""
        return bool(self.gemini_api_key)


# Instância única reutilizada por toda a aplicação.
settings = Settings()

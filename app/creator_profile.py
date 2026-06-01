"""Superpoder opcional: perguntas sobre o criador, seus projetos e seus livros.

Funciona como um "RAG manual" simples:

1. detecta, por palavras-chave, se a pergunta é sobre o criador/projetos/livros;
2. escolhe APENAS os documentos Markdown relevantes em ``app/data/``;
3. carrega o conteúdo desses documentos locais;
4. monta um prompt e pede ao Gemini que responda com base nesse contexto.

Não usa embeddings, banco vetorial, LangChain nem upload de arquivos — apenas
leitura de arquivos locais. A chave de API continua só no backend (via ``llm``).
"""

import unicodedata
from pathlib import Path

from . import llm

# Pasta com os documentos locais (Markdown).
_DATA_DIR = Path(__file__).resolve().parent / "data"

# Documento base do perfil — sempre incluído quando o assunto é "o criador".
_PROFILE_DOC = "creator_profile.md"

# Palavras-chave gerais sobre o criador / perfil (já sem acento, em minúsculas).
_CREATOR_KEYWORDS = (
    "alexandre",
    "criador",
    "autor",
    "desenvolvedor",
    "formacao",
    "curriculo",
    "experiencia",
    "tecnologias",
    "projetos",
    "portfolio",
    "quem criou",
    "quem e o criador",
)

# Cada documento específico e as palavras-chave que o ativam.
# As chaves são caminhos relativos a ``app/data/``.
_DOC_KEYWORDS = {
    "projects/lylla.md": (
        "lylla",
        "organismo cognitivo",
        "vida artificial",
        "alife",
        "memoria semantica",
        "arquitetura cognitiva",
    ),
    "projects/legacy_of_ashes.md": (
        "legacy of ashes",
        "legacy",
        "rpg",
        "jogo",
        "gacha",
        "fantasia sombria",
        "vila das cinzas",
        "combate por turnos",
    ),
    "projects/jackfin.md": (
        "jackfin",
        "trading",
        "bots",
        "cripto",
        "criptomoedas",
        "event sourcing",
        "cqrs",
        "paper trading",
    ),
    "books/eco_das_trevas.md": (
        "eco das trevas",
        "dinis",
        "dhymeria",
        "sentinelas",
        "guerreiro supremo",
        "livro de fantasia",
    ),
    "books/ciberseguranca_introducao_guerra_digital.md": (
        "ciberseguranca",
        "guerra digital",
        "seguranca da informacao",
        "cybersecurity",
        "cisco",
        "ameacas digitais",
    ),
}

# Prompt enviado ao Gemini no modo "Sobre o criador".
_PROMPT_TEMPLATE = """Você é um assistente que responde perguntas sobre Alexandre Rejes Coelho, seus projetos e suas obras.

Responda somente com base nos documentos fornecidos.
Se a informação não estiver nos documentos, diga claramente que essa informação não está disponível.
Não invente cargos, empresas, números, resultados, experiências, tecnologias ou detalhes pessoais.
Responda em português do Brasil, com clareza e objetividade.

DOCUMENTOS:
{contexto}

PERGUNTA DO USUÁRIO:
{mensagem}
"""

_NOT_CONFIGURED_MSG = (
    "Posso responder sobre o criador, seus projetos e livros, mas para isso o "
    "modelo de linguagem precisa estar configurado. Defina GEMINI_API_KEY no "
    "arquivo .env e reinicie o servidor."
)

_NO_DOCS_MSG = (
    "Ainda não há documentos sobre esse assunto em app/data/. "
    "Adicione os arquivos Markdown correspondentes para eu poder responder."
)


def _normalize(text: str) -> str:
    """Minúsculas e sem acentos, para casar palavras-chave de forma robusta."""
    decomposed = unicodedata.normalize("NFKD", text)
    without_accents = "".join(c for c in decomposed if not unicodedata.combining(c))
    return without_accents.lower()


def _matches_any(normalized: str, keywords) -> bool:
    return any(keyword in normalized for keyword in keywords)


def is_creator_question(message: str) -> bool:
    """True se a pergunta for sobre o criador, um projeto ou um livro."""
    normalized = _normalize(message)
    if _matches_any(normalized, _CREATOR_KEYWORDS):
        return True
    return any(_matches_any(normalized, keywords) for keywords in _DOC_KEYWORDS.values())


def select_documents(message: str) -> list[str]:
    """Escolhe quais documentos usar, começando sempre pelo perfil base.

    Evita mandar todos os documentos sempre: inclui o perfil e apenas os
    documentos específicos cujas palavras-chave aparecem na pergunta.
    """
    normalized = _normalize(message)
    docs = [_PROFILE_DOC]
    for doc, keywords in _DOC_KEYWORDS.items():
        if _matches_any(normalized, keywords):
            docs.append(doc)
    return docs


def _load_context(docs: list[str]) -> str:
    """Carrega o conteúdo dos documentos existentes, ignorando os ausentes."""
    parts = []
    for doc in docs:
        path = _DATA_DIR / doc
        if path.is_file():
            content = path.read_text(encoding="utf-8").strip()
            if content:
                parts.append(f"# Documento: {doc}\n{content}")
    return "\n\n---\n\n".join(parts)


def build_prompt(message: str, context: str) -> str:
    """Monta o prompt final para o Gemini, com os documentos como contexto."""
    return _PROMPT_TEMPLATE.format(contexto=context, mensagem=message)


def answer(message: str) -> str:
    """Responde uma pergunta sobre o criador usando os documentos locais.

    Degrada com elegância: devolve uma mensagem amigável se o LLM não estiver
    configurado ou se não houver documentos para usar como contexto.
    """
    if not llm.is_configured():
        return _NOT_CONFIGURED_MSG

    context = _load_context(select_documents(message))
    if not context:
        return _NO_DOCS_MSG

    try:
        return llm.generate(build_prompt(message, context))
    except llm.LLMError as error:
        return str(error)

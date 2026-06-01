"""Testes do módulo de perfil do criador.

Cobrem o roteamento (detecção por palavras-chave), a seleção de documentos e a
montagem do prompt — sem nunca chamar o Gemini de verdade.
"""

import pytest

from app import creator_profile


@pytest.mark.parametrize(
    "pergunta",
    [
        "Quem criou este projeto?",
        "Qual é a formação do Alexandre?",
        "Quais tecnologias Alexandre usa?",
        "Como funciona a Lylla?",
        "O que é Legacy of Ashes?",
        "O que é JackFin?",
        "Sobre o que é Eco das Trevas?",
        "O que aborda o livro CIBERSEGURANÇA: Introdução à Guerra Digital?",
    ],
)
def test_perguntas_sobre_o_criador_sao_detectadas(pergunta):
    assert creator_profile.is_creator_question(pergunta) is True


@pytest.mark.parametrize(
    "pergunta",
    [
        "quanto é 12 * 8?",
        "Qual é a capital da França?",
        "Me explique o que é uma API REST.",
    ],
)
def test_perguntas_fora_do_tema_nao_sao_detectadas(pergunta):
    assert creator_profile.is_creator_question(pergunta) is False


def test_selecao_geral_usa_apenas_o_perfil():
    assert creator_profile.select_documents(
        "Qual é a formação do Alexandre?"
    ) == ["creator_profile.md"]


def test_selecao_de_projeto_inclui_perfil_e_documento_especifico():
    docs = creator_profile.select_documents("Como funciona a Lylla?")
    assert "creator_profile.md" in docs
    assert "projects/lylla.md" in docs


def test_selecao_de_livro_inclui_perfil_e_documento_especifico():
    docs = creator_profile.select_documents("Sobre o que é Eco das Trevas?")
    assert "creator_profile.md" in docs
    assert "books/eco_das_trevas.md" in docs


def test_resposta_amigavel_quando_llm_desligado(monkeypatch):
    from app import llm

    monkeypatch.setattr(llm, "is_configured", lambda: False)
    resposta = creator_profile.answer("Quem é o Alexandre?")
    assert "GEMINI_API_KEY" in resposta


def test_answer_usa_generate_com_o_contexto_no_prompt(monkeypatch):
    from app import llm

    monkeypatch.setattr(llm, "is_configured", lambda: True)
    monkeypatch.setattr(creator_profile, "_load_context", lambda docs: "CONTEXTO_X")
    monkeypatch.setattr(llm, "generate", lambda prompt: f"ctx_no_prompt={'CONTEXTO_X' in prompt}")

    resposta = creator_profile.answer("Como funciona a Lylla?")
    assert resposta == "ctx_no_prompt=True"

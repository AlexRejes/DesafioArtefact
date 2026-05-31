"""Backend FastAPI do assistente de IA com calculadora.

Fluxo do endpoint POST /chat:
  1. Recebe a mensagem do usuário.
  2. Decide se é uma conta (decision.is_math_question).
  3. Se for conta: tenta calcular localmente com a calculadora segura.
  4. Se não for conta (ou se a conta falhar): chama o LLM.
  5. Se o LLM não estiver configurado: retorna um aviso amigável.

O frontend estático também é servido por este mesmo app, então basta abrir
http://localhost:8000 no navegador depois de iniciar o servidor.
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import calculator, decision, llm

app = FastAPI(title="AI Assistant + Calculadora")

# CORS liberado para facilitar abrir o frontend de qualquer origem (MVP).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mensagem usada quando o LLM é necessário mas não há chave configurada.
_LLM_NOT_CONFIGURED = (
    "O modelo de linguagem (LLM) não está configurado. "
    "Defina GEMINI_API_KEY no arquivo .env para responder perguntas gerais. "
    "As perguntas matemáticas continuam funcionando normalmente."
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str
    tool: str  # "Calculadora" ou "LLM"


@app.get("/health")
def health():
    """Endpoint simples para checar se o servidor está no ar."""
    return {"status": "ok", "llm_enabled": llm.is_configured()}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    message = (request.message or "").strip()
    if not message:
        return ChatResponse(answer="Envie uma pergunta para começar.", tool="LLM")

    # 1) Caminho da calculadora.
    if decision.is_math_question(message):
        try:
            result, expression = calculator.evaluate(message)
            return ChatResponse(answer=f"{expression} = {result}", tool="Calculadora")
        except calculator.CalculationError:
            # Detectamos como matemática mas não deu para calcular:
            # seguimos para o LLM como fallback.
            pass

    # 2) Caminho do LLM (também serve de fallback).
    if not llm.is_configured():
        return ChatResponse(answer=_LLM_NOT_CONFIGURED, tool="LLM")

    try:
        answer = llm.ask(message)
        return ChatResponse(answer=answer, tool="LLM")
    except llm.LLMError as error:
        return ChatResponse(answer=str(error), tool="LLM")


# Servir o frontend estático na raiz "/". É montado por último para não
# conflitar com as rotas de API definidas acima.
_FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
if _FRONTEND_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(_FRONTEND_DIR), html=True), name="frontend")

# AI Assistant + Calculadora

Assistente de IA simples que recebe perguntas do usuário e decide, a cada
mensagem, **quando responder com um LLM** e **quando usar uma ferramenta
externa** — neste caso, uma **calculadora local e segura**.

O foco do projeto é **simplicidade, clareza e precisão**: um MVP limpo, sem
overengineering (sem banco de dados, sem login, sem Docker, sem LangChain).

---

## ✨ O que ele faz

- Pergunta **matemática** → resolvida pela **calculadora local** (sem chamar API).
- Pergunta **geral** → encaminhada para o **LLM (Google Gemini)**.
- A interface mostra qual ferramenta foi usada em cada resposta:
  - 🟢 `Ferramenta usada: Calculadora`
  - 🔵 `Ferramenta usada: LLM`

---

## 📁 Estrutura do projeto

```
ai-assistant-calculator/
├── app/
│   ├── __init__.py      # marca a pasta como pacote Python
│   ├── main.py          # FastAPI: endpoint /chat e serve o frontend
│   ├── config.py        # lê variáveis de ambiente (.env)
│   ├── calculator.py    # calculadora segura (ast, sem eval)
│   ├── decision.py      # decide: matemática ou LLM?
│   └── llm.py           # integração com o Gemini via API REST
├── frontend/
│   ├── index.html       # chat centralizado
│   ├── style.css        # estilos
│   └── script.js        # chamada ao backend e renderização
├── tests/
│   ├── test_calculator.py   # calculadora segura
│   ├── test_decision.py     # decisão calculadora vs. LLM
│   └── test_api.py          # endpoint /chat e /health
├── conftest.py          # deixa o pacote `app` importável nos testes
├── .env.example         # modelo de configuração
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Como rodar

### 1. Instalar as dependências

Recomendado usar um ambiente virtual:

```bash
# Na pasta do projeto:
python -m venv .venv

# Ativar o ambiente:
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Instalar:
pip install -r requirements.txt
```

### 2. Configurar o `.env`

```bash
# Windows (PowerShell):
Copy-Item .env.example .env
# Linux / macOS:
cp .env.example .env
```

Abra o `.env` e preencha a chave do Gemini (gere a sua em
<https://aistudio.google.com/app/apikey>):

```env
GEMINI_API_KEY=sua_chave_aqui
GEMINI_MODEL=gemini-2.5-flash-lite
```

> 💡 **Sem a chave o projeto continua funcionando** para perguntas
> matemáticas. Perguntas gerais recebem um aviso amigável dizendo que o LLM
> não está configurado.

### 3. Executar o backend

```bash
uvicorn app.main:app --reload
```

O servidor sobe em <http://localhost:8000>.

### 4. Abrir o frontend

O backend **já serve o frontend**. Basta abrir no navegador:

```
http://localhost:8000
```

> Alternativa: você pode abrir o `frontend/index.html` diretamente (duplo
> clique). Nesse caso o `script.js` aponta automaticamente para
> `http://localhost:8000/chat`, e o CORS já está liberado no backend.

---

## 🧠 Como funciona a lógica de decisão

A decisão (em `app/decision.py`) é propositalmente simples e fácil de auditar.
Uma pergunta é tratada como **matemática** quando contém:

> **um número** **E** ( **um operador** **OU** **uma palavra-chave de matemática** )

- **Números:** qualquer dígito (`\d`).
- **Operadores:** `+  -  *  /  ×  ÷  ^  %` ou `x` entre dois números.
- **Palavras-chave:** `quanto é`, `calcule`, `soma`, `subtração`,
  `multiplicação`, `divisão`, `vezes`, `dividido`, `mais`, `menos`,
  `porcentagem`, `por cento`, `raiz`, `elevado`.

Exigir **um número** evita falsos positivos como _"quanto custa um carro?"_
(tem palavra-chave, mas nada para calcular).

Se a pergunta for matemática, o backend chama a **calculadora**. Se a
calculadora não conseguir interpretar a conta, há um **fallback** que envia a
pergunta para o LLM.

### Calculadora segura (sem `eval`)

A calculadora (`app/calculator.py`) **nunca usa `eval()`**. O processo é:

1. **Normaliza** o texto para uma expressão (ex.: `"quanto é 12 vezes 8?"` → `"12*8"`),
   incluindo porcentagem (`"20% de 50"` → `"((20/100)*50)"`) e raiz
   (`"raiz de 16"` → `"sqrt(16)"`).
2. **Transforma em árvore de sintaxe** com `ast.parse`.
3. **Avalia manualmente** a árvore, permitindo **apenas**:
   - números,
   - operadores `+ - * / // % **` e sinais unários,
   - a função `sqrt`.
4. Qualquer outra coisa (nomes, atributos, chamadas não autorizadas) é
   **rejeitada** com um erro claro. Há ainda travas para divisão por zero e
   expoentes absurdos.

---

## 💬 Exemplos para testar

### Perguntas matemáticas → Calculadora

| Você digita | Resultado |
|---|---|
| `quanto é 12 * 8?` | `12*8 = 96` |
| `7 + 5 - 3` | `7+5-3 = 9` |
| `calcule 144 dividido por 12` | `144/12 = 12` |
| `3 vezes 9` | `3*9 = 27` |
| `2 elevado a 10` | `2**10 = 1024` |
| `20% de 50` | `((20/100)*50) = 10` |
| `raiz de 81` | `sqrt(81) = 9` |
| `(2 + 3) * 4` | `(2+3)*4 = 20` |

### Perguntas gerais → LLM

- `Qual é a capital da França?`
- `Explique o que é uma API REST em uma frase.`
- `Me dê uma ideia de nome para um gato preto.`

---

## 🔌 Testando a API direto (sem navegador)

```bash
# Conta (calculadora):
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"quanto é 12 * 8?\"}"

# Pergunta geral (LLM):
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Qual a capital do Brasil?\"}"
```

Resposta esperada (exemplo):

```json
{ "answer": "12*8 = 96", "tool": "Calculadora" }
```

Há também `GET /health` para checar se o servidor está no ar e se o LLM está
configurado.

---

## ✅ Como rodar os testes

Com as dependências instaladas (o `requirements.txt` já inclui `pytest` e
`httpx`), basta rodar, na raiz do projeto:

```bash
pytest
```

Os testes são rápidos e **não dependem de internet nem de chave de API** — a
chamada ao Gemini é substituída por um *mock*. Eles cobrem:

- **Calculadora segura** (`tests/test_calculator.py`): contas válidas e
  rejeição de divisão por zero, expoente absurdo e tentativas de executar
  código (`__import__`, `open`).
- **Decisão calculadora vs. LLM** (`tests/test_decision.py`): perguntas
  matemáticas são roteadas para a calculadora e perguntas gerais para o LLM
  (incluindo o caso "quanto custa um carro?", que **não** deve virar conta).
- **Endpoint da API** (`tests/test_api.py`): `GET /health`, `POST /chat` com
  pergunta matemática (retorna `tool = "Calculadora"`), mensagem vazia
  (resposta controlada) e a rota do LLM com mock.

---

## 📚 O que eu aprendi

- **Separar decisão de execução** deixa o código limpo: `decision.py` só
  decide; `calculator.py` e `llm.py` executam. Cada arquivo tem uma
  responsabilidade clara.
- **Avaliar matemática com segurança** usando `ast` em vez de `eval` — a
  diferença prática entre uma calculadora e uma porta aberta para execução de
  código arbitrário.
- **Fallbacks amigáveis** importam: o app continua útil mesmo sem chave de API,
  degradando com elegância em vez de quebrar.
- **Normalizar linguagem natural** (acentos, vírgula decimal, operadores por
  extenso) antes de calcular melhora bastante a experiência.

## 🔭 O que eu faria diferente com mais tempo

- **Roteamento por LLM (function calling / tool calling):** deixar o próprio
  modelo decidir quando chamar a calculadora, em vez de heurística por
  palavras-chave — mais robusto para linguagem natural.
- **Suporte a números por extenso** ("dois mais dois") e frases como
  "a soma de 2 e 3".
- **Testes automatizados** (pytest) para a calculadora e a decisão, cobrindo
  casos de borda e tentativas maliciosas.
- **Histórico de conversa** enviado ao LLM para respostas com contexto.
- **Streaming** da resposta do LLM e indicador de carregamento mais rico.
- **Mais ferramentas** (datas, conversão de unidades) com uma interface comum.

---

## 🛡️ Notas de segurança

- A chave de API fica **somente no backend** (variável de ambiente). O
  frontend nunca a vê.
- O `.env` está no `.gitignore` para não vazar credenciais.
- A calculadora aceita **apenas** operações matemáticas básicas; qualquer
  tentativa de executar código é rejeitada.

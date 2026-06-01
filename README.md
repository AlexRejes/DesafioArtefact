# AI Assistant + Calculadora

Assistente de IA simples que recebe perguntas do usuário e decide, a cada
mensagem, **quando responder com um LLM** e **quando usar uma ferramenta
externa** — neste caso, uma **calculadora local e segura**.

O foco do projeto é **simplicidade, clareza e precisão**: um MVP limpo, sem
overengineering (sem banco de dados, sem login, sem Docker, sem LangChain).

---

## ✨ O que ele faz

- Pergunta **matemática** → resolvida pela **calculadora local** (sem chamar API).
- Pergunta **sobre o criador / projetos / livros** → responde com base em
  **documentos Markdown locais** + **LLM** (veja
  [Superpoder adicional](#-superpoder-adicional-perfil-do-criador)).
- Pergunta **geral** → encaminhada para o **LLM (Google Gemini)**.
- A interface mostra qual ferramenta foi usada em cada resposta:
  - 🟢 `Ferramenta usada: Calculadora`
  - 🟣 `Ferramenta usada: Sobre o criador`
  - 🔵 `Ferramenta usada: LLM`
- Um botão de **⚙️ Configurações** abre um modal que mostra o provider atual e
  se a API key está configurada — **sem nunca expor a chave** (veja
  [Notas de segurança](#️-notas-de-segurança)).

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
│   ├── llm.py           # integração com o Gemini via API REST
│   ├── creator_profile.py  # superpoder: perfil/projetos/livros (RAG simples)
│   └── data/            # documentos Markdown usados como contexto
│       ├── creator_profile.md
│       ├── projects/    # lylla, legacy_of_ashes, jackfin
│       └── books/       # eco_das_trevas, ciberseguranca_introducao_guerra_digital
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

## 🦸 Superpoder adicional: Perfil do criador

Além de calculadora e LLM, o assistente tem uma **terceira rota**: responder
perguntas sobre **Alexandre Rejes Coelho**, seus **projetos** e seus **livros**,
usando **documentos Markdown locais** (em `app/data/`) como fonte de contexto.

Funciona como um **RAG simples**: o backend detecta o assunto por palavras-chave,
carrega **apenas os documentos relevantes** e pede ao Gemini que responda **com
base neles**, instruído a **não inventar** e a dizer quando a informação não
existe. **Sem embeddings, sem banco vetorial, sem LangChain e sem upload de
arquivos** — só leitura de arquivos locais, mantendo o MVP simples.

### Documentos

```
app/data/
├── creator_profile.md
├── projects/
│   ├── lylla.md
│   ├── legacy_of_ashes.md
│   └── jackfin.md
└── books/
    ├── eco_das_trevas.md
    └── ciberseguranca_introducao_guerra_digital.md
```

- Pergunta **geral sobre o Alexandre** → usa `creator_profile.md`.
- Pergunta sobre um **projeto/livro específico** → `creator_profile.md` **+** o
  documento daquele tema.
- **Nunca** envia todos os documentos de uma vez (economia de tokens e foco).
- Se os documentos não existirem ou o LLM não estiver configurado, o assistente
  responde de forma **amigável**, sem quebrar.

### Exemplos de perguntas

- Quem criou este projeto?
- Qual é a formação do Alexandre?
- Quais tecnologias Alexandre usa?
- Como funciona a Lylla?
- O que é Legacy of Ashes?
- O que é JackFin?
- Sobre o que é Eco das Trevas?
- O que aborda o livro CIBERSEGURANÇA: Introdução à Guerra Digital?

> 🔒 **Segurança:** este modo continua usando a `GEMINI_API_KEY` **apenas no
> backend**. Os documentos são lidos no servidor; o frontend nunca vê a chave
> nem os arquivos brutos — só recebe a resposta final.

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

### Status de configuração (usado pelo botão ⚙️ Configurações)

```bash
curl http://localhost:8000/config/status
```

Resposta:

```json
{ "provider": "gemini", "llm_configured": true }
```

`llm_configured` é apenas um booleano: `true` quando existe `GEMINI_API_KEY` no
backend, `false` caso contrário. **O valor da chave nunca é retornado.**

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

### Por que o botão de Configurações é "somente leitura"

O modal de configurações foi pensado para **melhorar a experiência sem abrir
brechas de segurança**. Por isso:

- O endpoint `GET /config/status` devolve **apenas** `provider` e o booleano
  `llm_configured`. Ele **nunca** retorna o valor de `GEMINI_API_KEY`.
- O frontend **não envia, não guarda e não exibe** a chave — ele só pergunta
  "está configurada?" e mostra `Configurada` / `Não configurada`.
- **Não existe** endpoint para gravar a chave ou escrever no `.env` pela
  interface. Aceitar uma chave digitada no navegador a faria trafegar pela rede
  e poderia acabar em logs, histórico ou cache — exatamente o que queremos
  evitar. A configuração continua sendo feita só no `.env`, no servidor.

Essa decisão mantém o projeto **simples** e dentro do escopo: a interface ganha
um indicador útil, mas a credencial nunca sai do backend.

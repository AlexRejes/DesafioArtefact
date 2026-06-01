# JackFin V4 — Documentação Completa

## Índice

1. [Visão Geral](#1-visão-geral)
2. [Arquitetura do Sistema](#2-arquitetura-do-sistema)
3. [Tecnologias Utilizadas](#3-tecnologias-utilizadas)
4. [Estrutura do Monorepo](#4-estrutura-do-monorepo)
5. [Aplicações](#5-aplicações)
6. [Pacotes (Libraries)](#6-pacotes-libraries)
7. [Banco de Dados e Migrações](#7-banco-de-dados-e-migrações)
8. [Sistema de Eventos](#8-sistema-de-eventos)
9. [Estratégias de Trading](#9-estratégias-de-trading)
10. [Sistema de Gates](#10-sistema-de-gates)
11. [Intelligence de Mercado](#11-intelligence-de-mercado)
12. [Configuração de Bots (YAML)](#12-configuração-de-bots-yaml)
13. [Paper Trading (Backtesting)](#13-paper-trading-backtesting)
14. [Infraestrutura](#14-infraestrutura)
15. [Etapas de Execução](#15-etapas-de-execução)
16. [Referência de Comandos CLI](#16-referência-de-comandos-cli)
17. [Fases de Desenvolvimento](#17-fases-de-desenvolvimento)
18. [Fluxo Completo de uma Operação](#18-fluxo-completo-de-uma-operação)

---

## 1. Visão Geral

**JackFin V4** é uma plataforma de trading algorítmico de criptomoedas, construída sobre uma arquitetura **event-driven** (orientada a eventos) com **Event Sourcing** e **CQRS**. O sistema é projetado para ser completamente auditável, determinístico e extensível.

### Princípios Fundamentais

- **Bot é configuração, não código** — bots são definidos em arquivos YAML; nenhum novo código é necessário para criar um novo bot.
- **Todo estado é derivado de eventos** — cada mudança de estado gera um evento imutável e append-only no banco de dados. O banco de dados Postgres é a única fonte de verdade.
- **RAM é apenas cache quente** — projeções em memória são sempre reconstruíveis a partir do event log.
- **Exchange isolada atrás de um adapter** — toda comunicação com a Bybit passa por uma abstração, facilitando testes e substituição de exchange.
- **Strict TypeScript em todo o projeto** — sem `any`, tipagem completa, modo estrito ativado.

### O que o sistema faz

O JackFin permite:

1. **Coletar dados de mercado em tempo real** da exchange Bybit via WebSocket.
2. **Coletar inteligência externa** (notícias, dados macro) via CoinGecko, Marketaux e classificação por LLM (Gemini).
3. **Executar backtests (paper trading)** de estratégias configuradas em YAML contra dados históricos/simulados.
4. **Monitorar resultados** via dashboard web e API REST.
5. **Planejar execução real** de ordens (preparado para fase futura).

---

## 2. Arquitetura do Sistema

### Visão de Alto Nível

```
┌─────────────────────────────────────────────────────────────────┐
│                          FONTES DE DADOS                        │
│   Bybit WebSocket (trades/candles)    CoinGecko / Marketaux     │
└────────────────────┬────────────────────────┬───────────────────┘
                     │                        │
                     ▼                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                      APPS CLI (Orquestrador)                    │
│   market:read    intelligence:poll/classify/cycle               │
│   paper:run      paper:orchestrate    db:migrate                │
└───────────────────────────┬─────────────────────────────────────┘
                            │ publica eventos
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     EVENT BUS (InMemory)                        │
│              publish / subscribe / once                         │
└──────────┬────────────────┬──────────────────┬─────────────────┘
           │                │                  │
           ▼                ▼                  ▼
┌──────────────┐  ┌──────────────────┐  ┌─────────────────────┐
│ PostgreSQL   │  │  TRADER ENGINE   │  │   PROJECTIONS       │
│ Event Store  │  │  (FakePipeline)  │  │  (Views/State)      │
│ (imutável)   │  │                  │  │                     │
│              │  │ Strategy         │  │ MarketStatus        │
│ TimescaleDB  │  │ → Gates          │  │ PaperAnalytics      │
│ (candles,    │  │ → Risk           │  │ OpenPositions       │
│  trades)     │  │ → Planner        │  │ SystemHealth        │
│              │  │ → SimExecutor    │  │                     │
└──────────────┘  └──────────────────┘  └──────────┬──────────┘
                                                    │
                                                    ▼
                                         ┌──────────────────────┐
                                         │    API (Fastify)     │
                                         │   GET /api/*         │
                                         └──────────┬───────────┘
                                                    │
                                                    ▼
                                         ┌──────────────────────┐
                                         │  DASHBOARD (React)   │
                                         │  Vite + React 18     │
                                         └──────────────────────┘
```

### Padrões Arquiteturais

#### Event Sourcing
Cada mudança de estado é registrada como um evento imutável na tabela `events`. O estado atual de qualquer entidade é derivado replay dos eventos. Isso garante auditabilidade total e permite reconstruir qualquer estado histórico.

#### CQRS (Command-Query Responsibility Segregation)
- **Escritas (Commands):** Fluem pelo pipeline: Strategy → Gates → Risk → Planner → Executor → Eventos
- **Leituras (Queries):** Servidas por projeções materializadas (tabelas `paper_*_projection`, `market_snapshots`, etc.)

#### Monolito Modular
- Cada pacote tem responsabilidade única e bem definida
- Sem dependências cíclicas
- `core-domain` é a camada mais interna (zero dependências externas)
- Aplicações orquestram pacotes, nunca o inverso

---

## 3. Tecnologias Utilizadas

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Linguagem | TypeScript (modo estrito) | 5.7 |
| Runtime | Node.js | — |
| Gerenciador de pacotes | pnpm workspaces | 9.15.0 |
| Build | tsc (TypeScript Compiler) | — |
| Bundler (dashboard) | Vite | — |
| Framework API | Fastify | 5.2.0 |
| Framework UI | React | 18.3.1 |
| Validação | Zod | 3.24.1 |
| Banco de dados | PostgreSQL + TimescaleDB | 16 + 2.17.2 |
| Cache / Lock | Redis | 7.4 |
| Testes | Vitest | 2.1.8 |
| Lint | ESLint + TypeScript-ESLint | 9.17 / 8.18 |
| Formatação | Prettier | 3.4.2 |
| Exchange | Bybit (REST + WebSocket) | — |
| Dados macro | CoinGecko | API v3 |
| Dados de notícias | Marketaux | API v1 |
| Classificação LLM | Google Gemini | API |
| Monitoramento | Grafana | — |
| Formato de config | YAML | — |
| Containerização | Docker Compose | — |

### Por que TimescaleDB?
TimescaleDB é uma extensão do PostgreSQL otimizada para séries temporais. É usada para as tabelas `market_trades`, `market_candles` e `market_snapshots`, que recebem alto volume de dados e precisam de queries eficientes por intervalo de tempo. A extensão oferece:
- Compressão automática de chunks históricos
- Políticas de retenção de dados (90 dias para candles/trades)
- Índices otimizados para queries temporais

### Por que Redis?
Redis é usado como mecanismo de lock distribuído via `jackfin:paper-run:lock`. Garante que apenas um processo `paper:run` execute por vez, prevenindo corrupção de estado.

---

## 4. Estrutura do Monorepo

```
/opt/jackfin-v4-staging/app/
├── apps/                      # 5 aplicações executáveis
│   ├── api/                   # Servidor REST (Fastify)
│   ├── cli/                   # Orquestrador CLI (todos os comandos)
│   ├── dashboard/             # Frontend web (React + Vite)
│   ├── trader/                # Engine de execução de trades
│   └── replay/                # Utilitário de replay de eventos
│
├── packages/                  # 19 bibliotecas compartilhadas
│   ├── core-domain/           # Tipos e contratos do domínio (zero deps)
│   ├── core-events/           # Catálogo de eventos (62 tipos)
│   ├── core-bus/              # Event Bus (in-memory)
│   ├── config/                # Carregador de YAML e registry de bots
│   ├── persistence/           # Stores Postgres + Redis
│   ├── projections/           # Projeções sobre o event log
│   ├── strategies/            # Implementações de estratégias
│   ├── gates/                 # Gates de aprovação de sinais
│   ├── risk/                  # Engine de risco
│   ├── planner/               # Construtor de planos de execução
│   ├── executor-sim/          # Executor simulado (backtesting)
│   ├── executor-real/         # Executor real (placeholder Phase 5+)
│   ├── exchange-bybit/        # Adapter Bybit (WebSocket + REST)
│   ├── market-data/           # Abstração de fonte de mercado
│   ├── market-intelligence/   # Integrações CoinGecko/Marketaux/Gemini
│   ├── analytics/             # Cálculos analíticos
│   ├── observability/         # Logging, métricas, tracing, alertas
│   ├── reconciler/            # Reconciliação de posições (placeholder)
│   └── watcher/               # Monitor de posições reais (placeholder)
│
├── config/                    # Configurações YAML
│   ├── global.yaml            # Config global (stage, exchange, risk)
│   ├── exchanges/bybit.yaml   # Config da exchange
│   ├── stages/                # Defaults por stage (labs/validation/production)
│   │   ├── labs/
│   │   ├── validation/
│   │   └── production/
│   ├── bots/                  # Definições de bots por stage
│   │   ├── labs/
│   │   ├── validation/
│   │   └── production/
│   └── paper-runner/          # Planos de orquestração de backtests
│
├── migrations/                # 23 arquivos SQL (schema evolution)
├── infra/                     # Docker Compose, Systemd, Grafana
├── tests/unit/                # Suite de testes unitários (Vitest)
├── docs/                      # Documentação técnica
└── scripts/                   # Utilitários
```

---

## 5. Aplicações

### 5.1 apps/api — Servidor REST

API read-only para dashboards e consumidores externos. Construída com Fastify 5.2.0.

**Características:**
- Aceita apenas verbos HTTP `GET`, `HEAD` e `OPTIONS` (escrita é proibida)
- Valida todas as respostas com Zod
- Suporta projeções opcionais (market status, intelligence, paper analytics)

**Endpoints disponíveis:**

| Rota | Descrição |
|------|-----------|
| `GET /health` | Health check do sistema |
| `GET /events` | Lista eventos com filtros |
| `GET /events-by-type` | Eventos filtrados por tipo |
| `GET /events-by-correlation` | Eventos por correlation_id |
| `GET /market` | Dados de mercado atuais |
| `GET /market-candles` | Candles OHLCV por símbolo/timeframe |
| `GET /market-status` | Status do mercado por símbolo |
| `GET /intelligence/*` | Dados de inteligência de mercado |
| `GET /paper/*` | Analytics e posições de paper trading |
| `GET /system` | Métricas e configuração do sistema |

### 5.2 apps/cli — Orquestrador de Comandos

Ponto de entrada para todas as operações operacionais. O arquivo principal `main.ts` tem ~2.870 linhas e despacha todos os comandos.

**Grupos de comandos:**

- **db:** operações de banco de dados
- **market:** coleta de dados de mercado
- **intelligence:** inteligência externa
- **paper:** paper trading / backtesting
- **replay/projections:** replay e reconstrução de estado

### 5.3 apps/dashboard — Interface Web

Frontend React para monitoramento e análise.

**Páginas:**

| Página | Descrição |
|--------|-----------|
| `overview` | Home do dashboard com métricas gerais |
| `runner` | Status do paper trading runner |
| `live` | Dados de mercado em tempo real |
| `signals` | Sinais gerados pelas estratégias |
| `plans` | Planos de execução |
| `bots` | Registry de bots configurados |
| `analytics` | Analytics de paper trading (PnL, fills, stats) |
| `intelligence` | Dados de inteligência de mercado |
| `marketdata` | Candles OHLCV e status de mercado |

Consome dados exclusivamente via `GET /api/*`.

### 5.4 apps/trader — Engine de Execução

Engine modular de execução de trades. Exporta a classe `FakePipeline`.

**Fluxo do pipeline:**
```
MarketSource
    → Strategy.evaluate()    (gera Signal ou null)
    → Gates.evaluate()       (aprovação condicional)
    → Risk.evaluate()        (avaliação de risco)
    → Planner.build()        (cria ExecutionPlan)
    → SimExecutor.execute()  (simula fills)
    → EventBus.publish()     (persiste eventos)
```

Cada etapa publica eventos no EventBus. O pipeline é totalmente injetável (dependency injection), facilitando testes.

### 5.5 apps/replay — Replay de Eventos

Utilitário para reproduzir eventos do event log. Usado para auditoria, teste e recuperação de estado.

---

## 6. Pacotes (Libraries)

### 6.1 @jackfin/core-domain — Contratos do Domínio

Camada mais interna do sistema. **Zero dependências externas.** Define todos os tipos e contratos do domínio de negócio.

**Tipos principais:**

```typescript
// Primitivos
type UUID = string
type ISODateTime = string
type Stage = 'labs' | 'validation' | 'production'
type TradeSide = 'buy' | 'sell'
type SymbolId = string    // ex: "BTC/USDT:USDT"
type BotId = string

// Bot
interface BotInstance {
  bot_id: BotId
  display_name: string
  type: string
  strategy_family: string
  symbols: SymbolId[]
  risk_profile: RiskProfile
  scenario_rules: ScenarioRules
  // ...
}

// Mercado
interface Candle {
  open: number; high: number; low: number; close: number
  volume: number; closed_at: ISODateTime
  timeframe: '1m' | '5m' | '15m' | '1h'
}

interface MarketState {
  snapshot_id: string
  last_price: number
  bid: number; ask: number; spread: number
  candles_by_timeframe: Record<string, Candle[]>
}

// Posição
type PositionStatus =
  | 'opening' | 'open' | 'protected'
  | 'closing' | 'closed' | 'failed' | 'manual_review'

// Outros
interface Signal { ... }
interface Decision { ... }
interface RiskApproval { ... }
interface ExecutionPlan { ... }
interface GateResult { passed: boolean; reason?: string }
```

### 6.2 @jackfin/core-events — Catálogo de Eventos

Define os 62 tipos de eventos do sistema, organizados por domínio.

**Envelope base de todo evento:**

```typescript
interface DomainEvent {
  event_id: UUID
  event_type: string
  schema_version: number
  stage: Stage
  signal_id?: UUID
  plan_id?: UUID
  bot_id?: BotId
  strategy_name?: string
  strategy_version?: string
  strategy_hash?: string
  config_snapshot_id?: string
  correlation_id: UUID        // agrupa eventos relacionados
  causation_id?: UUID         // evento pai que causou este
  occurred_at: ISODateTime
  recorded_at: ISODateTime
  runtime_version: string
  git_commit: string
  payload: unknown            // validado por Zod por tipo
}
```

**Domínios de eventos:**

| Domínio | Exemplos de Tipos |
|---------|-------------------|
| Config | `config.snapshot_created` |
| Market | `market.connected`, `market.candle_closed`, `market.trade_received`, `market.snapshot_created` |
| Strategy | `strategy.version_registered` |
| Signal | `signal.generated` |
| Decision | `decision.approved`, `decision.rejected` |
| Risk | `risk.evaluated`, `risk.approved`, `risk.rejected` |
| Planner | `plan.created`, `plan.cancelled` |
| Sim | `sim.order_created`, `sim.fill_received`, `sim.position_opened`, `sim.position_closed` |
| Real | `real.order_submitted`, `real.fill_received`, `real.position_closed` |
| Lock | (gerenciamento de lock) |
| Intelligence | (polling e classificação de inteligência) |

### 6.3 @jackfin/core-bus — Event Bus

```typescript
interface EventBus {
  publish(event: DomainEvent): Promise<void>
  subscribe(eventType: string, handler: Handler): void
  once(eventType: string, handler: Handler): void
}
```

Implementação: `InMemoryEventBus` — sincronismo in-process, sem rede.

### 6.4 @jackfin/persistence — Camada de Persistência

Implementações concretas dos stores de dados.

| Store | Tabela(s) | Descrição |
|-------|-----------|-----------|
| `PostgresEventStore` | `events` | Event log imutável |
| `PostgresMarketStore` | `market_trades`, `market_candles`, `market_snapshots` | Dados de mercado (TimescaleDB) |
| `PostgresIntelligenceStore` | `external_raw_payloads`, `intelligence_items`, `intelligence_snapshots` | Inteligência externa |
| `PostgresGeminiCache` | `paper_gemini_cache` | Cache do classificador Gemini |
| `PaperProjectionsStore` | `paper_*_projection` | Projeções de paper trading |
| `PaperOpenPositionsStore` | `paper_open_positions_projection` | Posições abertas ao vivo |
| `PaperRunStore` | `paper_runs` | Ledger de execuções de backtests |
| `PaperRunLock` | Redis | Lock exclusivo (`jackfin:paper-run:lock`) |

### 6.5 @jackfin/projections — Projeções

Vistas materializadas sobre o event log. São sempre reconstruíveis via `paper:rebuild-projections`.

| Projeção | Descrição |
|----------|-----------|
| `MarketStatusProjection` | Último snapshot de mercado por símbolo |
| `RecentEventsProjection` | Últimos 100 eventos (apenas memória) |
| `SystemHealthProjection` | Uptime e saúde do sistema |
| `PaperProjectionBuilder` | Reconstrói `paper_*_projection` a partir de eventos `sim.*` |
| `PaperOpenPositionsBuilder` | Rastreia posições abertas via `plan.created` + `sim.fill_received` + `sim.position_closed` |

### 6.6 @jackfin/exchange-bybit — Adapter Bybit

Componentes do adapter:

- **`BybitMarketSource`** — gerencia assinaturas WebSocket
- **`CandleBuilder`** — agrega trades em candles (1m / 5m / 15m / 1h)
- **`RingBuffer`** — buffer circular para histórico de candles
- **`WsClient`** — gerenciamento de conexão WebSocket com reconexão automática

Funcionalidades:
- Stream de trades em tempo real
- Geração de candles em múltiplos timeframes simultaneamente
- Snapshots de mercado a cada 5 segundos
- Detecção de gaps de dados (`market.data_gap_detected`)
- Seed de candles históricos no startup (warmup)

### 6.7 @jackfin/market-intelligence — Inteligência de Mercado

**Adapters:**

| Adapter | Fonte | Dados |
|---------|-------|-------|
| `CoinGeckoAdapter` | CoinGecko API | Dados globais de mercado, preços de coins, trending |
| `MarketauxAdapter` | Marketaux API | Feed de notícias financeiras |
| `GeminiClassifierAdapter` | Google Gemini LLM | Classificação de sentimento de notícias |

**Funcionalidades avançadas:**
- Pool de chaves API com rastreamento de budget diário
- Detecção de rate limits e degradação graceful
- Deduplicação de conteúdo via content-hash
- Cache com TTL (skip inteligente por source)
- `CachingIntelligenceProvider` — cache em memória atualizado a cada 60s

---

## 7. Banco de Dados e Migrações

### Schema — Tabelas Principais

```sql
-- Event log imutável (append-only)
events (
  event_id UUID PRIMARY KEY,
  event_type TEXT NOT NULL,
  schema_version INT,
  stage TEXT,
  bot_id TEXT,
  plan_id UUID,
  signal_id UUID,
  correlation_id UUID,
  causation_id UUID,
  occurred_at TIMESTAMPTZ,
  recorded_at TIMESTAMPTZ,
  payload JSONB,
  -- Índices: event_type, bot_id, plan_id, signal_id, correlation_id
)

-- Dados de mercado (TimescaleDB hypertables)
market_trades     (symbol, price, qty, side, trade_time, ...)
market_candles    (exchange, symbol, timeframe, open, high, low, close, volume, closed_at)
market_snapshots  (symbol, snapshot_id, last_price, bid, ask, candles_json, ...)

-- Inteligência externa
external_raw_payloads  (source, content_hash, payload, fetched_at)
intelligence_items     (source, category, headline, sentiment, score, observed_at, ...)
intelligence_snapshots (snapshot_id, items, created_at)
source_health          (source, status, last_checked_at, error)

-- Paper trading (projeções reconstruíveis)
paper_trades_projection      (trade_id, bot_id, side, entry_price, exit_price, pnl, ...)
paper_fills_projection        (fill_id, plan_id, side, price, qty, fee, ...)
paper_orders_projection       (order_id, plan_id, type, status, ...)
paper_positions_projection    (position_id, bot_id, status, outcome, mfe, mae, ...)
paper_performance_projection  (bot_id, run_id, total_trades, win_rate, total_pnl, ...)
paper_open_positions_projection (position_id, bot_id, entry_price, current_price, ...)

-- Ledger de execuções
paper_runs (
  run_id UUID PRIMARY KEY,
  bot_id TEXT,
  status TEXT,  -- running | completed | failed | cancelled
  started_at TIMESTAMPTZ,
  stopped_at TIMESTAMPTZ,
  duration_ms INT,
  error_message TEXT,
  context_json JSONB  -- bot config snapshot no momento da execução
)
```

### Migrações (23 arquivos)

As migrações são aplicadas em ordem sequencial via `pnpm db:migrate`.

```
001 — Criação do event log (events, processed_events)
002 — Strategy versions
003 — Config snapshots
004 — Market trades (TimescaleDB hypertable)
005 — Market candles (TimescaleDB hypertable)
006 — Market snapshots
007 — Market tickers
008 — External raw payloads (intelligence)
009 — Intelligence items
010 — Intelligence snapshots
011 — Source health
012 — Paper projection tables (5 tabelas)
013 — Paper outcome kinds enum
014 — Paper config variant tracking
015 — Key health (API key rate limit tracking)
016 — Paper sim MFE/MAE
017 — Paper open positions projection
018 — Paper runs ledger
019 — Runtime context
020 — Sim trade context
021 — Índices otimizados no event log
022 — Políticas de retenção TimescaleDB (90 dias market, 30 dias intelligence)
023 — Índices adicionais para queries de paper analytics
```

---

## 8. Sistema de Eventos

### Fluxo de um Evento

```
1. Ação ocorre (trade recebido, sinal gerado, etc.)
2. Evento criado com envelope padronizado
3. EventBus.publish(event) chamado
4. Event Store persiste o evento em Postgres (append-only)
5. Subscribers recebem o evento sincronamente
6. Projeções são atualizadas
```

### Correlação de Eventos

O `correlation_id` agrupa todos os eventos de uma "cadeia de causalidade":

```
market.snapshot_created  [correlation_id: abc-123]
    └─ signal.generated  [correlation_id: abc-123, causation_id: snapshot_event_id]
        └─ decision.approved  [correlation_id: abc-123]
            └─ plan.created   [correlation_id: abc-123]
                ├─ sim.order_created   [correlation_id: abc-123]
                ├─ sim.fill_received   [correlation_id: abc-123]
                └─ sim.position_closed [correlation_id: abc-123]
```

Isso permite rastrear toda a história de uma operação de ponta a ponta via `GET /events-by-correlation?id=abc-123`.

---

## 9. Estratégias de Trading

### Contrato

```typescript
interface StrategyDefinition {
  name: string
  version: string
  hash: string    // SHA256 do código fonte para versionamento imutável
  evaluate(context: StrategyContext): Signal | null
}

interface StrategyContext {
  bot: BotInstance
  market: MarketState
  calendar?: CalendarContext     // hora do dia, dia da semana, etc.
  intelligence?: IntelligenceContext  // dados macro e de notícias
  params: Record<string, unknown>     // parâmetros do YAML do bot
}
```

### Estratégias Implementadas (v1)

| Estratégia | Nome | Descrição |
|-----------|------|-----------|
| `breakout/v1` | Breakout | Identifica rompimentos de range com momentum |
| `diagnostic-momentum/v1` | Diagnostic Momentum | Momentum com sinais diagnósticos detalhados |
| `pullback-momentum/v1` | Pullback Momentum | Momentum em retrações de tendência |
| `mean-reversion/v1` | Mean Reversion | Reversão à média com parâmetro K configurável |
| `noop/v1` | Noop | Estratégia nula para testes (nunca gera sinal) |

### Estratégias Planejadas (Phase 4D — stubs)

| Estratégia | Descrição |
|-----------|-----------|
| `trend-following/v1` | Seguidor de tendência |
| `volatility-squeeze/v1` | Squeeze de volatilidade |
| `regime-switch/v1` | Troca de regime de mercado |
| `low-vol-reversion/v1` | Reversão em baixa volatilidade |

### Versionamento de Estratégias

Cada estratégia tem um `strategy_hash` (SHA256 do código fonte). Se o código muda, o hash muda, e o evento `strategy.version_registered` é emitido. Isso garante que backtests históricos sempre referenciem a versão exata do algoritmo que gerou os resultados.

---

## 10. Sistema de Gates

Gates são filtros que aprovam ou rejeitam sinais antes da execução. São avaliados em sequência; o primeiro gate que falhar rejeita o sinal.

### Gates Core (sempre ativos)

| Gate | Descrição |
|------|-----------|
| `SymbolAllowedGate` | Verifica se o símbolo está na lista permitida do bot |
| `SideAllowedGate` | Verifica se o lado (buy/sell) é permitido pelo bot |
| `StageGate` | Restringe execução ao stage configurado (labs/validation/production) |
| `KillSwitchGate` | Bloqueia todas as operações se o kill switch estiver ativo |
| `CooldownGate` | Impõe período de espera entre operações do mesmo bot |
| `MarketFreshnessGate` | Rejeita sinais se os dados de mercado estiverem muito antigos |

### Gates de Inteligência (condicionais ao YAML do bot)

| Gate | Ativação | Descrição |
|------|----------|-----------|
| `NewsLockGate` | `scenario_rules.news_lock: true` | Bloqueia sinais quando há notícias severas (por símbolo ou macro) |
| `RegimeGate` | `scenario_rules.regimes: [...]` | Filtra operações por regime de mercado atual (RANGING / TRENDING / VOLATILE) |

### Resultado de Gate

```typescript
interface GateResult {
  gate: string
  passed: boolean
  reason?: string    // explicação quando reprovado
}
```

Todos os resultados de gates são incluídos no evento `decision.approved` ou `decision.rejected`, permitindo análise de quais gates são mais restritivos.

---

## 11. Intelligence de Mercado

### Ciclo de Inteligência

```
pnpm intelligence:cycle
    │
    ├─ CoinGeckoAdapter.fetchGlobalMarket()
    │       → salva em external_raw_payloads
    │       → cria intelligence_items (tipo: macro)
    │
    ├─ MarketauxAdapter.fetchNews()
    │       → filtra por content-hash (deduplicação)
    │       → salva em external_raw_payloads
    │       → cria intelligence_items (tipo: news)
    │
    └─ GeminiClassifierAdapter.classify()
            → envia notícias não classificadas ao Gemini LLM
            → Gemini retorna: sentimento (bullish/bearish/neutral),
              score (-1.0 a +1.0), categorias, símbolos afetados
            → salva classificação em intelligence_items
            → persiste em gemini_cache (evita reclassificar mesmo conteúdo)
```

### Intelligence Context para Gates

```typescript
interface IntelligenceContext {
  macro_score: number           // -1.0 a +1.0 (saúde geral do mercado)
  macro_regime: ExchangeRegime  // RANGING | TRENDING | VOLATILE
  symbol_scores: Record<SymbolId, number>   // score por símbolo
  has_severe_news: boolean      // se há notícias severas recentes
  severe_news_symbols: SymbolId[]  // quais símbolos têm notícias severas
}
```

---

## 12. Configuração de Bots (YAML)

### Estrutura de um Bot YAML

```yaml
# config/bots/labs/asterion.yaml
bot_id: asterion
display_name: "Asterion Labs"
type: paper
strategy_family: momentum
stage: labs

strategy_name: pullback-momentum
strategy_version: v1

symbols:
  - BTC/USDT:USDT
  - ETH/USDT:USDT

allowed_sides:
  - buy
  - sell

risk:
  margin_usdt: 100
  leverage: 5
  tp_pct: 1.5
  sl_pct: 0.8
  max_margin_mult: 1.0

cooldown:
  minutes: 15

scenario:
  regimes:
    - TRENDING
    - RANGING
  news_lock: true
  correlation_states: []

sim:
  fee_bps: 6
  slippage_bps: 3
  max_duration_minutes: 240

strategy_params:
  lookback_candles: 20
  momentum_threshold: 0.002
  k_factor: 1.5

variants:
  aggressive:
    risk:
      tp_pct: 2.5
      sl_pct: 1.2
    strategy_params:
      momentum_threshold: 0.001
  conservative:
    risk:
      tp_pct: 1.0
      sl_pct: 0.5
```

### Variantes (Variants)

Variantes permitem testar diferentes parametrizações do mesmo bot sem criar arquivos separados. São deep-merged sobre a config base:

```bash
pnpm paper:run --bot asterion --variant aggressive --duration 4h
```

### Stages

| Stage | Propósito |
|-------|-----------|
| `labs` | Desenvolvimento e experimentos iniciais |
| `validation` | Validação de performance antes de produção |
| `production` | Config pronta para execução real |

---

## 13. Paper Trading (Backtesting)

### Como funciona

O paper trading executa a engine de trading contra dados históricos/simulados sem enviar ordens reais para a exchange.

```
1. Carrega bot YAML (com optional --variant)
2. Aquece cache de candles (--warmup N candles do Postgres)
3. Adquire Redis lock (impede runs simultâneos)
4. Registra início no paper_runs ledger
5. Inicia FakePipeline com SimExecutor
6. Para cada candle/snapshot recebido:
   a. Strategy avalia o mercado
   b. Gates filtram o sinal
   c. Risk avalia a operação
   d. Planner cria o plano de execução
   e. SimExecutor resolve o trade vs candles subsequentes
   f. Eventos sim.* são emitidos e persistidos
7. Ao fim da duração, posições abertas são fechadas (grace period)
8. Libera Redis lock
9. Atualiza paper_runs com status e métricas finais
```

### SimExecutor (Executor Realístico)

O `RealisticSimExecutor` resolve cada trade contra candles reais subsequentes:

```
Para cada posição aberta:
  Para cada candle subsequente:
    Se high >= TP_price  → fecha como TP (take profit)
    Se low  <= SL_price  → fecha como SL (stop loss)
    Se candle_count >= max_duration → fecha como timeout
    Se high >= TP e low <= SL no mesmo candle → "ambiguous" (heurística)

Parâmetros de simulação:
  fee_bps      — taxa da exchange em basis points (ex: 6 = 0.06%)
  slippage_bps — slippage simulado (ex: 3 = 0.03%)
  max_duration_minutes — timeout máximo da posição
```

### Métricas Calculadas

- **PnL por trade** (realizado)
- **MFE** (Maximum Favorable Excursion) — máximo lucro que o trade chegou a ter
- **MAE** (Maximum Adverse Excursion) — máxima perda que o trade chegou a ter
- **Win rate, total trades, total PnL** por bot/run
- **Outcome kind** — TP / SL / timeout / early_cancel

### Orquestração de Runs (paper:orchestrate)

```yaml
# config/paper-runner/plan.yaml
runs:
  - bot: asterion
    variant: conservative
    duration: 4h
    warmup: 100
  - bot: asterion
    variant: aggressive
    duration: 4h
    warmup: 100
  - bot: nyx
    duration: 8h
    warmup: 200
```

```bash
pnpm paper:orchestrate --plan config/paper-runner/plan.yaml
```

Executa os runs sequencialmente, aguardando o término de cada um antes de iniciar o próximo.

---

## 14. Infraestrutura

### Docker Compose (infra/docker-compose.yml)

```yaml
services:
  postgres:
    image: timescale/timescaledb:2.17.2-pg16
    ports: ["5432:5432"]
    volumes: [postgres_data:/var/lib/postgresql/data]

  redis:
    image: redis:7.4-alpine
    ports: ["6379:6379"]
```

### Variáveis de Ambiente

```bash
# Banco de dados
DATABASE_URL=xxx

# Redis
REDIS_URL=xxx

# Exchange
BYBIT_API_KEY=xxx
BYBIT_API_SECRET=xxx

# Intelligence APIs
COINGECKO_API_KEY=xxx
MARKETAUX_API_KEY=xxx
GEMINI_API_KEY=xxx

# Runtime
NODE_ENV=development
STAGE=labs
GIT_COMMIT=abc123
RUNTIME_VERSION=4.0.0
```

### Systemd (Produção)

**market-reader.timer** — executa `market:read` continuamente, coletando dados de mercado.

**intelligence-cycle.timer** — executa `intelligence:cycle` periodicamente, buscando notícias e classificando com Gemini.

### Grafana

Dashboards de monitoramento para:
- Volume de eventos por tipo
- Latência de persistência
- Taxa de sinais gerados vs rejeitados
- PnL cumulativo de paper trading
- Saúde das fontes de inteligência

---

## 15. Etapas de Execução

### Pré-requisitos

1. Node.js (versão LTS recente)
2. pnpm >= 9.15.0
3. Docker e Docker Compose

### Setup Inicial

```bash
# 1. Instalar dependências
cd /opt/jackfin-v4-staging/app
pnpm install

# 2. Subir infraestrutura
docker compose -f infra/docker-compose.yml up -d

# 3. Verificar saúde do banco
pnpm db:health

# 4. Aplicar migrações
pnpm db:migrate

# 5. Verificar status das migrações
pnpm db:status

# 6. Compilar todos os pacotes
pnpm build
```

### Coleta de Dados de Mercado

```bash
# Coletar dados do Bybit por 1 hora
pnpm market:read --symbols BTC/USDT:USDT,ETH/USDT:USDT --duration 1h

# Em produção (loop contínuo via systemd timer)
# O systemd restarta o processo automaticamente
```

### Coleta de Inteligência

```bash
# Ciclo completo (CoinGecko + Marketaux + Gemini)
pnpm intelligence:cycle

# Apenas uma fonte
pnpm intelligence:poll --source coingecko --limit 20
pnpm intelligence:poll --source marketaux --limit 50

# Apenas classificação (dados já coletados)
pnpm intelligence:classify --source marketaux --limit 20
```

### Executar Paper Trading

```bash
# Run básico
pnpm paper:run --bot asterion --duration 2h --warmup 50

# Com variante
pnpm paper:run --bot asterion --variant aggressive --duration 4h --warmup 100

# Verificar status (em outro terminal)
pnpm paper:status

# Forçar parada
pnpm paper:unlock

# Reconstruir projeções se corrompidas
pnpm paper:rebuild-projections
pnpm paper:rebuild-open-positions

# Orquestrar múltiplos runs
pnpm paper:orchestrate --plan config/paper-runner/plan.yaml
```

### API e Dashboard

```bash
# Iniciar API
pnpm api:start         # produção
pnpm api:dev           # desenvolvimento (watch mode)

# Dashboard
pnpm dashboard:dev     # servidor de desenvolvimento Vite
pnpm dashboard:build   # build de produção
```

### Testes

```bash
# Rodar todos os testes
pnpm test

# Com coverage
pnpm test:coverage

# Watch mode
pnpm test:watch
```

---

## 16. Referência de Comandos CLI

### Grupo db

| Comando | Descrição |
|---------|-----------|
| `pnpm db:migrate` | Aplica migrações pendentes |
| `pnpm db:status` | Mostra quais migrações foram aplicadas |
| `pnpm db:health` | Verifica conectividade com Postgres e Redis |

### Grupo market

| Comando | Flags | Descrição |
|---------|-------|-----------|
| `pnpm market:read` | `--symbols`, `--duration` | Conecta ao Bybit WebSocket e persiste trades/candles/snapshots |

### Grupo intelligence

| Comando | Flags | Descrição |
|---------|-------|-----------|
| `pnpm intelligence:poll` | `--source`, `--limit` | Busca dados de uma fonte específica |
| `pnpm intelligence:classify` | `--source`, `--limit` | Classifica itens com Gemini LLM |
| `pnpm intelligence:cycle` | — | Executa ciclo completo orquestrado |

### Grupo paper

| Comando | Flags | Descrição |
|---------|-------|-----------|
| `pnpm paper:run` | `--bot`, `--duration`, `--warmup`, `--variant` | Executa backtest de um bot |
| `pnpm paper:status` | — | Status do paper:run em execução |
| `pnpm paper:unlock` | — | Libera o Redis lock (emergência) |
| `pnpm paper:orchestrate` | `--plan` | Executa sequência de runs de um arquivo YAML |
| `pnpm paper:rebuild-projections` | — | Reconstrói tabelas `paper_*_projection` do event log |
| `pnpm paper:rebuild-open-positions` | — | Reconstrói `paper_open_positions_projection` |

### Grupo replay

| Comando | Descrição |
|---------|-----------|
| `pnpm replay` | Reproduz eventos do event log |
| `pnpm rebuild-projections` | Reconstrói todas as projeções |

---

## 17. Fases de Desenvolvimento

O código é anotado com identificadores de fase, permitindo desenvolvimento incremental com compatibilidade retroativa.

| Fase | Escopo |
|------|--------|
| Phase 0–1A | Fundação: event sourcing, tipos base, trader simples |
| Phase 2–3A | Dados de mercado básicos, pipeline inicial |
| Phase 3B–3E | Paper trading, SimExecutor, gates core |
| Phase 3F–3F.2C | Configuração de bots em YAML, variantes, composição de gates |
| Phase 3G–3G.4 | Lock management, ledger de open positions, paper run tracking |
| Phase 4D | Stubs de novas estratégias (trend-following, volatility-squeeze, etc.) |
| Phase 4F | Propagação de CalendarContext e IntelligenceContext para eventos |
| Phase 4L | Política de regime, lógica failOpen nos gates |
| Phase 4N | Seed de histórico de regime (regime history seeding) |
| Phase 5+ | Executor real (Bybit), reconciliador, watcher de posições |

---

## 18. Fluxo Completo de uma Operação

Exemplo: `pnpm paper:run --bot asterion --duration 2h --warmup 50`

```
CLI (main.ts)
│
├─ 1. Parse de flags (--bot, --duration, --warmup)
│
├─ 2. Carrega config YAML
│   └─ ConfigLoader.load('asterion')
│   └─ Resolve variante (se --variant especificado)
│   └─ Cria BotInstance com todos os parâmetros
│
├─ 3. Conecta ao banco
│   └─ PostgresEventStore, PaperRunStore, PaperRunLock
│
├─ 4. Adquire Redis lock
│   └─ PaperRunLock.acquire('jackfin:paper-run:lock')
│   └─ Se já travado → erro "outro run em execução"
│
├─ 5. Registra início no ledger
│   └─ paper_runs.insert({run_id, bot_id, status: 'running', started_at})
│
├─ 6. Warmup de candles
│   └─ Busca últimas 50 candles de cada timeframe do Postgres
│   └─ Seed no RingBuffer do CandleBuilder
│
├─ 7. Inicializa FakePipeline
│   └─ strategy  = StrategyRegistry.get('pullback-momentum', 'v1')
│   └─ gates     = [SymbolAllowed, SideAllowed, Stage, KillSwitch,
│                    Cooldown, MarketFreshness, NewsLock, Regime]
│   └─ risk      = StubRiskEngine
│   └─ planner   = SimplePlanBuilder
│   └─ executor  = RealisticSimExecutor({fee_bps: 6, slippage_bps: 3, max_duration: 240m})
│   └─ bus       = InMemoryEventBus
│
├─ 8. Loop de execução (por 2 horas)
│   │
│   └─ Para cada market.snapshot_created recebido:
│       │
│       ├─ a. Strategy.evaluate(context)
│       │   └─ Analisa candles, calcula momentum
│       │   └─ Retorna Signal{side: 'buy', entry: 43250.00} ou null
│       │   └─ Emite: signal.generated
│       │
│       ├─ b. Gates.evaluate(signal, context)
│       │   └─ SymbolAllowedGate → passed
│       │   └─ SideAllowedGate   → passed
│       │   └─ CooldownGate      → passed (15min desde último trade)
│       │   └─ MarketFreshnessGate → passed (snapshot recente)
│       │   └─ RegimeGate        → passed (mercado em TRENDING)
│       │   └─ NewsLockGate      → passed (sem notícias severas para BTC)
│       │   └─ Emite: decision.approved (ou decision.rejected)
│       │
│       ├─ c. Risk.evaluate(decision)
│       │   └─ Calcula tamanho da posição: $100 margem × 5x leverage = $500 noção
│       │   └─ Emite: risk.approved
│       │
│       ├─ d. Planner.build(risk_approval)
│       │   └─ Cria ExecutionPlan:
│       │       entry: 43250.00
│       │       tp:    43897.50   (entry × 1.015)
│       │       sl:    42902.50   (entry × 0.992)
│       │       qty:   0.01157 BTC
│       │   └─ Emite: plan.created
│       │
│       └─ e. SimExecutor.execute(plan)
│           └─ Abre posição simulada
│           └─ Emite: sim.order_created, sim.fill_received, sim.position_opened
│           └─ Para cada candle subsequente:
│               └─ Verifica TP/SL
│               └─ Se TP atingido (high >= 43897.50):
│                   └─ Emite: sim.position_closed {outcome: 'tp', pnl: +$6.47}
│
├─ 9. Grace period (posições abertas ao final do tempo)
│   └─ Fecha todas as posições abertas no preço atual
│   └─ Emite: sim.position_closed {outcome: 'timeout'}
│
├─ 10. Libera Redis lock
│
└─ 11. Atualiza ledger
    └─ paper_runs.update({status: 'completed', stopped_at, duration_ms: 7200000,
                          total_trades: 23, win_rate: 0.609, total_pnl: +$47.32})
```

Todos os eventos emitidos neste fluxo ficam permanentemente no `events` log, permitindo auditoria completa, replay e reconstrução de qualquer estado.

---

*Documentação gerada em 01/06/2026 — JackFin V4 Staging*

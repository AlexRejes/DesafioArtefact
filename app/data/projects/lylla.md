# Lylla

## Documentação geral do organismo cognitivo experimental

> Este documento apresenta a visão, o desenvolvimento, a arquitetura e as
> funcionalidades da Lylla. Ele distingue com cuidado o que já existe no código
> daquilo que representa uma direção de pesquisa e evolução futura.

---

## 1. Visão geral

Lylla é um organismo digital experimental de Vida Artificial (`ALife`) escrito
em Python. O projeto investiga uma pergunta ambiciosa:

> É possível construir uma inteligência artificial a partir de mecanismos
> cognitivos simples, persistentes e conectados, permitindo que estruturas mais
> complexas surjam gradualmente da interação entre percepção, memória,
> associação, avaliação, abstração e ação?

A proposta não é criar apenas uma interface conversacional que responde a
comandos. A Lylla busca desenvolver uma arquitetura cognitiva própria, capaz de
acumular experiência, formar hipóteses, consolidar conhecimento, avaliar seus
resultados, reorganizar sua memória e experimentar estratégias.

O projeto segue uma abordagem **bottom-up**, ou **de baixo para cima**:
capacidades complexas não são tratadas como uma única função central. Elas
emergem da integração progressiva de subsistemas menores.

Lylla não deve ser apresentada como uma reprodução completa do cérebro humano,
como uma inteligência geral concluída ou como um sistema consciente. Hoje ela é
uma plataforma experimental inspirada em princípios cognitivos e biológicos,
com mecanismos implementados que permitem investigar caminhos nessa direção.

---

## 2. A ideia central: construir uma inteligência integrada

Grande parte dos sistemas de IA é desenvolvida para resolver uma tarefa
específica: classificar imagens, prever palavras, responder perguntas ou
executar instruções. A Lylla parte de outro ponto de vista.

O objetivo de longo prazo é criar uma inteligência artificial integrada:

- com continuidade entre ciclos;
- com memória persistente;
- com aprendizado incremental;
- com formação e revisão de hipóteses;
- com noção de relevância;
- com controle de qualidade semântico;
- com comportamento adaptativo;
- com períodos de foco e de reorganização interna;
- com capacidade de agir em ambientes experimentais;
- com rastreabilidade suficiente para compreender como uma resposta ou relação
  foi produzida.

Neste contexto, a expressão **verdadeira inteligência artificial** não é usada
como uma alegação de que o objetivo já foi alcançado. Ela descreve uma direção:
construir um sistema que não dependa somente de respostas prontas, mas possua
processos internos conectados, memória evolutiva e aprendizado contínuo.

---

## 3. Arquitetura bottom-up

A arquitetura da Lylla não começa com uma inteligência monolítica. Ela começa
com unidades simples:

1. palavras percebidas em textos;
2. coocorrências entre palavras;
3. núcleos semânticos derivados dessas coocorrências;
4. relações estruturadas entre conceitos;
5. hipóteses reforçadas ou enfraquecidas pela recorrência;
6. conhecimento consolidado após validação;
7. pontes entre domínios;
8. abstrações e leis gerais;
9. estratégias de linguagem, ação e adaptação;
10. reflexão sobre o próprio estado.

O resultado esperado é que estruturas maiores surjam do acoplamento entre essas
camadas. Em vez de programar diretamente todas as respostas possíveis, o
sistema mantém um ciclo contínuo de percepção, associação, consolidação,
avaliação e reorganização.

### 3.1 Fluxo conceitual

```text
texto externo e corpus
        |
        v
    PERCEIVE
        |
        v
    REPRESENT  ---> coocorrências e núcleos semânticos
        |
        v
     LEXICON   ---> significado, normalização e relações lexicais
        |
        v
    ASSOCIATE  ---> relações SVO/RDF com proveniência
        |
        v
  THOUGHT_MAP  ---> hipóteses em maturação
        |
        v
  TRUTH LAYER  ---> evidência, consistência, origem e recência
        |
        v
  WISDOM_MAP   ---> conhecimento consolidado e distribuído em shards
        |
        +-------------------+
        |                   |
        v                   v
    ABSTRACT            GENERATE / DIALOGUE
  leis e padrões       linguagem e interação
```

Outros processos atuam transversalmente:

```text
FOCUS_MANAGER       atenção e seleção de corpus
DREAMER             recombinação de ideias durante ociosidade
EVALUATOR           fitness, coerência, novidade e fidelidade semântica
MORPHOGENESIS       seleção evolutiva de variantes de comportamento
SEMANTIC GOVERNANCE auditoria, quarentena e saneamento
PROCEDURAL_CORTEX   aprendizado de ação em ambientes controlados
SELF_REPORTER       autorrelato e observabilidade
```

---

## 4. Inspiração no cérebro humano

Lylla simula **funções cognitivas por analogia computacional**. Ela não tenta
reproduzir neurônios biológicos, neurotransmissores ou regiões cerebrais com
fidelidade anatômica.

As comparações abaixo são mapas de inspiração para organizar o desenvolvimento:

| Função humana aproximada | Mecanismo da Lylla | Papel no projeto |
|---|---|---|
| Percepção sensorial | `core.py` e fase `PERCEIVE` | Receber estímulos textuais, corpus e sinais do ambiente. |
| Formação de associações | `representer.py` e `associator.py` | Criar coocorrências, núcleos e relações entre conceitos. |
| Memória de trabalho e maturação | `thought_map.py` | Manter hipóteses antes da consolidação. |
| Memória semântica de longo prazo | `wisdom_map.py` e `wisdom_shards/` | Preservar relações confirmadas, consultar conceitos e distribuir memória. |
| Atenção seletiva | `focus_manager.py` | Priorizar determinados corpora e domínios em janelas de ciclos. |
| Controle executivo | `truth_layer.py`, `semantic_cleanup.py` e `semantic_enforcer.py` | Verificar consistência, filtrar ruído e impedir propagação indiscriminada. |
| Saliência afetiva | `ValenceLayer` em `truth_layer.py` | Dar maior ou menor relevância a relações conforme feedback e fitness. |
| Consolidação durante repouso | `dreamer.py` | Criar pontes entre domínios durante períodos ociosos. |
| Plasticidade e seleção adaptativa | variantes de comportamento, `evaluator.py` e torneios | Favorecer estratégias com melhor desempenho ao longo do tempo. |
| Aprendizado procedural | `procedural_cortex.py` | Aprender ações em sandboxes controlados por reforço. |
| Metacognição e autorrelato | `self_reporter.py`, reflexão e monitoramento | Observar estado interno, tendências e sinais de qualidade. |
| Linguagem e interação social | `dialogue_manager.py` e `generator.py` | Sintetizar frases, interpretar intenções e responder a estímulos. |

### 4.1 O que significa “simular um cérebro” neste projeto

No contexto da Lylla, simular um cérebro significa construir módulos que
representem capacidades cognitivas complementares e fazê-los interagir:

- perceber;
- selecionar atenção;
- memorizar;
- esquecer ou colocar em quarentena;
- associar;
- generalizar;
- avaliar;
- imaginar combinações;
- responder;
- aprender ações;
- monitorar o próprio estado.

O valor dessa abordagem está na integração. Um módulo isolado pode ser simples.
O experimento começa a ficar interessante quando memória, linguagem, valência,
governança, sonho e aprendizado procedural passam a influenciar uns aos outros.

---

## 5. Desenvolvimento do projeto

O desenvolvimento da Lylla pode ser entendido como a construção gradual de um
organismo cognitivo em camadas.

### 5.1 Fundação: ciclo contínuo e persistência

O primeiro princípio é a continuidade. A Lylla roda em ciclos, percebe arquivos
de entrada, produz saídas e salva memória. Ela não depende de uma sessão única:
o sandbox preserva estados que podem ser retomados.

Arquivos centrais:

- `core.py`: orquestração do organismo;
- `memory_manager.py`: histórico persistente de ciclos;
- `organism_sandbox/`: território de memória e operação;
- `organism_sandbox/input.txt`: entrada externa;
- `organism_sandbox/output.txt`: saída externa;
- `organism_sandbox/memory.json`: registro resumido de ciclos.

### 5.2 Representação: palavras tornam-se estruturas

O módulo `representer.py` processa texto, normaliza tokens e atualiza
coocorrências. A partir delas, deriva núcleos semânticos: vizinhanças que
registram quais conceitos aparecem conectados no material percebido.

O módulo `lexicon.py` mantém um léxico modular por domínio. Cada entrada pode
conter informações como:

- palavra;
- núcleo ou forma canônica;
- hierarquia;
- glossário;
- domínio;
- papéis semânticos;
- ciclo de atualização.

Exemplo de uma entrada lexical:

```json
{
  "word": "acoplado",
  "core": "acoplar",
  "hierarchy": ["acoplar"],
  "gloss": "fazer dois objetos, ideias ou pessoas ficarem juntos",
  "domain": "acao",
  "roles": ["irregular", "modifica"]
}
```

O projeto também inclui normalização lexical, etiquetagem morfossintática e
pontes com fontes semânticas externas, como recursos WordNet, NILC e ConceptNet.

### 5.3 Associação: estruturas tornam-se hipóteses

O módulo `associator.py` procura relações entre conceitos percebidos. As
relações são representadas de forma estruturada, com sujeito, verbo e objeto,
além de qualificadores e proveniência.

Uma relação não precisa entrar imediatamente na memória consolidada. Primeiro
ela pode ser registrada no `ThoughtMap`, onde permanece como hipótese em
maturação.

Essa separação é importante:

- `thought_map.py`: memória de hipóteses, confirmações, refutações e estados
  pendentes;
- `wisdom_map.py`: memória semântica consolidada;
- `rdf_triple.py`: estrutura relacional;
- `truth_layer.py`: validação epistêmica.

### 5.4 Conhecimento consolidado e governança

O `WisdomMap` armazena relações confirmadas e permite consulta por conceito,
cluster, direção e força. A memória pode ser dividida em `shards`, reduzindo a
pressão sobre RAM e permitindo carregar regiões relevantes conforme o cluster
ativo.

A governança semântica evita crescimento puramente quantitativo. O objetivo não
é apenas acumular relações, mas preservar relações úteis e rastreáveis.

Módulos envolvidos:

- `semantic_cleanup.py`: identifica ruído e inconsistências;
- `semantic_enforcer.py`: aplica quarentena e reclassificação por fases;
- `law_guard.py`: monitora a integridade de leis abstratas;
- `truth_layer.py`: calcula qualidade epistêmica;
- `lexical_normalizer.py`: reduz contaminação lexical.

As operações de quarentena preservam rastreabilidade. Uma relação problemática
pode ser retirada do conjunto ativo sem ser apagada destrutivamente.

### 5.5 Abstração: relações tornam-se padrões gerais

O módulo `abstractor.py` procura padrões recorrentes na sabedoria consolidada.
Quando há evidência suficiente e ausência de contradições proibitivas, o sistema
pode formar leis gerais (`LEI_*`).

Esse mecanismo representa um passo além da memorização:

```text
observações recorrentes
        |
        v
relações consolidadas
        |
        v
padrões compartilhados
        |
        v
leis abstratas candidatas
```

As leis são protegidas por validação e monitoradas pelo `law_guard.py`.

### 5.6 Linguagem, diálogo e comunicação

Lylla possui dois caminhos complementares:

- `generator.py`: geração interna de frases e registro no diário;
- `dialogue_manager.py`: processamento de estímulos externos e síntese de
  respostas.

O gerador trabalha com estratégias em múltiplos níveis (`G1..G7`), incluindo
uso de fragmentos memorizados, relações estruturadas, composição, analogia,
dedução, mudança de perspectiva e combinações híbridas. O módulo também contém
mecanismos de diversidade, memória de curto prazo, sanitização de saída e
controle de repetição.

O gerenciador de diálogo classifica intenções discursivas e propaga ativação por
fontes diferentes:

```text
entrada do usuário
      |
      v
ativação de conceito
      |
      +--> léxico
      +--> WisdomMap
      +--> vizinhos do Representer
      +--> pontes entre clusters
      |
      v
síntese da resposta
```

Esse desenho busca fazer com que uma resposta resulte da memória interna e das
relações aprendidas, não apenas de uma tabela fixa.

### 5.7 Sonho e recombinação interna

O módulo `dreamer.py` implementa uma analogia funcional com a rede de modo
padrão (`Default Mode Network`, ou `DMN`).

Quando o organismo permanece ocioso, ele pode:

- selecionar relações de clusters diferentes;
- buscar uma ponte semântica entre elas;
- formar um insight candidato;
- calcular um score epistêmico;
- rejeitar combinações fracas;
- persistir combinações viáveis;
- injetar hipóteses controladas no `ThoughtMap`.

O sonho não grava qualquer associação como verdade. Ele produz possibilidades
que continuam sujeitas a validação.

### 5.8 Evolução de comportamento

Lylla mantém uma população de variantes comportamentais. O sistema executa,
avalia e compara essas variantes por fitness.

O fitness considera dimensões como:

- estabilidade;
- compressão;
- novidade;
- coerência;
- fidelidade semântica;
- diversidade;
- penalidades por estagnação ou deriva.

Periodicamente, torneios eliminam variantes fracas e derivam novas variantes a
partir das mais aptas. Esse mecanismo representa uma forma de adaptação
evolutiva dentro do organismo.

### 5.9 Aprendizado procedural

O módulo `procedural_cortex.py` adiciona um eixo diferente do aprendizado
puramente textual. Ele permite que Lylla pratique ações em ambientes isolados e
registre valores aprendidos em `action_map.json`.

Atualmente, o repositório inclui um sandbox de jogo da velha:

- `procedural_sandboxes/sandbox_tictactoe.py`.

O córtex procedural usa exploração, reforço e atualização de valores de ação.
As recompensas também podem ser ajustadas pela camada epistêmica. Isso cria uma
ponte inicial entre “saber que” e “saber fazer”.

---

## 6. Ciclo operacional atual

Em alto nível, o loop central executa:

```text
PERCEIVE
  -> REPRESENT
  -> LEXICON
  -> ASSOCIATE
  -> THOUGHT_MAP
  -> CLEANUP_SHADOW / SEMANTIC_ENFORCE     [periódico]
  -> ABSTRACT                              [periódico]
  -> LAW_GUARD / BENCHMARK / MONITOR       [periódico]
  -> REFLECTION
  -> ACT                                   [inclui PROCEDURAL]
  -> GENERATE
  -> DIALOGUE                              [quando há entrada]
  -> EVALUATE
  -> RECORD
  -> FEEDBACK
  -> SELF_REPORT                           [periódico]
  -> MORPHOGENESIS
  -> FOCUS ou DREAM
```

Nem todas as etapas executam com a mesma frequência. Processos mais caros, como
abstração, auditoria e monitoramento, são intervalados.

---

## 7. Funcionalidades implementadas

### 7.1 Cognição semântica

- percepção contínua de corpus e estímulos externos;
- tokenização e normalização lexical;
- coocorrências e núcleos semânticos;
- léxico modular por domínio;
- relações SVO/RDF;
- deduções transitivas;
- clusters e pontes entre clusters;
- hipóteses, confirmações, refutações e quarentena;
- sabedoria consolidada distribuída em shards;
- abstração de padrões em leis.

### 7.2 Regulação interna

- avaliação de fitness;
- curiosidade adaptativa;
- valência positiva e negativa;
- decaimento periódico de valência;
- registro de evidências tóxicas;
- propagação controlada de herança e refutação;
- auditoria semântica;
- governança de memória;
- controle adaptativo de RAM;
- reflexão sobre crescimento e clusters fracos.

### 7.3 Linguagem e interação

- geração textual em múltiplas estratégias;
- anti-repetição;
- sanitização de tokens;
- memória textual de curto prazo;
- diário interno;
- canal de estímulo e resposta;
- classificação de intenção discursiva;
- comandos de foco e esquecimento;
- respostas sobre o próprio sistema;
- integração de relações por conceito.

### 7.4 Aprendizado e adaptação

- variantes de comportamento;
- seleção por torneio;
- mutação de variantes;
- eliminação emergencial de variantes instáveis;
- aprendizado procedural em sandbox;
- rastreamento de ações e recompensas;
- insights durante modo de sonho.

### 7.5 Observabilidade

O projeto inclui um observatório web:

- backend FastAPI em `server.py`;
- frontend em `interface/index.html`;
- status em tempo real;
- visualização de memória e mapa mental;
- acompanhamento de hipóteses, leis e sonhos;
- painel procedural;
- histórico de fitness;
- telemetria de RAM;
- injeção de estímulos;
- relatórios periódicos.

---

## 8. Estrutura principal do repositório

```text
Lylla/
|
|-- core.py                         loop principal e orquestração
|-- representer.py                  coocorrências e núcleos semânticos
|-- associator.py                   relações estruturadas
|-- lexicon.py                      léxico modular
|-- lexical_normalizer.py           normalização lexical
|-- pos_tagger.py                   apoio morfossintático
|-- thought_map.py                  hipóteses em maturação
|-- wisdom_map.py                   sabedoria consolidada
|-- truth_layer.py                  validação, valência e evidência
|-- abstractor.py                   abstração em leis
|-- dreamer.py                      recombinação durante ociosidade
|-- generator.py                    geração textual G1..G7
|-- dialogue_manager.py             interação externa
|-- evaluator.py                    fitness e qualidade
|-- cluster_manager.py              clusters e pontes semânticas
|-- procedural_cortex.py            aprendizado procedural
|-- self_reporter.py                autorrelato e snapshots
|-- semantic_cleanup.py             auditoria semântica
|-- semantic_enforcer.py            quarentena e reclassificação
|-- law_guard.py                    integridade de leis
|-- server.py                       API do observatório
|-- interface/index.html            interface web
|
|-- procedural_sandboxes/           ambientes de ação controlados
|-- scripts/                        auditorias, sementes e manutenção
|-- tests/                          testes automatizados
|
`-- organism_sandbox/               memória e território do organismo
```

---

## 9. Memória persistente

O diretório `organism_sandbox/` funciona como território operacional. Ele contém
o estado acumulado pelo organismo.

Alguns artefatos importantes:

| Arquivo ou diretório | Função |
|---|---|
| `memory.json` | Histórico resumido de ciclos. |
| `nucleos.json` | Coocorrências e núcleos semânticos. |
| `lexicon/` | Entradas lexicais organizadas por domínio. |
| `thought_map.json` | Hipóteses em maturação. |
| `wisdom_map.json` | Sabedoria consolidada. |
| `wisdom_shards/` | Fragmentos carregáveis da memória semântica. |
| `chunks.json` | Fragmentos textuais memorizados. |
| `short_term_memory.json` | Contexto textual recente do gerador. |
| `insights.rdf.json` | Insights viáveis do modo de sonho. |
| `dream_state.json` | Estado do módulo de sonho. |
| `action_map.json` | Valores aprendidos pelo córtex procedural. |
| `procedural_trace.jsonl` | Histórico de ações procedurais. |
| `reporter_snapshot.json` | Snapshot para monitoramento. |
| `core.log` | Log detalhado do organismo. |
| `organism_diary.txt` | Diário de produções textuais. |

Como esses arquivos mudam durante a execução, contagens específicas devem ser
tratadas como métricas dinâmicas e consultadas no observatório ou no snapshot
mais recente.

---

## 10. Qualidade, segurança semântica e explicabilidade

Uma inteligência incremental pode acumular erros com a mesma facilidade com que
acumula conhecimento. Por isso, a Lylla possui mecanismos de contenção.

### 10.1 Proveniência

As relações podem registrar:

- fonte;
- evidências;
- relações de origem;
- tags;
- ciclo de atualização;
- confiança;
- modalidade;
- temporalidade;
- polaridade;
- valência.

### 10.2 Gate epistêmico

O `truth_layer.py` calcula um score composto a partir de:

- evidência;
- consistência;
- origem;
- recência.

Esse score ajuda a decidir se uma relação candidata deve avançar no fluxo.

### 10.3 Quarentena em vez de apagamento imediato

Relações suspeitas podem sair do conjunto ativo sem desaparecer do histórico.
Isso favorece auditoria, reversibilidade e análise posterior.

### 10.4 Benchmarks e relatórios

O projeto mantém:

- benchmark lexical;
- monitor operacional;
- relatórios de limpeza semântica;
- relatórios de leis;
- logs de decisões epistêmicas;
- eventos de emergência;
- relatórios procedurais;
- testes automatizados.

---

## 11. Limitações atuais

É importante registrar com clareza o que ainda não está resolvido.

- A percepção principal ainda é textual.
- A compreensão semântica permanece limitada pelas regras, recursos lexicais,
  corpus e estruturas implementadas.
- Analogias com regiões cerebrais são funcionais, não neurobiológicas.
- O modo de sonho recombina estruturas existentes; ele não garante criatividade
  profunda ou descobertas corretas.
- A geração textual ainda pode apresentar frases frágeis, ruído lexical ou
  mistura inadequada de conceitos.
- O aprendizado procedural está em estágio inicial e possui um conjunto pequeno
  de ambientes.
- Leis abstratas precisam de validação rigorosa para não transformar repetição
  em falsa generalização.
- Autonomia operacional não implica consciência, experiência subjetiva ou
  inteligência geral humana.

Essas limitações não invalidam o projeto. Elas definem as próximas fronteiras
experimentais.

---

## 12. Direções futuras

Para aproximar a Lylla de uma arquitetura cognitiva mais abrangente, algumas
frentes naturais são:

### 12.1 Percepção multimodal

- imagens;
- áudio;
- sensores;
- eventos temporais;
- ambientes simulados mais ricos.

### 12.2 Memória mais próxima de experiências

- memória episódica explícita;
- reconstrução de contexto;
- linha temporal de eventos;
- distinção mais forte entre fato, hipótese, lembrança e previsão.

### 12.3 Planejamento e agência

- definição de objetivos;
- decomposição em etapas;
- comparação entre planos;
- previsão de consequências;
- aprendizado por resultado;
- expansão dos sandboxes procedurais.

### 12.4 Modelo de mundo

- entidades persistentes;
- causalidade;
- relações espaciais e temporais;
- simulação interna antes da ação;
- revisão de crenças diante de evidências novas.

### 12.5 Linguagem mais robusta

- melhor resolução morfológica;
- síntese discursiva longa;
- coerência entre turnos;
- redução de ruído;
- explicações ligadas à proveniência real.

### 12.6 Metacognição

- identificar incerteza;
- reconhecer ausência de conhecimento;
- solicitar evidência;
- explicar por que uma hipótese foi aceita;
- comparar desempenho antes e depois de mudanças internas.

---

## 13. Como executar

### 13.1 Organismo

```powershell
cd D:\Lylla
python core.py
```

### 13.2 Observatório web

Em outro terminal:

```powershell
cd D:\Lylla
uvicorn server:app --reload --port 8080
```

Depois, acessar:

```text
http://localhost:8080
```

### 13.3 Gerenciador de foco

Quando for desejável conduzir a atenção do organismo por uma sequência de
corpora:

```powershell
cd D:\Lylla
python focus_manager.py
```

---

## 14. Princípios do projeto

1. **Crescer de baixo para cima.** Complexidade deve surgir da integração entre
   mecanismos menores.
2. **Preservar memória.** Aprendizado sem continuidade produz apenas respostas
   isoladas.
3. **Separar hipótese de conhecimento.** Nem toda associação deve virar verdade.
4. **Manter rastreabilidade.** Relações importantes precisam de proveniência.
5. **Permitir reorganização.** Esquecimento, quarentena e sonho fazem parte do
   processo.
6. **Medir evolução.** Fitness, benchmarks e relatórios devem orientar mudanças.
7. **Evitar alegações prematuras.** Inspiração biológica não significa
   equivalência com um cérebro humano.
8. **Integrar cognição e ação.** Inteligência não é apenas linguagem: também é
   perceber consequências e aprender a agir.

---

## 15. Conclusão

Lylla é um experimento de construção cognitiva incremental. Sua arquitetura
combina percepção textual, representação semântica, memória persistente,
hipóteses, sabedoria consolidada, governança epistêmica, linguagem, sonho,
evolução de estratégias, aprendizado procedural e observabilidade.

O projeto não parte da ideia de que inteligência será encontrada em uma única
função. Ele aposta que inteligência pode ser investigada como um processo:
uma organização que percebe, registra, conecta, seleciona, revisa, imagina,
avalia e aprende continuamente.

Esse é o sentido mais importante da arquitetura bottom-up da Lylla: construir
as condições para que capacidades maiores possam emergir da cooperação entre
partes menores, mantendo abertura para experimentação e rigor para distinguir
visão de resultado comprovado.

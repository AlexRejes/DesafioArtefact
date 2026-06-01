# Legacy of Ashes: Reborn

## Visão geral

**Legacy of Ashes: Reborn** é um RPG de fantasia sombria para navegador, atualmente em estágio alpha/protótipo. O jogador cria um herói sobrevivente em um mundo devastado pela Calamidade e parte da **Vila das Cinzas** para explorar regiões perigosas, enfrentar criaturas, coletar equipamentos e descobrir fragmentos da história do mundo.

O jogo combina progressão de personagem, combate por turnos, exploração em etapas, economia, inventário, missões e recursos online. Ele possui uma interface responsiva para desktop e celular, além de suporte para instalação como Web App.

## Contexto do mundo

Depois da Calamidade, poucos sobreviventes ainda se arriscam fora dos limites da vila. Florestas cobertas pela névoa, ruínas tomadas por mercenários e santuários esquecidos escondem monstros, equipamentos, passagens secretas e sinais de um mundo que ainda não terminou de morrer.

A jornada começa na **Vila das Cinzas**, o ponto seguro do jogador entre uma expedição e outra.

## Como o jogo funciona

### 1. Criação do herói

O jogador pode testar o jogo no modo demonstrativo ou criar uma conta online. No fluxo online, existe cadastro, verificação por código enviado por e-mail, login e persistência de progresso.

Na criação do herói, o jogador escolhe:

- Nome do personagem;
- Sexo e retrato;
- Classe;
- Origem, que altera os atributos iniciais.

As classes disponíveis são:

| Classe | Recurso | Estilo de jogo |
| --- | --- | --- |
| Guerreiro | Vigor | Força, resistência, armas pesadas, escudos e contra-ataques. |
| Mago | Mana | Inteligência, dano mágico e habilidades arcanas. |
| Ladino | Foco | Agilidade, evasão, veneno e golpes críticos. |

As origens adicionam bônus ou trocas de atributos. Alguns exemplos são **Sobrevivente das Cinzas**, **Aprendiz Exilado**, **Caçador da Névoa**, **Filho da Forja** e **Passos de Sombra**.

### 2. Preparação na Vila das Cinzas

A vila funciona como o centro da jornada. Nela, o jogador administra ouro, recupera o herói e acessa construções:

| Construção | Função atual |
| --- | --- |
| Casa do Herói | Descansar, recuperar HP e organizar os quatro slots de consumíveis usados em combate. |
| Mercado | Comprar poções, armas, armaduras e acessórios. |
| Taverna | Aceitar contratos rotativos com recompensas de ouro, XP e Fama. |
| Santuário | Ativar bênçãos temporárias e redistribuir atributos ou habilidades. |
| Alquimista | Cabana construível com um protótipo interativo de alquimia. |
| Ferreiro | Construção bloqueada no progresso inicial, com protótipo interativo de forja já presente no código. |
| Mural de Crônicas | Área reservada para expansão futura. |

Na Casa do Herói:

- Descansar recupera até 80% do HP máximo e possui recarga de 30 minutos;
- A cura completa restaura 100% do HP por 200 de ouro;
- Quatro slots rápidos definem quais consumíveis podem ser usados durante batalhas.

### 3. Exploração e expedições

O mapa apresenta regiões com etapas lineares organizadas de **A1** até **C3**. Concluir uma etapa libera a próxima. Finalizar o chefe de uma região libera o acesso à seguinte.

Existem duas regiões jogáveis no estado atual:

| Região | Faixa recomendada | Conteúdo |
| --- | --- | --- |
| Floresta Sombria | Níveis 1 a 5 | Nove etapas com lobos, criaturas da névoa, elites, semichefe e chefe regional. |
| Vila Caída | Níveis 8 a 15 | Nove etapas com mercenários, elite, semichefe e chefe regional. |

O mapa também possui marcadores visuais para expedições futuras, da terceira até a décima região.

Algumas etapas possuem duas ou três subetapas. Entre combates pode aparecer o **Caminho Livre**, onde o jogador escolhe continuar, usar um item, gastar energia para recuperar HP ou abandonar a expedição mantendo as recompensas já obtidas.

### 4. Energia

A exploração utiliza um sistema de energia:

- O herói começa com 20 pontos de energia;
- Iniciar uma etapa custa 1 ponto;
- Subetapas não consomem energia adicional;
- A energia recupera 1 ponto a cada 10 minutos;
- Poções específicas também podem restaurar energia.

No modo online, o gasto de energia é registrado pelo backend.

### 5. Combate por turnos

Durante uma batalha, o jogador pode:

- Realizar um ataque básico;
- Defender para reduzir dano recebido;
- Usar uma habilidade;
- Consumir um item preparado nos slots rápidos.

O combate considera atributos, equipamentos, defesa proporcional, agilidade, precisão, esquiva, chance de crítico, dano crítico, recursos de classe, recarga de habilidades, efeitos temporários e intenção do inimigo.

Ao vencer, o jogador pode receber:

- XP;
- Ouro;
- Materiais;
- Ingredientes;
- Poções;
- Armas, armaduras e acessórios;
- Itens-chave usados para liberar chefes e notas de história.

Ao ser derrotado, o herói perde 10% do XP atual e retorna com parte do HP.

### 6. Progressão do herói

O herói evolui com XP recebido em batalhas, missões, desafios e contratos. A progressão inclui:

- Aumento de nível;
- Pontos distribuíveis de atributos;
- Equipamentos com requisitos de nível e classe;
- Árvore de habilidades;
- Escolha de uma habilidade de classe no nível 5;
- Slots de equipamento para mão principal, mão secundária, capacete, peitoral, luvas, botas, amuleto, anéis e relíquia;
- Bônus temporários e bênçãos.

Os marcos de habilidade dos níveis 10, 15 e 20 aparecem na interface como conteúdo futuro.

### 7. Inventário, raridade e economia

O inventário armazena itens concretos do jogador, incluindo quantidade, qualidade, modificadores e slot equipado.

O catálogo gerado do projeto possui:

- 305 blueprints de equipamento;
- 1.220 variantes determinísticas;
- Raridades comum, incomum, rara e lendária;
- Armas, escudos, armaduras, acessórios, consumíveis, materiais, ingredientes e itens-chave.

O Mercado:

- Possui estoque rotativo global a cada duas horas;
- Mantém poções básicas sempre disponíveis;
- Aplica filtros por categoria e classe;
- Possui limites diários para determinados produtos;
- Permite comprar várias poções de uma vez;
- Oferece a opção de colocar uma poção comprada diretamente em um slot rápido.

Também é possível vender itens pelo inventário. Equipamentos em uso e itens-chave não podem ser vendidos.

### 8. Missões, contratos e desafios

O jogo possui três formatos complementares de objetivos:

| Sistema | Funcionamento |
| --- | --- |
| Missões | Guiam os primeiros passos e acompanham objetivos da Floresta Sombria. |
| Contratos da Taverna | Três ofertas rotativas a cada quatro horas. Apenas um contrato pode ficar ativo por vez. |
| Desafios | Feitos permanentes divididos em categorias, com recompensas progressivas por tier. |

Os desafios acompanham atividades como derrotar monstros e chefes, concluir etapas, obter itens raros, completar contratos, acumular ouro, usar poções, usar habilidades, acertar críticos e esquivar de ataques.

### 9. Passagens e notas

Alguns inimigos especiais liberam itens-chave chamados **Passagens**. Esses itens revelam notas de história e podem ser necessários para alcançar chefes regionais.

Na Floresta Sombria, a Serpente das Sombras pode conceder a **Passagem I**. Na Vila Caída, derrotar Urivar concede a passagem necessária para chegar ao Trono Rubro.

### 10. Santuário

O Santuário oferece:

- Bênção do Ataque: aumenta o dano em 20% por 30 minutos;
- Bênção da Defesa: aumenta a defesa em 30% por 30 minutos;
- Recarga de quatro horas para cada bênção;
- Redistribuição de atributos;
- Redistribuição da árvore de habilidades.

A primeira redistribuição é gratuita. As próximas aumentam de preço progressivamente.

## Recursos online

O projeto possui backend próprio e modo de conta online. Os principais recursos são:

- Cadastro, verificação de e-mail, login e logout;
- Sessão persistente por cookie `HttpOnly`, com modo `Secure` configurável para HTTPS;
- Save online do personagem;
- Exclusão do personagem sem remover a conta;
- Códigos promocionais com limite de resgate;
- Chat global;
- Chat por região selecionada no mapa;
- Canal de mercado;
- Mensagens privadas entre amigos;
- Lista de amigos, busca, solicitações e presença online;
- Ranking ordenado por nível ou quantidade de abates;
- Exibição de Fama no ranking.

### Party cooperativa

Jogadores online também podem iniciar expedições cooperativas para duas pessoas:

- Criar uma sala para uma etapa;
- Entrar por código;
- Convidar amigos;
- Aceitar ou recusar convites;
- Confirmar prontidão;
- Consumir energia dos dois participantes ao iniciar;
- Lutar em turnos com estado de combate controlado pelo servidor;
- Receber XP, ouro, drops e avanço de mapa individualmente.

O backend trata concorrência de turnos, reconexão, expiração de salas, abandono de combates parados e aplicação transacional das recompensas.

## Recursos de interface

- Layout responsivo com navegação inferior no celular e barra lateral no desktop;
- Landing page com apresentação do mundo e dos sistemas;
- Guia interno do jogo;
- HUD com HP, recurso de classe, XP, energia e ouro;
- Alertas visuais para missões, desafios, inventário, chat e amigos;
- Música ambiente em rotação aleatória;
- Efeitos sonoros para mapa, notificações, level up, vitória, derrota e suspense com HP baixo;
- Controle de volume e ativação de música ou efeitos;
- Modo de tela cheia;
- Manifesto PWA e orientação para instalar o jogo na tela inicial do iPhone;
- Assets visuais em PNG, WebP e SVG.

## Estado atual dos sistemas

| Sistema | Estado |
| --- | --- |
| Combate solo por turnos | Implementado |
| Floresta Sombria e Vila Caída | Jogáveis |
| Inventário, equipamentos, drops e venda | Implementado |
| Mercado rotativo | Implementado |
| Missões, contratos e desafios | Implementado |
| Santuário, bênçãos e redistribuição | Implementado |
| Cadastro, save online e códigos promocionais | Implementado |
| Chat, amigos, mensagens privadas e ranking | Implementado |
| Party cooperativa para dois jogadores | Implementado |
| Árvore de habilidade do nível 5 | Implementada |
| Marcos de habilidade dos níveis 10, 15 e 20 | Planejados |
| Alquimia | Protótipo interativo; o resultado ainda não é aplicado ao inventário persistido |
| Forja | Protótipo interativo; o resultado ainda não é aplicado ao inventário persistido |
| Guildas | Tela informativa; implementação planejada |
| Expedições III a X | Marcadores no mapa; conteúdo jogável planejado |
| PvP | Estrutura reservada; não implementado |

## Tecnologias utilizadas

### Frontend

| Tecnologia | Uso no projeto |
| --- | --- |
| React 18 | Componentes, telas e estado da interface. |
| React DOM | Renderização da aplicação no navegador. |
| JavaScript com ES Modules | Regras de domínio, catálogos e integração com a API. |
| Vite 5 | Servidor de desenvolvimento, proxy de API e build de produção. |
| CSS modular por responsabilidade | Estilos globais, layout, componentes, telas e landing page. |
| Web App Manifest | Instalação como PWA e execução em modo standalone. |
| Fullscreen API | Modo de tela cheia quando suportado pelo navegador. |
| Local Storage | Preferências de áudio, alertas visualizados e lembrete local de instalação. |

### Backend

| Tecnologia | Uso no projeto |
| --- | --- |
| Node.js | Execução da API. |
| Express 4 | Rotas REST e middlewares. |
| PostgreSQL | Banco de dados relacional. |
| Prisma 6 | ORM, schema e migrações do banco. |
| Zod | Validação dos dados recebidos pela API. |
| Argon2id | Hash seguro de senhas. |
| Cookie Parser | Leitura da sessão persistente. |
| CORS | Controle de origem do frontend. |
| Express Rate Limit | Limites para cadastro, login, chat, amizade, party e códigos promocionais. |
| Resend | Envio de códigos de verificação por e-mail. |

### Assets, scripts e operação

| Tecnologia | Uso no projeto |
| --- | --- |
| Sharp | Otimização de imagens pelo script `npm run optimize:assets`. |
| WebP, PNG e SVG | Cenários, retratos, mapas, ícones, inimigos e itens. |
| MP3 e API `Audio` do navegador | Música e efeitos sonoros. |
| PM2 | Configuração de execução da API em produção. |
| Google Fonts | Fontes temáticas usadas pela interface. |

## Organização do projeto

```text
src/
  assets/          Imagens, mapas, ícones e sons
  audio/           Gerenciamento de música e efeitos
  components/      Componentes compartilhados e componentes de jogo
  config/          Navegação e flags
  data/            Catálogos, conteúdo e dados iniciais
  domains/         Regras de negócio separadas da interface
  screens/         Telas da aplicação

server/
  prisma/          Schema e migrações PostgreSQL
  scripts/         Scripts administrativos
  src/
    controllers/   Entrada das requisições
    routes/        Rotas REST
    services/      Regras do backend
    validators/    Schemas Zod
    middlewares/   Autenticação, rate limit e erros

docs/              Relatórios gerados e documentação auxiliar
scripts/           Scripts de assets e catálogo
shared/            Regras compartilhadas de equipamentos
```

## Como executar localmente

### Frontend

```bash
npm install
npm run dev
```

O Vite inicia o frontend e encaminha chamadas para `/api` ao backend em `http://localhost:4000`.

Opcionalmente, `VITE_API_URL` pode apontar o frontend para outra URL de API.

### Backend

```bash
npm install --prefix server
npm run db:generate --prefix server
npm run db:migrate --prefix server
npm run dev:server
```

Variáveis relevantes para o backend:

| Variável | Finalidade |
| --- | --- |
| `DATABASE_URL` | Conexão PostgreSQL. |
| `CLIENT_ORIGIN` | Origem permitida pelo CORS. |
| `PORT` | Porta da API; padrão `4000`. |
| `SESSION_COOKIE_NAME` | Nome do cookie de sessão. |
| `SESSION_TTL_DAYS` | Duração da sessão. |
| `COOKIE_SECURE` | Ativa cookie seguro em HTTPS. |
| `RESEND_API_KEY` | Habilita envio real de e-mail. |
| `EMAIL_FROM` | Remetente dos e-mails de verificação. |

Sem `RESEND_API_KEY`, o backend imprime o código de verificação no terminal durante o desenvolvimento.

### Build de produção

```bash
npm run build
```

## Scripts úteis

| Comando | Função |
| --- | --- |
| `npm run optimize:assets` | Otimiza imagens e gera versões WebP. |
| `npm run items:report` | Atualiza os relatórios do catálogo de itens em `docs/`. |
| `npm run reset-characters -- <argumentos>` | Executa o reset administrativo de personagens pelo backend. |
| `npm run promo:create --prefix server` | Cria códigos promocionais pelo backend. |
| `npm run promo:seed --prefix server` | Popula códigos promocionais iniciais. |

## Resumo

Legacy of Ashes: Reborn já possui um núcleo jogável consistente: criação de personagem, vila, progressão, combate solo, duas regiões, economia, inventário, missões, desafios e sistemas sociais online. O projeto também já possui uma base técnica preparada para crescer com novas regiões, habilidades, guildas, crafting integrado e outros modos de jogo.

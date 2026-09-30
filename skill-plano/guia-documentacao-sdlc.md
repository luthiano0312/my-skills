# Guia de Documentação por Fase do SDLC

> Objetivo: definir **como conduzir** e **o que documentar, onde, e em que formato** em cada fase do ciclo de desenvolvimento, de um jeito que funcione tanto pra humanos quanto pra agentes de código. Este guia é a base para uma skill futura.

---

## 1. Princípio geral

Cada entregável de documentação existe para reduzir risco de mal-entendido ou retrabalho. Se o risco que ele mitiga é baixo no contexto do projeto, o entregável pode ser simplificado ou eliminado — documentação por documentação não agrega valor. As tabelas de "obrigatoriedade" abaixo servem para decidir isso caso a caso, não como checklist fixo.

Regra prática para estrutura de arquivos: **multi-arquivo, pequeno e nomeado com precisão**, com um arquivo de entrada único (`CLAUDE.md`/`AGENTS.md`) que funciona como mapa. Nomeie pensando em como alguém (humano ou agente) buscaria aquilo — `how-to/configurar-auth.md`, não `misc.md`.

---

## 2. O modelo: fases pontuais + processos contínuos

Segundo a ISO/IEC/IEEE 29148:2018, Engenharia de Requisitos não é uma fase única — é um processo guarda-chuva com sub-processos, alguns pontuais e outros contínuos ao longo de todo o projeto:

```
┌─────────────────────── ENGENHARIA DE REQUISITOS ───────────────────────┐
│                                                                        │
│  1. LEVANTAMENTO  →  2. ANÁLISE  →  3. ESPECIFICAÇÃO  →  4. VALIDAÇÃO  │
│     (elicitação)      (estruturação)   (documentação)      e GESTÃO    │
│                                                             (contínua) │
└──────────────────────────────────┬─────────────────────────────────────┘
                                    ▼
                    Projeto (Design) → Implementação → Testes → Deploy → Manutenção
```

Isso significa duas categorias distintas de trabalho, que pedem tratamento diferente:

**Atividades pontuais** — acontecem, geram um artefato, e (idealmente) se encerram: Levantamento, Análise, Design/System Design. Cobertas nas seções 4 a 6.

**Processos contínuos** — não têm fase fixa, são acionados a qualquer momento do projeto: Especificação formal, Verificação e Validação, Gestão de Requisitos. Cobertos na seção 7. É aqui que entram cenários como "descobrimos um requisito esquecido durante o Design" ou "um requisito mudou no meio do projeto" — que não são falha de processo, são esperados.

**Regra prática pra saber em qual das duas categorias uma tarefa cai:**
- "Estou descobrindo ou organizando algo novo" → atividade pontual (seções 4–6)
- "Estou checando se algo já documentado está correto, ainda vale, ou precisa mudar" → processo contínuo (seção 7)

---

## 3. Estrutura de pastas proposta

```
CLAUDE.md                          ← carregado sempre, curto e denso, aponta pro resto
AGENTS.md                          ← alias/equivalente genérico do CLAUDE.md, se aplicável

docs/
├── 01-requisitos/
│   ├── stakeholders.md            (registro de stakeholders)
│   ├── srs.md / backlog.md        (um ou outro, não os dois)
│   ├── casos-de-uso/              (um arquivo por caso de uso, ou agrupados por módulo)
│   ├── regras-de-negocio.md       (catálogo, quando numerosas)
│   ├── glossario.md
│   ├── escopo.md                  (in scope / out of scope)
│   └── rastreabilidade.md
│
├── 02-design/
│   ├── arquitetura-hld.md         (visão geral, diagramas de componentes)
│   ├── system-design.md           (quando há requisitos de escala relevantes)
│   ├── modelo-de-dados.md         (schema físico, evoluído do DER conceitual)
│   ├── apis/                      (specs OpenAPI/Swagger por serviço)
│   ├── ui-ux/                     (wireframes, protótipos navegáveis)
│   └── adr/
│       ├── 0002-monolito-vs-microsservicos.md   ← ativos
│       ├── 0015-...
│       └── archive/
│           └── 0003-usar-mongodb.md              ← substituídos, número original mantido
│
├── how-to/                        (guias operacionais: setup, deploy, troubleshooting)
├── reference/                     (convenções de código, comandos, padrões de commit)
└── explanation/                   (contexto de negócio, "por que o sistema existe assim")
```

A separação `01-requisitos` / `02-design` não precisa ser rígida — em times ágeis isso vive mais como backlog + ADRs vivos do que como pastas cheias de documento formal. A estrutura serve de referência para saber **onde colocar** algo quando ele precisar existir.

---

## 4. Levantamento (Elicitação)

### Objetivo
Entender **o problema** antes de pensar na solução. Responder "o que o sistema precisa fazer e por quê?" — não "como ele vai fazer".

### Como fazer — técnicas

| Técnica | Quando usar | Observação |
|---|---|---|
| **Entrevistas** | Aprofundar em pontos específicos | Estruturadas ou semiestruturadas; ótimas para esclarecer ambiguidade na hora |
| **Questionários** | Muitos usuários espalhados geograficamente | Escala bem, mas é menos profundo que entrevista |
| **Observação direta / Etnografia** | Entender o processo real de trabalho | Revela problemas que o próprio usuário nem menciona, por já ser "natural" pra ele |
| **Workshops / JAD** | Alinhar visões divergentes rapidamente | Reúne múltiplos stakeholders ao mesmo tempo |
| **Análise de Documentos** | Sistemas legados, processos já documentados | Manuais, relatórios, planilhas em uso |
| **Protótipos** | Requisitos de interface, descoberta de necessidades ocultas | Nessa fase servem para **descobrir** requisitos (o usuário vê e lembra "ah, também preciso de...") |
| **Casos de Uso** | Extrair cenários de interação | Aqui funcionam como **técnica de elicitação** — puxam requisitos que o usuário não citaria diretamente |
| **User Stories / Storytelling** | Métodos ágeis | Formato: "Como [usuário], eu quero [ação] para que [benefício]" |

Passos: identificar stakeholders → coletar (técnicas acima) → negociar prioridades preliminarmente → documentar inicialmente → validar com stakeholders → começar a gerir mudanças desde já.

### Boas práticas
- Envolver o **usuário final**, não só o gestor.
- Combinar mais de uma técnica pra compensar pontos cegos de cada uma.
- Registrar requisitos assim que forem ditos, mesmo que de forma bruta.
- Validar continuamente com o stakeholder, não guardar tudo pro final.

### Problemas comuns
Requisitos implícitos não ditos; conflito entre stakeholders não resolvido; requisitos voláteis sem controle; excesso de detalhe técnico cedo demais (foco deve ser o problema, não a solução); requisito vago demais pra ser testável; falta de envolvimento do usuário final.

### O que produzir e onde vai

| Documento | Obrigatório quando | Vai em |
|---|---|---|
| SRS **ou** Backlog de User Stories | contrato/licitação, sistema regulado, terceirização → SRS; time ágil → Backlog | `docs/01-requisitos/srs.md` ou `backlog.md` |
| Registro de stakeholders | quase sempre (mesmo informal) | `docs/01-requisitos/stakeholders.md` |
| Diagramas de Casos de Uso (elicitação) | muitos atores, fluxos complexos | `docs/01-requisitos/casos-de-uso/` |
| Protótipos | interface complexa ou incerteza de UX | `docs/02-design/ui-ux/` (versão validada) |

---

## 5. Análise

### Objetivo
Transformar os requisitos brutos coletados em algo estruturado, classificado e formal que a equipe técnica consegue usar para projetar o sistema.

### Como fazer

**1. Classificar** em Requisitos Funcionais (RF — o que o sistema faz) e Não-Funcionais (RNF — como se comporta: performance, segurança, usabilidade, disponibilidade, escalabilidade).

**2. Verificar a qualidade de cada requisito** contra estes atributos (ISO/IEC/IEEE 29148:2018):

| Atributo | Significado |
|---|---|
| Necessário | Realmente precisa existir |
| Não ambíguo | Só uma interpretação possível |
| Completo | Não deixa lacunas |
| Singular | Trata de uma única coisa por vez |
| Factível/viável | Possível de implementar no prazo/orçamento |
| Verificável | Dá para testar se foi atendido |
| Correto | Reflete a real necessidade do stakeholder |
| Conforme | Segue o padrão/template adotado |

O **conjunto** de requisitos deve ser: completo, consistente e delimitado (bounded).

**3. Priorizar** — MoSCoW (Must/Should/Could/Won't) ou matriz impacto x urgência.

**4. Definir o escopo** — limites do sistema (o que é responsabilidade dele vs. externo), restrições de negócio e técnicas, critérios de aceitação, registro formal (Documento de Visão). Separar claramente "in scope" e "out of scope".

**5. Extrair e catalogar regras de negócio** — dentro dos RFs quando poucas; catálogo separado quando numerosas ou reutilizadas por vários módulos.

**6. Modelar** — casos de uso formalizados (UML + fluxo principal/alternativo/pré-pós-condições), diagramas de fluxo para regras complexas, DER conceitual, diagrama de classes conceitual (se orientado a objetos), protótipos de baixa fidelidade (aqui para **validar**, não descobrir), glossário de termos.

### Boas práticas
- Manter rastreabilidade: todo requisito, regra e caso de uso deve linkar de volta a uma necessidade de stakeholder.
- Revisar contra a tabela de qualidade antes de encerrar a fase.
- Separar regras de negócio em catálogo próprio quando numerosas.
- Escopo sempre por escrito e validado, nunca implícito.

### Problemas comuns
Misturar RF e RNF sem classificar; regras de negócio espalhadas sem catálogo; escopo não formalizado; pular a verificação de qualidade dos requisitos; modelagem excessivamente técnica cedo demais (isso é papel do Design).

### O que produzir e onde vai

| Documento | Obrigatório quando | Vai em |
|---|---|---|
| SRS/ERS com RF/RNF classificados | sempre que houver SRS formal | `docs/01-requisitos/srs.md` |
| Documento de Visão / Escopo | quase sempre, mesmo que curto | `docs/01-requisitos/escopo.md` |
| Catálogo de Regras de Negócio | regras numerosas/reutilizadas | `docs/01-requisitos/regras-de-negocio.md` |
| Casos de Uso (formalizados) | mesmo critério do levantamento | `docs/01-requisitos/casos-de-uso/` |
| DER conceitual / Diagrama de Classes conceitual | modelagem relevante | `docs/01-requisitos/` (evolui pro Design) |
| Glossário | domínio complexo/especializado | `docs/01-requisitos/glossario.md` |
| Matriz de Rastreabilidade (baseline inicial) | sistemas regulados, projetos grandes/multi-equipe | `docs/01-requisitos/rastreabilidade.md` |

---

## 6. Design (incluindo System Design)

### Objetivo
Responder **como** o sistema vai atender ao que foi levantado e analisado — parte do SRS/ERS validado como insumo, sem reabrir o "o quê".

### Como fazer

**1. HLD antes de LLD.** Arquitetura geral primeiro (monolito, microsserviços, event-driven, escolha de tecnologias, fluxo de dados macro), detalhe de implementação depois (classes, schema físico, contratos de API, algoritmos).

**2. Partir sempre dos RNFs validados**, não de preferência tecnológica da equipe — um RNF como "disponibilidade 99,9%" vira decisão concreta de arquitetura (replicação, load balancer, multi-região).

**3. Validar cada decisão contra restrições já identificadas na Análise** (legado, orçamento, prazo, equipe).

**4. Formalizar contratos de API e schemas antes da implementação começar**, para times paralelos trabalharem sem bloqueio.

**5. Aprofundar em System Design quando a escala justificar** — escalabilidade (vertical vs. horizontal), disponibilidade/tolerância a falha, balanceamento de carga, cache, filas/processamento assíncrono, trade-offs de consistência (teorema CAP), sharding, estimativas de capacidade. Isso é HLD levado a sério, não uma fase separada — só vale aprofundar quando o sistema tem crescimento esperado, alto tráfego ou natureza distribuída; em sistema pequeno/interno é over-engineering.

### Boas práticas
- Documentar o **porquê** das decisões (ADRs — seção 8), não só o resultado.
- Validar contra RNFs, não só contra RFs.
- Prototipar/testar decisões arriscadas antes de comprometer o sistema inteiro (spike técnico).
- Explicitar trade-offs — toda decisão de Design troca uma coisa por outra.
- Revisitar a arquitetura em checkpoints, não só uma vez no início.

### Problemas comuns
Over-engineering (desenhar pra escala que o sistema nunca vai ter); under-engineering (ignorar RNFs de escala conhecidos); pular direto pra tecnologia antes de entender o problema; ignorar restrições da Análise (legado, orçamento, equipe); não documentar o porquê das decisões.

### O que produzir e onde vai

| Documento | Obrigatório quando | Vai em |
|---|---|---|
| Documento de Arquitetura (HLD) | sempre | `docs/02-design/arquitetura-hld.md` |
| System Design (aprofundamento) | sistemas com escala/tráfego relevante | `docs/02-design/system-design.md` |
| Design Detalhado (LLD) — schema físico | sempre que houver banco de dados | `docs/02-design/modelo-de-dados.md` |
| Especificação de APIs (OpenAPI/Swagger) | integração entre serviços/times | `docs/02-design/apis/` |
| ADRs | decisão difícil de reverter ou de alto impacto | `docs/02-design/adr/` |
| Design de UI/UX detalhado | interface relevante | `docs/02-design/ui-ux/` |

---

## 7. Processos contínuos — Especificação, Verificação/Validação, Gestão de Requisitos

Diferente das seções 4–6, isto não é "uma fase" — é trabalho que pode ser acionado **no início** (linha de base), **durante** (mudança de requisito, ADR substituído, requisito esquecido descoberto tarde) e **depois** (auditoria, manutenção) do projeto.

### Especificação formal
Consolidação contínua em documentos padronizados — StRS (Stakeholder Requirements Specification), SyRS (System Requirements Specification), SRS (Software Requirements Specification), ConOps/OpsCon (Concept of Operations). Não é um evento único: é revisitada toda vez que o entendimento do problema muda.

### Verificação e Validação
- **Verificação**: os requisitos especificados estão corretos e seguem os critérios de qualidade da seção 5 (não ambíguo, verificável, etc.)?
- **Validação**: eles de fato atendem à necessidade real do stakeholder? Isso se conecta com os Testes de Aceitação lá na frente do ciclo.

Pode (e deve) ser acionado a qualquer momento — não só uma vez no fim da Análise. É a atividade certa quando a pergunta é "esse requisito que já existe ainda está bom?", não "que requisito novo existe?".

### Gestão de Requisitos
Processo contínuo de controlar mudanças, manter baseline e rastreabilidade **ao longo de todo o projeto** — não termina quando a codificação começa. É aqui que entram os cenários do dia a dia:
- Um requisito muda no meio do projeto → atualizar SRS/backlog + matriz de rastreabilidade, registrar o motivo da mudança.
- O Design revela que um requisito estava mal especificado ou incompleto → volta pontual à Análise; isso é normal, só em cascata puro é visto como falha de processo.
- Um ADR é substituído → ver seção 8, mas o gatilho de "por que essa decisão mudou" costuma vir de uma mudança de requisito/RNF capturada aqui.

### Onde vive
Atualiza os mesmos arquivos das seções 4–6 (`srs.md`, `rastreabilidade.md`, `escopo.md`) em vez de criar arquivos novos — o processo contínuo é sobre **manter vivo** o que já existe, não sobre gerar um documento à parte.

---

## 8. ADRs — regras de uso

- Um ADR por decisão **difícil de reverter** ou de **alto impacto arquitetural** (banco de dados, linguagem/framework, monólito vs. microsserviços, síncrono vs. assíncrono). Renomear variável não é ADR.
- Numerado sequencialmente: `0001-titulo.md`, `0002-titulo.md`.
- Formato fixo e curto: **Status → Contexto → Decisão → Consequências**.
- **Imutável quando aceito.** Decisão mudou? Cria-se um novo ADR que referencia o antigo (`Status: Substituído por ADR-0015`). O conteúdo do ADR antigo nunca é reescrito.
- Vive versionado junto do código, em `docs/02-design/adr/`.
- É a ponte mais direta entre RNF (levantado na fase de Requisitos) e decisão técnica concreta (tomada no Design) — vale linkar o ADR de volta ao RNF que o motivou, quando fizer sentido para a rastreabilidade.

**Arquivamento de ADRs substituídos (`adr/archive/`)**

Em workflows com agente de código, deixar ADRs ativos e substituídos misturados na mesma pasta gera *context rot*: o agente carrega decisões descartadas junto com as válidas. A separação recomendada:

- `docs/02-design/adr/` → só ADRs com `Status: Aceito` (ativos)
- `docs/02-design/adr/archive/` → ADRs com `Status: Substituído por ADR-XXXX`

Regras para isso funcionar de verdade:

1. **O número original nunca muda** ao mover um ADR para `archive/` — a ordem cronológica é o valor principal do ADR, mudar o número quebra isso.
2. **Atualizar o `Status` antes de mover.** O ADR arquivado continua imutável em conteúdo, mas o campo `Status` é justamente o registro de que ele foi substituído — isso é atualização de metadado, não reescrita da decisão.
3. **O vínculo é bidirecional**: o novo ADR referencia o antigo (`Substitui ADR-0003`) e o antigo aponta pro novo (`Substituído por ADR-0015`).
4. **A separação de pastas só evita context rot se o carregamento respeitar isso.** Se o `CLAUDE.md` mandar carregar `adr/` de forma recursiva, `archive/` entra junto e a separação não ajuda em nada. É preciso ser explícito: carregar `adr/*.md` (não recursivo) por padrão, e só abrir `adr/archive/` quando for investigar por que uma abordagem anterior foi descartada ou antes de propor uma mudança arquitetural grande — inclua essa instrução literalmente no `CLAUDE.md`, não deixe implícita.

---

## 9. Arquivo de entrada (`CLAUDE.md` / `AGENTS.md`)

Função: ser o **roteiro sempre carregado** que diz onde procurar o quê — o equivalente ao README para agentes, mas escrito para ser lido em toda sessão (por isso precisa ser enxuto).

Deve conter:
- Convenções do projeto (estilo de código, padrão de commit) — **de forma explícita e literal**, não "siga o padrão do projeto"
- Comandos executáveis (`npm run test:unit`), não descrições vagas ("rode os testes")
- Links diretos para `docs/02-design/arquitetura-hld.md`, `docs/02-design/adr/`, `docs/how-to/`
- Aviso para sempre checar ADRs antes de propor mudança arquitetural relevante (evita o agente "reinventar" uma decisão já descartada)
- Regra explícita de carregamento dos ADRs: por padrão só `docs/02-design/adr/*.md` (ativos); `docs/02-design/adr/archive/` só quando for investigar uma decisão passada ou antes de propor mudança arquitetural grande — sem essa linha explícita, a separação em `archive/` não impede o agente de carregar tudo mesmo assim

Não substitui a documentação detalhada — é o índice que evita que a fragmentação (boa pra humanos) vire um problema de descoberta (ruim pra agentes).

---

## 10. Boas práticas transversais (valem para todas as fases e processos)

- **Rastreabilidade**: todo requisito, regra de negócio, decisão de design e caso de uso deve poder ser ligado de volta a uma necessidade de stakeholder.
- **Uma fonte de verdade por informação.** Duplicação é ainda mais perigosa com agente de código: ele pode pegar a versão errada e agir sobre ela sem "desconfiar" como um humano desconfiaria.
- **Nomear pensando em busca**: arquivo pequeno + nome descritivo funciona como índice de busca tanto para humano quanto para agente.
- **Documentar o porquê, não só o resultado** — vale para ADRs, mas também para decisões de escopo e regras de negócio.
- **Revisitar em checkpoints, não só uma vez**: arquitetura, escopo e regras de negócio evoluem — é justamente o que a seção 7 formaliza.

---

## 11. Checklist rápido ao decidir se algo vira documento formal

1. Essa informação, se perdida, causa retrabalho caro ou mal-entendido caro? → documentar.
2. É uma decisão difícil de reverter? → ADR.
3. Vários times/pessoas vão precisar consultar isso de forma assíncrona? → documento formal, não conversa/memória.
4. Existe exigência contratual, regulatória ou de auditoria? → formal é obrigatório.
5. É uma tarefa nova (descobrir/organizar) ou manutenção de algo que já existe (mudou, precisa ser revalidado)? → a segunda cai na seção 7, não gera documento novo, atualiza o existente.
6. Nenhum dos anteriores e o time é pequeno/ágil? → pode viver como backlog/comentário/ADR curto, sem exigir documento completo.

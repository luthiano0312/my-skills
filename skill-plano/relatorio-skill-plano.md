# Relatório: Design da Skill `plan`

> Consolidação da entrevista (`/grill-me`) feita sobre a skill `plan`, terceira skill do conjunto descrito em `relatorio-skill-implementacao.md` (`docs` → `plan` → `implementacao`). Usa como base o `plano.md` do projeto Recolhe (etapas 5–8), tratado como exemplo editável, não como padrão fixo.

---

## 1. Contexto extraído dos arquivos (antes desta entrevista)

**SDLC e engenharia de requisitos** (`Fases do desenvolvimento de sistemas.md`, `Engenharia de requisitos.md`, `projeto.md`): Levantamento e Análise são sub-processos de um "guarda-chuva" contínuo (ISO/IEC/IEEE 29148:2018); Projeto (Design) é fase distinta que parte do SRS validado; System Design é HLD aprofundado, não fase separada.

**`guia-documentacao-sdlc.md`**: já formaliza a skill `docs` — estrutura de pastas (`docs/01-requisitos/`, `docs/02-design/`), padrão de arquivamento de ADRs (`adr/` ativos vs. `adr/archive/`, número original preservado, status atualizado antes de mover), e o princípio-chave citado várias vezes nesta entrevista: **"uma fonte de verdade por informação"** (seção 10) — duplicação é ainda mais perigosa com agente de código.

**`Conversa.md`**: conversa anterior que estabeleceu as 7 fases clássicas do desenvolvimento e onde o System Design se encaixa (dentro do Projeto/Design).

**`plano.md`**: exemplo concreto de plano de implementação (projeto Recolhe, etapas 5–8), com cabeçalho de Status/Escopo/Pré-condição/Fontes de verdade, 8 seções numeradas, e etapas contendo tasks com `Fazer`/`Não alterar`/`Entregáveis`/`Critério de conclusão`. Serviu como base editável para esta entrevista.

**`relatorio-skill-implementacao.md`**: já define 3 skills (`docs` existente, `plan` a criar, `implementacao` consumindo `plano.md`), e já antecipa dois gatilhos que devolvem trabalho pra fora do ciclo de implementação: contradição documental nova, e 3 rodadas de correção sem convergir. Também já registra `registro.md` (`docs_sistema_recolhe/execucao/registro.md`) como rastreamento central de status por task, e `achados/` como pasta de relatórios persistidos.

---

## 2. Decisões já fechadas

### 2.1 Escopo e ritmo da skill
| Decisão | Porquê |
|---|---|
| A skill opera **um marco por vez**, não o projeto inteiro | Requisitos/prioridades mudam entre marcos; planejar tudo de uma vez força fatiar tasks distantes no tempo com informação que ainda vai ficar velha |
| Tem uma seção dedicada de análise do estado atual + definição de marcos, no espírito de seções-por-fase da skill `docs` | Reaproveita o fato de `docs` já trabalhar com escopo como base pra identificar o próximo marco |
| `escopo.md` (docs/01-requisitos) permanece a visão do sistema inteiro; a skill nunca o reescreve | "Uma fonte de verdade por informação" — reescrever por marco faria perder o rastro do escopo total ou forçar reescrita repetida |
| Fonte primária de "o que já foi feito": `registro.md` da skill `implementacao`, quando existir; repositório só como checagem de sanidade (primeiro marco ou suspeita de divergência) | Evita a skill `plan` reinventar rastreamento de estado que a `implementacao` já mantém |
| A seção de análise **propõe** um recorte de marco candidato (via escopo + prioridade MoSCoW/backlog, agrupado por dependência técnica) e **pede confirmação/ajuste** | "Onde corta o marco" é decisão de risco/prioridade, não fato verificável — não pode ser decidido sozinha pela skill |

### 2.2 Fatiamento de task
| Decisão | Porquê |
|---|---|
| Critério de divisão: uma task deve conter no máximo **um comportamento fim-a-fim independentemente testável e revisável** | Critério objetivo (não subjetivo, não contagem de linhas/camadas): dois+ itens com critério de sucesso verificável independente, que não precisam ser commitados juntos, é sinal de dividir. Testado contra o `plano.md`: Task 8.6 (pagamentos) falha o teste (as 3 actions não dependem uma da outra); Task 8.3 (cadastro de OS) passa (backend+frontend juntos são um único comportamento fim-a-fim) |

### 2.3 `Não alterar`
| Decisão | Porquê |
|---|---|
| Duas categorias com rigor diferente: **rastreável** (ADR/regra/escopo — obrigatório, referencia a origem) vs. **boa prática sem fonte** (dedução técnica sem doc, sugestão cortável na confirmação) | Itens sem fonte documentada podem estar errados ou fora de contexto sem alguém validar; itens rastreáveis não têm essa ambiguidade |

### 2.4 Arquivamento do plano
| Decisão | Porquê |
|---|---|
| Um arquivo por marco, arquivado no mesmo padrão dos ADRs (atual no caminho padrão carregado; anteriores em pasta tipo `planos/marco-N.md`, lidos só pela análise do próximo marco) | Evita tanto perder histórico de decisões de deferimento entre marcos quanto o *context rot* de carregar planos de marcos passados durante a implementação do atual |

### 2.5 Gatilhos vindos da `implementacao` durante um marco aberto
| Decisão | Porquê |
|---|---|
| Contradição documental nova → vai para a skill **`docs`**, não para `plan` | É V&V/Gestão de Requisitos (seção 7 do guia), processo contínuo explicitamente descrito como acionável a qualquer momento — domínio de requisitos/análise/design, não de fatiamento de implementação |
| Estouro de 3 rodadas de correção sem convergir → **é** escopo do `plan` | Sinal de que a própria task foi mal fatiada/especificada — quem escreve a especificação é o `plan`; não tem pra quem mais devolver |
| Nesses dois casos, o marco em andamento é editado **in place** (task re-especificada), nunca fechado/reaberto | Fechar o marco no meio quebraria a premissa de "marco = recorte coerente por dependência e prioridade" e forçaria reconciliação estranha no `registro.md` |
| Ao re-especificar, `plan` lê **só os artefatos já persistidos** (task original + `achados/task-X-revisao-*.md`) — nunca reabre diff/código | Reinvestigar código seria duplicar o papel do revisor da `implementacao`, quebrando a responsabilidade única que já motivou separar as skills |

### 2.6 Cortes estruturais no `plano.md` (vs. o exemplo original)
| Seção original | Decisão | Porquê |
|---|---|---|
| 1. Objetivo | **Removida** | Puramente redundante com a seção 8 (Resultado esperado), sem sobrar papel próprio |
| 2. Limites globais | Removida como texto restatado → vira referência curada | Duplicava conteúdo de ADRs/regras já documentados; risco de desatualização quando a fonte mudar |
| 3. Tecnologias e convenções | Sai → vira referência (arquitetura-hld/convenções) | Não é decisão do marco, é da stack do projeto inteiro (decidida na etapa 4/ADRs); mesmo risco de duplicação da seção 2 |
| 5. Definition of Done | Sai → vai para convenções de desenvolvimento, referenciado | Não muda de task pra task nem de marco pra marco; merece documento estável próprio |
| 6. Gates de qualidade acumulativos | **Removida inteira** | "Gate para iniciar etapa X" não se aplica (ordem sempre sequencial); "Gate para homologação local" já é convenção de testes; "Gate para ambiente contratado"/"Gate para produção" não são testáveis nesta fase do projeto |
| "Gate da etapa X" (subseção dentro de cada etapa) | Removida | Redundante com a soma dos "Critério de conclusão" das tasks daquela etapa — sem checagem cruzada real identificada |
| 7. Ordem recomendada de commits | Sai do `plan` inteiramente → `implementacao` sugere a mensagem no momento da aprovação da task | O próprio `plano.md` já admite que a previsão de commit raramente bate com o resultado efetivo; sugerir no momento do relatório final é mais preciso e não custa escopo extra ao `plan` |
| 8. Resultado esperado ao final das etapas | **Mantida** | É a única das duas (vs. seção 1) que pode ser derivada mecanicamente das tasks já fatiadas, servindo de sanity check |
| Cabeçalho "Fontes de verdade" | Vira o ponto de referência central e curado do plano (só o relevante a este marco), substituindo as antigas seções 2 e 3 | Cada `Não alterar` rastreável referencia de volta a um item dela, em vez de cada task carregar link solto sem relação com o cabeçalho |
| "Critério de conclusão" por task | **Mantido** | Não é redundante — é o nível certo de granularidade, ao contrário do gate de etapa |

---

## 3. Estrutura do `plano.md` aprovado para a skill

```
Cabeçalho
├── Status e identificação do marco
├── Recorte do marco (referência ao escopo global)
├── Pré-condições externas
└── Fontes de verdade curadas (caminhos reais)

Ordem e dependências
├── A ordem física das tasks é a sequência prática sugerida
└── Somente dependências obrigatórias justificadas em diagrama/tabela

Etapas opcionais, só quando agruparem trabalho útil
└── Tasks com ID estável após aprovação
    ├── Fazer
    ├── Não alterar ([Fonte: caminho#trecho] ou [Decisão deste marco])
    ├── Entregáveis
    └── Critério de conclusão observável

Resultado esperado (síntese derivada das tasks, sem novas promessas)
```

Permanecem fora do plano as antigas seções globais de Objetivo, Limites, Tecnologias, Definition of Done, gates acumulativos, gates de etapa e sugestão de commits: vivem nas fontes, convenções ou no fluxo da `implementacao`.

---

## 4. Resolução dos sete ramos e ajuste após leitura do plano real

1. **Resultado esperado**: derivar dos Entregáveis e Critérios de conclusão; lacuna volta para as tasks, nunca vira promessa inventada. O plano real confundia “pronto para homologação física” com homologação efetivamente realizada.
2. **Dependências e ordem**: inferir relações obrigatórias a partir de pré-condições/artefatos e justificar cada seta; a ordem **física** das tasks é a sequência prática sugerida. O usuário valida o recorte e a proposta. Refatiar e reorganizar tasks para remover ciclos e minimizar vai e vem: no plano real, a 8.3 exige reconciliação prevista só na 8.5.
3. **Etapas**: opcionais; IDs de task não dependem da posição da etapa e devem permanecer estáveis após aprovação/execução.
4. **Arquivamento**: preservar raiz de documentação já usada. No Recolhe: `docs_sistema_recolhe/plano.md`, `docs_sistema_recolhe/planos/`, `docs_sistema_recolhe/execucao/registro.md`. Em projetos novos sem convenção: `docs/03-execucao/plano.md`, `planos/` e `registro.md` na mesma área. Planos encerrados são lidos seletivamente ao planejar o próximo marco, não por padrão na implementação.
5. **Registro**: a skill `plan` inicializa linhas das tasks como “não iniciada” ao salvar o plano aprovado, na mesma conversa; a skill `implementacao` gerencia estados, achados, revisão e commit em conversas novas. Histórico e vínculos de tasks substituídas não são apagados.
6. **Invocação**: comando ou linguagem natural, sem parâmetro obrigatório. Mesmo via comando, confirmar **antes de iniciar análise**; propor recorte ao usuário e pedir aprovação explícita da proposta antes de gravar plano/registro. A autorização para analisar não autoriza salvar.
7. **`Não alterar`**: `[Fonte: caminho#trecho]` para restrição verificada; `[Proposta sem fonte]` apenas no rascunho, removida ou explicitamente aceita como `[Decisão deste marco]` antes de salvar. Todos os itens finais são obrigatórios para `implementacao`.

**Ajuste adicional ao critério de fatiamento:** “um comportamento fim a fim” não cobre configuração de SQLite, migrations e outras tasks técnicas do plano real. A regra geral é **uma entrega coerente, testável e revisável independentemente**; comportamento fim a fim é a preferência para funcionalidades, resultado técnico verificável para infraestrutura.

---

## 5. Estado da decisão

Os sete ramos antes em aberto foram resolvidos com o usuário, assim como o ajuste do critério de fatiamento. Implementação da skill: `.agents/skills/plan/SKILL.md`. O `skill-plano/plano.md` é insumo histórico para refatorar no projeto Recolhe, não foi convertido automaticamente no novo plano nem usado para criar um `registro.md` real: a própria skill exige confirmação e aprovação antes disso.

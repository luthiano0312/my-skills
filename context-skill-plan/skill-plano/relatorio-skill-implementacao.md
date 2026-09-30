# Relatório: Design da Skill de Implementação

> Consolidação da entrevista (`/grill-me`) feita sobre o workflow original de implementação (`Conversa.md`) e o `plano.md` do projeto Recolhe. Objetivo: dar contexto completo para avaliar a ideia antes de a skill ser efetivamente escrita.

---

## 1. Ponto de partida

Havia dois materiais na mesa, escritos em momentos diferentes e sem estar alinhados entre si:

1. **Um workflow genérico** (`Conversa.md`) descrevendo um ciclo `implementação → revisão independente → correção → commit`, com prompts prontos para "implementador" e "revisor". Esse workflow tinha pontos deixados propositalmente vagos (ex: "correção pode ser na conversa do implementador ou numa conversa específica" — sem decidir qual).
2. **Um plano concreto** (`plano.md`) já fatiado em 17 tasks (etapas 5 a 8.10), cada uma com `Fazer`/`Não alterar`/`Entregáveis`/`Critério de conclusão`, mais gates acumulativos por etapa e uma sugestão de convenção de commits por etapa (squash).

A pergunta original era: **transformar esse workflow em uma skill, no mesmo espírito da skill `docs`, mas voltada para implementação.**

A entrevista serviu para expor que o workflow genérico tinha ambiguidades que só apareciam quando confrontadas com um plano real — e resolver cada uma antes de qualquer código de skill ser escrito.

---

## 2. Decisão estrutural mais importante: três skills, não uma

A primeira pergunta da entrevista foi sobre um pressuposto que o workflow original nem menciona: **de onde vem um plano já bem fatiado?** Sem isso, os prompts de implementação/revisão (que citam "Task 5.1 de [[plano]]") não têm o que consumir.

A resposta gerou a decisão mais importante de todo o processo: **dividir responsabilidades em três skills separadas**, em vez de uma só:

| Skill | Responsabilidade | Papel do `plano.md` |
|---|---|---|
| `docs` (já existe) | Documentação de requisitos/design (SRS, ADRs, arquitetura) | Não mexe |
| **`plan`** (a criar depois) | Fatiar/gerar o plano de implementação, com granularidade correta, dependências e gates | **Produz** o `plano.md` |
| **`implementacao`** (esta) | Executar o ciclo implementador→revisor→correção→commit sobre um plano já pronto | **Consome** o `plano.md` como pré-condição |

**Por quê:** manter a skill de implementação focada evita que ela vire uma ferramenta de planejamento disfarçada de ferramenta de execução. Cada skill tem um tipo de rigor diferente — fatiar bem uma task exige pensar em dependências e granularidade; executar uma task exige rastrear estado e não deixar passar desvio de escopo. Misturar as duas responsabilidades numa skill só tende a fazer as duas mal.

Essa decisão também resolve, por tabela, o problema de tasks grandes demais: no `plano.md` atual, as tasks 8.3, 8.6 e 8.8 são grandes (o próprio workflow original já sinalizava isso como risco). A skill de implementação **não** vai tentar dividir essas tasks — isso é trabalho da futura skill `plan`. A skill de implementação só mantém um freio de segurança para quando, mesmo assim, uma task se revelar maior do que o esperado durante a execução (ver seção 5).

---

## 3. Fluxo detalhado de uso da skill

Este é o ciclo de vida completo de **uma task**, do início ao commit. Cada seta representa uma troca de conversa (contexto resetado — ver seção 4.3 sobre por que isso é sistemático).

```
                    ┌─────────────────────────────────────────┐
                    │  Você invoca a skill numa task específica │
                    │  ("implementa a Task 8.3")                │
                    └───────────────────┬───────────────────────┘
                                         ▼
                    ┌────────────────────────────────────────┐
                    │ 1. IMPLEMENTADOR (conversa nova)         │
                    │  - Atualiza registro: "em andamento"     │
                    │  - Verifica gate da etapa (seção 6 plano)│
                    │  - Lê task: Fazer/Não alterar/Entregáveis│
                    │  - Implementa                            │
                    │  - Freio: se sair do Entregáveis ou tocar│
                    │    algo de "Não alterar" → PARA e reporta│
                    │  - Se achar contradição doc↔repo → PARA, │
                    │    manda pra skill plan               │
                    │  - Ao terminar: roda testes, persiste     │
                    │    relatório completo em disco            │
                    └───────────────────┬───────────────────────┘
                                         ▼
                    ┌────────────────────────────────────────┐
                    │ 2. REVISOR (conversa nova, sem herdar    │
                    │    contexto do implementador)            │
                    │  - Atualiza registro: "aguardando revisão"│
                    │  - Lê a TASK + o git diff PRIMEIRO,      │
                    │    forma conclusão própria               │
                    │  - SÓ DEPOIS lê o relatório do            │
                    │    implementador, compara                │
                    │  - Checklist obrigatório: cada item de   │
                    │    "Não alterar" foi respeitado?          │
                    │  - Classifica achados: bloqueador /      │
                    │    importante / melhoria opcional         │
                    │  - Ao terminar: persiste arquivo de       │
                    │    achados completo em disco              │
                    └───────────────────┬───────────────────────┘
                                         ▼
                       zerou bloqueador E importante?
                            │                    │
                           não                   sim
                            ▼                     ▼
        ┌──────────────────────────────┐   ┌─────────────────┐
        │ 3. CORREÇÃO (conversa nova,   │   │      COMMIT      │
        │    cega — recebe task +       │   │  (por task; você │
        │    arquivo de achados)        │   │  cria/troca o    │
        │  - Atualiza registro:         │   │  branch manual-  │
        │    "em correção"              │   │  mente antes)     │
        │  - Corrige                    │   └─────────────────┘
        │  - Volta pro passo 2           │
        │    (SEMPRE reaudita, mesmo     │
        │    achado pequeno)             │
        └───────────────┬────────────────┘
                         │
              3 rodadas de correção
              sem convergir?
                         │
                        sim
                         ▼
        ┌──────────────────────────────────┐
        │ Estoura pra skill plan         │
        │ (sinal de que o problema é a task, │
        │ não a implementação)               │
        └────────────────────────────────────┘
```

**Observações sobre o fluxo:**
- Só **uma task roda por vez** — mesmo que o `plano.md` mencione que a etapa 8.8 (impressão) pode avançar em paralelo com outras, isso é tratado como nota técnica de dependência, não como modo real de operação.
- Todas as trocas de "conversa nova" acima são **manuais** — você mesmo abre a conversa e invoca o papel certo. Não há orquestração automática (subagentes) nessa primeira versão.
- Criação/troca de branch também é manual, feita por você antes de começar — a skill só avisa se perceber que o branch atual não bate com a etapa da task.

---

## 4. Decisões importantes e a justificativa de cada uma

Organizado por tema. Cada linha resume a pergunta, a decisão e o porquê.

### 4.1 Escopo das três skills
| Decisão | Porquê |
|---|---|
| Skill de implementação exige plano já fatiado como pré-condição | Evita que a skill vire ferramenta de planejamento disfarçada |
| Fatiamento de tasks grandes (8.3, 8.6, 8.8) é trabalho da skill `plan`, não da de implementação | Responsabilidade única — quem cria a task garante o tamanho certo |

### 4.2 Ritmo de execução
| Decisão | Porquê |
|---|---|
| Skill invocada task por task, manualmente, sem avanço automático | O ponto central do workflow original é resetar contexto e dar controle humano entre etapas; automação total recriaria o problema que o workflow tenta evitar, especialmente em tasks sensíveis (financeiro, container) |
| Uma task em andamento por vez | Consistente com controle manual; paralelismo do plano é só nota técnica |

### 4.3 Isolamento de contexto (o "porquê" que atravessa quase tudo)
| Decisão | Porquê |
|---|---|
| Correção sempre em conversa nova, cega, nunca reaproveitando a conversa do implementador original | Reaproveitar a conversa reintroduz viés — o agente tende a defender/racionalizar o que já fez, em vez de tratar o achado como requisito novo e neutro |
| Revisor lê a task + o `git diff` cru primeiro, forma conclusão própria, e SÓ DEPOIS lê o relatório do implementador | "Não confiar no relatório" não resiste bem a viés de ancoragem — ler a narrativa do implementador antes tende a fazer o revisor procurar confirmação em vez de procurar problemas do zero. Ler o relatório depois ainda serve: divergências entre "o que ele diz que fez" e "o que ele realmente fez" são, em si, um achado |
| Toda correção gera reauditoria completa, mesmo achados pequenos | Uma correção de bloqueador pode, ela mesma, introduzir um bug novo — e ninguém checa isso se o achado já for marcado como resolvido pelo próprio agente que corrigiu. É o mesmo viés que justificou ter revisor independente, reaparecendo um passo depois |
| Contradição documental nova (não prevista na task) faz o implementador parar e devolver — a resolução (ADR/doc) é encaminhada à skill `docs`, e depois a skill `plan` ajusta o plano; a implementação reabre do zero | Resolver "ali mesmo" seria o implementador fazendo trabalho de design dentro de uma conversa que devia ser só execução, sem o mesmo rigor da skill `docs`, e com incentivo sutil de resolver de um jeito que não invalide o que já foi feito |

### 4.4 Robustez do que conta como "bloqueado"
| Decisão | Porquê |
|---|---|
| Achado "importante" (não só "bloqueador") também impede commit | No domínio do projeto (dinheiro, prazo, diária, container), a diferença entre "bloqueador" e "importante" tende a ser sobre *certeza* do revisor, não sobre gravidade real. Deixar "importante" passar cria incentivo para sub-classificar achados só para não travar o progresso |
| Freio do implementador: qualquer coisa fora do Entregáveis (ou não consequência óbvia deles) → pausa | Critério objetivo e checável, em vez de "perceber" subjetivamente que ficou grande — evita tanto falso negativo (deixar passar) quanto falso positivo por contagem arbitrária de camadas tocadas |
| Itens de "Não alterar": dupla camada — implementador se autopolicia mecanicamente **e** revisor confere item por item no checklist | Autopolicial sozinho tem o mesmo viés de sempre (mesmo agente, mesmo ponto cego); mas exigir do revisor também garante que não fica "por acaso" dependente de ele notar ao ler o diff |
| Limite de 3 rodadas de correção sem convergir → estoura para a skill `plan` | Loop que não converge é sinal de que o problema é a especificação da task, não a implementação — 3 é um número arbitrário usado como circuit breaker |

### 4.5 Rastreamento de estado (por que a skill não pode confiar só no Git)
| Decisão | Porquê |
|---|---|
| Registro central `docs_sistema_recolhe/execucao/registro.md` (tabela task → status → commit → data → observações) | O `plano.md` tem 17 tasks com dependências rígidas e gates acumulativos (seção 6) — só o Git não responde rápido "posso começar a etapa 8?"; teria que reconstruir isso do histórico toda vez |
| Estados intermediários rastreados (implementação em andamento / aguardando revisão / em correção / concluída), atualizados como primeiro passo de cada conversa | Sem isso, "não concluída" na tabela não diferencia entre três situações que pedem ações bem diferentes de você (ninguém começou / está no meio / está esperando decisão sua) |
| Skill verifica mecanicamente o gate da etapa antes de começar | Condição objetiva e checável — o tipo de verificação que a skill deve fazer sozinha, sem custar atenção sua. O risco de não checar é sutil: erro de runtime confuso em vez de aviso claro de dependência |

### 4.6 Persistência de relatórios (não só na conversa, que é descartada)
| Decisão | Porquê |
|---|---|
| Revisor sempre termina a conversa escrevendo o arquivo de achados completo em disco (`docs_sistema_recolhe/execucao/achados/`) — a tabela central só linka pra ele | Uma linha na tabela não cabe "evidência, arquivo, requisito violado, correção recomendada" — e copiar isso manualmente entre conversas é exatamente o tipo de passo frágil que o resto do design já evita |
| Implementador também persiste relatório completo em disco por task **aprovada** (não a cada tentativa) | O Definition of Done do `plano.md` (seção 5) exige que "o próximo desenvolvedor consiga identificar o que foi feito e como validar" — mensagem de commit tende a ficar curta na prática, mesmo pedindo para não ficar |

### 4.7 Git e organização de arquivos
| Decisão | Porquê |
|---|---|
| Commit por task (squash por etapa depois, como limpeza de histórico — não substituto) | Cada task já passou por revisão independente antes do commit; não commitar isso jogaria fora a garantia construída pelo ciclo inteiro. O squash da seção 7 do `plano.md` continua acontecendo, mas como passo de limpeza antes do merge pra `main` |
| Branch criado/trocado manualmente por você; skill só avisa se detectar descompasso | Diferente de gate/Entregáveis/Não alterar (checagens objetivas contra o plano), criar/trocar branch é ação destrutiva no ambiente de trabalho, amarrada a convenções e contexto fora do alcance da skill |
| Artefatos de execução (registro, achados, relatórios) dentro de `docs_sistema_recolhe/execucao/`, não numa pasta separada | Esse conteúdo não é lixo transitório — é rastreabilidade, item do próprio Definition of Done. Manter tudo sob uma raiz de documentação única evita duas respostas diferentes para "onde procuro documentação desse projeto?" |
| Convenção fixa de caminhos (plano, registro, achados sempre no mesmo lugar relativo ao diretório de trabalho), sem parâmetro por invocação | Mantém a invocação simples ("implementa a Task 8.3") sem exigir que você lembre de passar caminho toda vez |

### 4.8 Arquitetura técnica da skill em si
| Decisão | Porquê |
|---|---|
| Conjunto de prompts padronizados (implementador/revisor/corretor) invocados manualmente em conversas novas — sem orquestração automática via subagentes nessa primeira versão | Consistente com a decisão de ritmo manual entre tasks; além disso, subagentes (Task tool) ainda compartilham processo/sessão pai — o isolamento de contexto não é garantidamente tão limpo quanto abrir uma conversa nova de verdade, e isolamento é o ponto central do design inteiro |

---

## 5. O que fica de fora do escopo desta skill

- **Gerar ou fatiar o `plano.md`** — isso é da skill `plan`, desenhada posteriormente a esta conversa.
- **Resolver contradições documentais ou ambiguidades de regra de negócio** — a skill de implementação detecta e para, mas não decide; a decisão é sempre levada para fora do ciclo de implementação.
- **Orquestração automática de múltiplas tasks/subagentes** — deliberadamente fora do escopo da primeira versão; pode ser revisitado depois se o isolamento de contexto via Task tool se mostrar confiável o suficiente.
- **Criação/gestão de branches** — fica com você, fora da skill.

---

## 6. Artefatos que a skill vai gerar/consumir em disco

```
docs_sistema_recolhe/
├── plano.md                          (consumido — não é gerado pela skill)
└── execucao/
    ├── registro.md                   (tabela central de status por task)
    └── achados/
        ├── task-8.3-revisao-1.md     (revisor)
        ├── task-8.3-revisao-2.md     (revisor, se houve correção)
        └── task-8.3-relatorio.md     (implementador, ao ser aprovada)
```

---

## 7. Estado da decisão

Todos os ramos levantados durante a entrevista foram fechados com concordância explícita. Não há pontos em aberto pendentes de decisão — o próximo passo natural é escrever a skill propriamente dita (ex: com a `skill-creator`), usando este relatório e o arquivo de memória do projeto (`areas/skill-implementacao.md`) como especificação.

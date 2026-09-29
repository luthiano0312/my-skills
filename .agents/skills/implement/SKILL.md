---
name: implement
description: Executa o ciclo implementador→revisor→correção→commit para uma task de um plano.md já fatiado (formato Fazer/Não alterar/Entregáveis/Critério de conclusão, com gates acumulativos). Use sempre que o usuário pedir para "implementar a Task X", "auditar/revisar a implementação da Task X", "corrigir os achados da Task X", ou mencionar tocar em qualquer task de um plano de desenvolvimento existente — mesmo que ele não use a palavra "skill". NÃO use esta skill para criar ou fatiar um plano do zero (isso é trabalho de uma skill de planejamento separada, ainda não fornecida aqui) — se não existir um plano.md com o formato esperado, avise e pare antes de implementar qualquer coisa.
---

# Implementação orientada por plano (ciclo implementador → revisor → correção → commit)

## Por que essa skill existe

Implementação feita por um agente de código, numa conversa só, do início ao commit, tem um problema estrutural: o mesmo agente que escreveu o código tende a acreditar no próprio trabalho quando "revisa" o que fez. Essa skill resolve isso trocando de **papel** a cada etapa crítica — implementador, revisor, corretor — cada um numa conversa nova, sem herdar o contexto/viés do anterior. A continuidade entre essas conversas não fica na memória de nenhuma delas: fica registrada em disco (Git + um registro de execução), que é o que permite que cada conversa comece "cega" e ainda assim saiba onde o trabalho parou.

Cada task é tratada como uma unidade fechada: implementação → revisão → (correção → reauditoria)\* → commit. Nunca se avança para a próxima task sem esse ciclo fechado, e nunca se avança automaticamente para a próxima task sem você invocar de novo.

## Pré-condição: o plano

Esta skill **consome** um `plano.md` já pronto — ela não cria nem fatia tasks. Antes de fazer qualquer coisa, confirme que o plano existe e que a task pedida tem, no mínimo:

- **Fazer** — o que a task exige
- **Não alterar** — o que está explicitamente fora dos limites
- **Entregáveis** — lista concreta do que deve existir ao final
- **Critério de conclusão** — como saber que terminou

Se a task não tiver esses campos, ou parecer grande demais para uma conversa (mexe em várias camadas — migration + model + controller + frontend + testes de múltiplos fluxos — ou tem entregáveis heterogêneos demais), **pare e diga isso ao usuário** em vez de tentar implementar ou de subdividir você mesmo. Subdividir tasks é trabalho de uma skill de planejamento separada, não desta.

Se o `plano.md` também define **gates acumulativos** por etapa (ex: "etapa 8 só começa se as etapas 5, 6 e 7 estiverem concluídas"), essa skill verifica esses gates mecanicamente antes de começar qualquer task — ver passo 0 abaixo.

## Convenção fixa de arquivos

Esta skill sempre procura e escreve nos mesmos caminhos, relativos à raiz do repositório onde você está trabalhando — sem pedir nem aceitar caminho customizado:

```
docs_sistema_recolhe/          (ou o nome real da pasta de documentação do projeto —
│                                pergunte se não existir "docs_sistema_recolhe/")
├── plano.md                   (consumido, nunca gerado por esta skill)
└── execucao/
    ├── registro.md            (tabela central: task → status → commit → data → observações)
    └── achados/
        ├── task-<N>-revisao-<R>.md    (escrito pelo revisor a cada rodada)
        └── task-<N>-relatorio.md      (escrito pelo implementador quando a task é aprovada)
```

Se `docs_sistema_recolhe/execucao/registro.md` ainda não existir na primeira invocação, crie-o vazio com apenas o cabeçalho da tabela (ver `assets/registro-template.md`).

## Os três papéis

Você (o usuário) invoca esta skill dizendo qual papel quer rodar, numa conversa nova a cada troca de papel — isso é deliberado, não é conveniência: **não** avance sozinho de um papel para o outro dentro da mesma conversa, e **não** use subagentes para simular isso. O isolamento de contexto entre papéis é o mecanismo central que sustenta o resto do design.

| Quando o usuário pede | Papel a seguir | Instruções completas |
|---|---|---|
| "implementa a Task X", "continua a Task X" | **Implementador** | `references/implementador.md` |
| "revisa/audita a Task X", "faz o code review da Task X" | **Revisor** | `references/revisor.md` |
| "corrige os achados da Task X", "aplica as correções" | **Corretor** | `references/corretor.md` |

Leia o arquivo de referência correspondente **antes** de agir — cada um tem o passo a passo completo, incluindo o que escrever em disco ao final. Não improvise um resumo do papel a partir desta tabela.

## Passo 0 — sempre, antes de qualquer papel

Isso vale para os três papéis, como primeiro passo de qualquer conversa nova aberta com esta skill:

1. Leia `docs_sistema_recolhe/execucao/registro.md` para saber o estado atual da task (se a linha dela não existir ainda, ela nunca foi iniciada).
2. Atualize a linha de status da task para refletir o papel que está começando agora (`implementação em andamento`, `aguardando revisão`, `em correção`) — **antes** de fazer qualquer trabalho, não só no final. Use `scripts/update_registro.py` para isso em vez de editar a tabela manualmente (evita quebrar a formatação markdown).
3. Se você é o **implementador** e é a primeira vez que essa task é aberta (sem linha de correção anterior), verifique o gate de etapa no `plano.md`: todas as tasks das etapas anteriores exigidas já estão `concluída` no registro? Se não, pare e explique o que falta — não implemente mesmo assim.
4. Confirme que está numa branch coerente com a etapa da task (ex: task da etapa 8 deveria estar numa branch tipo `feat/etapa-8`). Se a branch atual parecer de outra etapa, **avise o usuário e pergunte antes de continuar** — não troque de branch sozinho, isso é decisão do usuário.

## Visão geral do ciclo (para orientação, não para pular os arquivos de referência)

```
Implementador (conversa nova)
  → implementa, roda testes, persiste relatório em disco (só se aprovado depois)
  → freio: qualquer coisa fora dos Entregáveis, ou que toque algo de "Não alterar",
    ou contradição documento↔repositório → PARA e reporta, não decide sozinho
        ↓
Revisor (conversa nova, sem herdar o contexto do implementador)
  → lê a task + o git diff PRIMEIRO, forma opinião própria
  → só depois lê o relatório do implementador, compara
  → checklist obrigatório item a item contra "Não alterar"
  → classifica achados: bloqueador / importante / melhoria opcional
  → persiste o relatório de achados completo em disco
        ↓
   zerou bloqueador E importante? ──não──→ Corretor (conversa nova, cega,
        │                                    recebe task + arquivo de achados)
       sim                                          ↓
        ↓                                  corrige → volta pro Revisor
   Revisor faz o commit                     (SEMPRE reaudita, mesmo achado pequeno)
   (por task; squash por etapa
   fica pra depois, como limpeza
   de histórico, não substitui isso)
```

Se o ciclo revisão→correção passar de **3 rodadas** sem zerar bloqueadores, pare: isso é sinal de que o problema é a especificação da task, não a implementação. Reporte ao usuário e recomende levar a task de volta para a skill de planejamento, em vez de insistir numa quarta correção.

## Referências

- `references/implementador.md` — passo a passo completo do papel de implementador, incluindo os freios de escopo e o formato do relatório final
- `references/revisor.md` — passo a passo completo do papel de revisor, incluindo a ordem obrigatória de leitura (diff antes do relatório) e o formato do arquivo de achados
- `references/corretor.md` — passo a passo completo do papel de corretor, incluindo a contagem de rodadas e quando escalar
- `assets/registro-template.md` — cabeçalho vazio para criar `registro.md` na primeira vez
- `scripts/update_registro.py` — atualiza (ou cria) a linha de uma task na tabela do registro sem quebrar a formatação

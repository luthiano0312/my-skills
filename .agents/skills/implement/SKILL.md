---
name: implement
description: Executa o ciclo implementador→revisor→correção→commit para uma task de um plano.md aprovado (Fazer/Não alterar/Entregáveis/Critério de conclusão) e um registro de execução inicializado. Use quando o usuário pedir para implementar uma task planejada, revisar sua implementação ou corrigir achados, mesmo sem mencionar a skill. Para criar, dividir ou reordenar tasks, use a skill plan; não implemente sem plano e registro válidos.
---

# Implementação orientada por plano (ciclo implementador → revisor → correção → commit)

## Por que essa skill existe

Implementação feita por um agente de código, numa conversa só, do início ao commit, tem um problema estrutural: o mesmo agente que escreveu o código tende a acreditar no próprio trabalho quando "revisa" o que fez. Essa skill resolve isso trocando de **papel** a cada etapa crítica — implementador, revisor, corretor — cada um numa conversa nova, sem herdar o contexto/viés do anterior. A continuidade entre essas conversas não fica na memória de nenhuma delas: fica registrada em disco (Git + um registro de execução), que é o que permite que cada conversa comece "cega" e ainda assim saiba onde o trabalho parou.

Cada task é tratada como uma unidade fechada: implementação → revisão → (correção → reauditoria)* → commit funcional → commit de metadados do registro. Nunca se avança para a próxima task antes dos **dois commits** e nunca se avança automaticamente sem você invocar de novo. A autorização explícita do usuário deve cobrir ambos os commits; aprovação técnica sozinha não autoriza nenhum.

## Pré-condição: o plano

Esta skill **consome** um `plano.md` já pronto — ela não cria nem fatia tasks. Antes de fazer qualquer coisa, confirme que o plano existe e que a task pedida tem, no mínimo:

- **Fazer** — o que a task exige
- **Não alterar** — o que está explicitamente fora dos limites
- **Entregáveis** — lista concreta do que deve existir ao final
- **Critério de conclusão** — como saber que terminou

Se faltar algum campo ou a task reunir entregas independentes com critérios próprios, **pare e encaminhe à skill `plan`** em vez de subdividir durante a execução. Uma entrega fim a fim pode tocar backend, frontend e testes; número de camadas, por si só, não é motivo para recusá-la. Verifique as dependências obrigatórias declaradas no plano antes de começar uma task, haja ou não etapas. Não exija gates acumulativos que o plano não prevê.

## Onde estão os arquivos

Leia o mapa de caminhos no `AGENTS.md` ou `CLAUDE.md` **do projeto em execução**, não o desta skill. Use os caminhos exatos, relativos à raiz do repositório, para o plano atual e o registro. Caminhos apenas *previstos* no template `docs` não significam que os arquivos existam. Se ambos os arquivos de entrada existirem e divergirem, ou faltarem caminhos, peça esclarecimento; não adivinhe uma pasta padrão. A pasta `achados/` fica ao lado de `registro.md`:

```text
<área escolhida>/plano.md                 (consumido, nunca gerado aqui)
<local do registro>/registro.md           (criado pela skill plan após aprovação)
<local do registro>/achados/
    task-<ID>-revisao-<R>.md               (revisor)
    task-<ID>-relatorio.md                 (relatório da task)
```

No Recolhe, esses caminhos são `docs_sistema_recolhe/plano.md` e `docs_sistema_recolhe/execucao/registro.md`; num projeto novo com a estrutura padrão, `docs/03-execucao/plano.md` e `docs/03-execucao/registro.md`. **Não crie um registro ausente**: a skill `plan` o inicializa ao aprovar o marco. Confira as seis colunas `Task | Marco | Status | Commit | Atualizado em | Observações` e a linha da task antes de agir. Se registro e plano não concordarem, pare e encaminhe a divergência à `plan`. Atualize o registro com `scripts/update_registro.py`; não altere a tabela à mão. A coluna `Atualizado em` é o instante da última mudança de status em ISO 8601 com fuso explícito, não a data do commit. Antes da **primeira invocação de uma task `não iniciada`**, verifique no Git que o plano aprovado, o registro e o arquivo de entrada que contém o mapa estão rastreados, já commitados e sem mudanças pendentes nesses caminhos (`git ls-files`, `git status --short -- <caminhos>`). Sem esse baseline, peça ao usuário para autorizar/versionar os três arquivos **antes** de implementar. Faça a mesma checagem ao iniciar novas tasks após replanejamento. Não exija registro limpo durante a implementação, revisão ou correção da task em curso: seus estados intermediários ainda aguardam o commit de metadados.

## Os três papéis

Você (o usuário) invoca esta skill dizendo qual papel quer rodar, numa conversa nova a cada troca de papel — isso é deliberado, não é conveniência: **não** avance sozinho de um papel para o outro dentro da mesma conversa, e **não** use subagentes para simular isso. O isolamento de contexto entre papéis é o mecanismo central que sustenta o resto do design.

| Quando o usuário pede | Papel a seguir | Instruções completas |
|---|---|---|
| "implementa a Task X", "continua a Task X" | **Implementador** | `references/implementador.md` |
| "revisa/audita a Task X", "faz o code review da Task X" | **Revisor** | `references/revisor.md` |
| "corrige os achados da Task X", "aplica as correções" | **Corretor** | `references/corretor.md` |
| "o código já foi commitado; falta registrar a conclusão da Task X" | **Recuperação de metadados** | seção "Recuperação" de `references/revisor.md` |

Leia o arquivo de referência correspondente **antes** de agir — cada um tem o passo a passo completo, incluindo o que escrever em disco ao final. Não improvise um resumo do papel a partir desta tabela.

## Passo 0 — sempre, antes de qualquer papel

1. Resolva plano e registro pelo arquivo de entrada do projeto. Leia a task e a linha correspondente no registro; confirme que o ID não é `concluída`/`substituída` e que seu estado permite o papel pedido (`não iniciada`/`em andamento` → implementador, início ou continuação; `aguardando revisão` → revisor; `em correção` → corretor). Se estiver `pausada`, peça ao usuário a resolução do bloqueio antes de retomar. Não crie linha para task desconhecida. **Exceção:** no pedido explícito de recuperar um commit de registro pendente, `concluída` localmente não basta para declarar a task finalizada; siga a seção de recuperação do revisor e verifique o Git.
2. Antes de iniciar uma task `não iniciada`, confirme o commit de baseline descrito acima. Para começar uma task, confirme no registro que **todas as dependências obrigatórias identificadas no plano** estão `concluída` **e que seus commits de metadados já estão no Git**; se alguma estiver ausente, pendente ou substituída sem vínculo resolvido, pare e explique. Etapas são opcionais, não são prova de dependência por si mesmas.
3. Confira a branch contra as convenções reais do projeto, sem presumir branch por etapa. Se houver descompasso, pergunte antes de continuar; não troque de branch sozinho.
4. Só depois de todas as verificações o implementador muda `não iniciada` para `em andamento` via `scripts/update_registro.py` (ou mantém `em andamento` se já estava em execução). O corretor mantém `em correção` até devolver para `aguardando revisão`; o revisor mantém `aguardando revisão` até publicar o resultado. Ao bloquear uma task por contradição, marque `pausada` com motivo. Não altere o estado antes de validar o gate.

## Visão geral do ciclo (para orientação, não para pular os arquivos de referência)

```
Implementador (conversa nova)
  → implementa, roda testes, persiste relatório em disco antes da revisão
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
        ↓                                  corrige, registra a rodada no relatório → volta pro Revisor
   Revisor informa aprovação                 (SEMPRE reaudita, mesmo achado pequeno)
   → após autorização explícita do usuário:
     1. commit funcional (código + relatórios/achados)
     2. commit só de registro (status + hash do 1º)
   → squash, se adotado, é posterior
```

Antes de qualquer commit, siga a regra do arquivo de entrada do projeto: aprovação técnica da revisão não é autorização. O revisor só inicia **os dois commits** após pedido explícito que os inclua (ex.: "revise e, se passar, faça os commits da task e do registro"). Pedido de "commit" ambíguo não autoriza o segundo: confirme o alcance. Sem autorização, informe que a revisão passou e aguarde. O campo `Commit` guarda o hash do **primeiro commit**, não do commit de metadados. Atualize para `concluída` após o primeiro commit, mas só declare a task concluída e libere a próxima quando o commit de metadados tiver sido confirmado. Se o segundo falhar, não refaça o primeiro: preserve o hash e oriente recuperação do registro pendente.

Depois de **3 correções completas**, se a reauditoria seguinte ainda encontrar bloqueadores ou importantes, pause a task e encaminhe à `plan`; não abra uma quarta correção. São até 3 correções e até 4 revisões (a inicial mais uma após cada correção). Isso pode indicar problema na especificação, sem provar que todo achado veio dela. Reporte ao usuário e recomende levar a task de volta para a skill de planejamento, em vez de insistir numa quarta correção.

## Referências

- `references/implementador.md` — passo a passo completo do papel de implementador, incluindo os freios de escopo e o formato do relatório final
- `references/revisor.md` — passo a passo completo do papel de revisor, incluindo a ordem obrigatória de leitura (diff antes do relatório) e o formato do arquivo de achados
- `references/corretor.md` — passo a passo completo do papel de corretor, incluindo a contagem de rodadas e quando escalar
- `assets/registro-template.md` — contrato do registro criado pela skill `plan`; não o crie nesta skill
- `scripts/update_registro.py` — valida o formato e as transições e atualiza uma linha já criada pela `plan`; nunca cria o registro nem novas tasks

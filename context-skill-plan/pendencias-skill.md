# Pendências de integração: docs, plan e implement

**Estado:** as decisões de P1–P4 foram aprovadas nesta retomada e aplicadas às skills/scripts do laboratório. Os testes locais estão registrados na seção 7; **ainda não houve validação do fluxo completo com agentes em conversas independentes**. O diagnóstico anterior e as alternativas discutidas foram preservados como histórico, não como requisitos adicionais.

## Como retomar

Leia primeiro o contexto e as decisões já fechadas; depois confira os arquivos indicados em cada pendência. As decisões abaixo já estão fechadas: retome as verificações ainda pendentes, não a escolha entre alternativas históricas. Não reabra decisões fechadas sem encontrar um conflito concreto. Não implemente todas as alternativas como se fossem requisitos.

O pedido anterior foi **registrar as pendências**. Nesta retomada, o usuário aprovou o desenho e autorizou as alterações locais e testes, **sem commits no laboratório e sem modificar `AGENTS-recolhe.md`**. As operações Git da fixture de squash ocorreram somente em repositórios temporários. Não execute commits, push, merge, squash, troca de branch ou migração do projeto Recolhe sem pedido explícito. Confira `git status` e os diffs antes de editar: o estado do repositório pode ter mudado entre conversas.

## 1. Contexto e divisão de responsabilidades

Este repositório é um laboratório de skills. O conjunto em discussão é:

| Skill | Responsabilidade | Fonte principal |
|---|---|---|
| `docs` | Requisitos, análise, design, ADRs e arquivo de entrada do projeto | [.agents/skills/docs/SKILL.md](.agents/skills/docs/SKILL.md) |
| `plan` | Planejar/refatiar **um marco de implementação por vez**, gerar plano aprovado e inicializar o registro | [.agents/skills/plan/SKILL.md](.agents/skills/plan/SKILL.md) |
| `implement` | Executar uma task: implementação → revisão independente → correções → dois commits autorizados | [.agents/skills/implement/SKILL.md](.agents/skills/implement/SKILL.md) |

A skill de planejamento se chama **`plan`**, não `plano`; a de implementação se chama **`implement`**, não `implementacao`. O documento consumido continua se chamando `plano.md`.

O Recolhe serviu de exemplo real. [AGENTS-recolhe.md](AGENTS-recolhe.md) é uma **cópia de contexto**, não o arquivo de instruções ativo do laboratório, nem comprovação do estado atual do repositório real do Recolhe. Ele ainda descreve convenções anteriores e não foi migrado nesta discussão. Os arquivos completos de requisitos/convenções do Recolhe citados nele não foram disponibilizados aqui; não invente seu conteúdo.

## 2. Decisões já fechadas — preservar

### Planejamento e limites

- `plan` confirma **antes de começar a analisar** o projeto, inclusive se chamada por comando. A invocação pode vir sem parâmetros. Depois propõe o recorte do marco e pede validação; antes de salvar plano/registro/mapa, pede aprovação explícita do conteúdo. Autorizar análise não autoriza gravação.
- Tasks têm uma entrega coerente, verificável e revisável independentemente. Funcionalidades podem ser fim a fim (backend + interface + testes); infraestrutura pode ser uma entrega técnica testável. Número de camadas não é, sozinho, motivo para dividir.
- A ordem física das tasks é a sequência prática sugerida. Dependências obrigatórias ficam explícitas e justificadas, sem transformar a ordem do arquivo numa cadeia artificial. Etapas são opcionais. A execução é sequencial, uma task por vez, sem orquestração automática de papéis/subagentes.
- Cada task contém `Fazer`, `Não alterar`, `Entregáveis` e `Critério de conclusão`. Todo `Não alterar` final é obrigatório: `[Fonte: caminho#trecho]` ou `[Decisão deste marco]` aprovada. `[Proposta sem fonte]` só pode aparecer no rascunho.
- Resultado esperado é derivado das tasks, sem prometer homologação/deploy que seus critérios não comprovem. Convenções, stack e regras globais são referenciadas, não copiadas para cada plano.
- Contradição entre requisitos/design vai primeiro à `docs`; depois a `plan` ajusta o marco em curso. Reespecificação por não convergência usa task, registro e achados persistidos, **não uma nova investigação do diff/código pela plan**.

### Caminhos e arquivo de entrada

`AGENTS.md` é o padrão **para projetos novos**. `CLAUDE.md` é alternativa explícita. A `docs` preserva um arquivo de entrada existente, sem criar automaticamente duas cópias divergentes. O template atual é `.agents/skills/docs/assets/templates/agent-entrypoint.md`, renderizado por `scripts/scaffold_docs.sh`.

O arquivo de entrada **do projeto em execução** aponta para plano e registro por caminhos exatos, relativos à raiz do repositório. A `docs` indica caminhos **previstos**, sem criar plano/registro vazios. Depois da aprovação, a `plan` confirma ou atualiza esse mapa. A `implement` lê o mapa e valida os arquivos; não adivinha caminhos nem cria um segundo registro.

```text
Recolhe (preservar estrutura existente):
docs_sistema_recolhe/plano.md
docs_sistema_recolhe/planos/marco-<id>.md
docs_sistema_recolhe/execucao/registro.md
docs_sistema_recolhe/execucao/achados/

Projeto novo sem convenção anterior:
docs/03-execucao/plano.md
docs/03-execucao/planos/marco-<id>.md
docs/03-execucao/registro.md
docs/03-execucao/achados/
```

O plano atual fica na raiz da área escolhida, não necessariamente na raiz de `docs/`. Marcos encerrados são arquivados sem apagar o histórico; planos anteriores são consultados seletivamente no planejamento/investigação, não carregados por padrão pela implementação.

### Contrato do registro

A `plan` cria as linhas das tasks **na mesma conversa em que salva o plano aprovado**. A `implement` não cria arquivo/linha ausente; seu script só atualiza um registro existente e valida o formato e as transições.

```md
| Task | Marco | Status | Commit | Atualizado em | Observações |
|---|---|---|---|---|---|
| M01-T01 | M01 | não iniciada | - | 2026-09-30T14:20:00-03:00 | - |
```

- IDs são únicos **entre todos os marcos do projeto**, estáveis após aprovação/uso; não renumere silenciosamente tasks com achados ou histórico. `M01-T01` e `M02-T01` são exemplos do padrão, não IDs existentes no Recolhe.
- `Atualizado em` registra a **última mudança de status**, em ISO 8601 com fuso explícito. Não é data do commit nem histórico de todas as transições. Atualizar só observações não altera esse instante.
- Estados: `não iniciada`, `em andamento`, `aguardando revisão`, `em correção`, `pausada`, `concluída`, `substituída`. Pausa exige motivo; substituição mantém a linha antiga e os vínculos com as novas tasks. Estados finais não são reabertos silenciosamente.
- Use `-` para commit/observações ausentes. Não coloque quebras de linha nem `|` literal dentro de uma observação. O registro contém progresso e links, não cópia dos requisitos/entregáveis.

### Revisão, persistência e Git

- Implementador, revisor e corretor trabalham em **conversas novas** a cada troca de papel. O handoff é em disco, não por recuperação da conversa anterior.
- O implementador grava `achados/task-<ID>-relatorio.md` **antes** de entregar para revisão. O corretor acrescenta seções por rodada, sem apagar o relato anterior. Na mesma conversa, o revisor usa `scripts/review_inputs.py`, persiste a **Avaliação independente** e só então lê relatos/achados e preenche a **Decisão final**. `Estado: incompleta` não libera correção/commit nem consome outra rodada; `Estado: finalizada` identifica o handoff publicado. O filtro não substitui o cumprimento dessa sequência pelo agente.
- Bloqueador **e importante** impedem commit. Melhoria opcional não impede. Toda correção exige reauditoria completa.
- Limite já aprovado: até **3 correções e 4 revisões** (uma inicial + uma após cada correção). A revisão 4 ainda com achado obrigatório pausa a task e devolve à `plan`. Não é prova automática de que o problema veio da especificação. Reinício por reespecificação substancial aprovada recebe novo ID: a antiga fica substituída, sem reset cosmético de contagem. Código reaproveitado é explicitado e revisado integralmente, não descartado nem aprovado automaticamente.
- Revisão aprovada não autoriza commit. O usuário deve autorizar explicitamente **dois commits**: primeiro código + relatórios/achados; depois apenas `registro.md`, com status `concluída` e hash do primeiro. A task só libera a próxima após os dois commits. Se o segundo falhar, recupere apenas os metadados; não repita o primeiro.
- `Commit` guarda o hash do commit **funcional**, nunca o hash do commit que contém o próprio registro. Após squash/reescrita, ele permanece histórico, sem garantia de disponibilidade. A garantia escolhida é localizar a entrega integrada, mesmo com várias tasks, por `Integração: <hash-completo>` em Observações. O vínculo exige conferência Git, autorização e commit documental posterior, sem mudar status, hash original ou timestamp.
- Antes da primeira task, é obrigatório um **commit de baseline** com plano aprovado, registro inicial e mapa no arquivo de entrada. A `plan` não o faz automaticamente. Antes de iniciar nova task, a `implement` verifica que esses arquivos estão versionados e sem mudanças pendentes. Isso não exige registro limpo durante revisão/correção da task atual. Replanejamento também deve ser versionado antes de novas tasks.
- Preserve alterações preexistentes do usuário. Se não conseguir separá-las das mudanças da task, pare. Não use `git add .` indiscriminadamente nem faça gestão automática de branches.

## 3. P1 — Relatórios vazam para a primeira inspeção do revisor

**Estado:** desenho aprovado e implementado; filtro coberto por testes locais. O comportamento de agentes ainda precisa ser observado no fluxo real.

**Diagnóstico anterior.** Antes destas alterações, `.agents/skills/implement/references/revisor.md`, seção **Ordem obrigatória de leitura** (linhas 12–14 na revisão deste handoff), manda ler `git diff HEAD` e examinar os arquivos novos listados por `git ls-files --others --exclude-standard`. Só no passo seguinte manda ler o relatório do implementador. Entretanto, o relatório inicial já existe antes da auditoria e pode ser um desses arquivos novos; em reauditorias, suas seções podem estar no diff rastreado. Achados anteriores também podem aparecer. Assim, a narrativa entra no contexto antes da conclusão independente, mesmo obedecendo literalmente ao procedimento.

**O que precisa ser decidido.** Como separar a primeira inspeção de código/testes/artefatos entregues dos arquivos narrativos de execução, sem ocultar código novo ou documentação que seja um entregável real da task. Definir quando relatórios/achados são lidos e como reconciliar isso com a revisão posterior de tudo que vai ao commit. Os metadados mínimos de ID/status já necessários ao Passo 0 não devem virar desculpa para carregar relatos inteiros antecipadamente.

**Decisão aprovada e aplicada.** Duas fases na mesma conversa do revisor: `review_inputs.py` produz metadados mínimos, inventário, diffs filtrados (HEAD/staged/unstaged), arquivos novos permitidos e snapshot. O conteúdo de relatos, achados e Observações não é emitido. O revisor persiste a Avaliação independente no próprio arquivo de revisão antes de ler as narrativas; preserva essa seção e acrescenta confronto/decisão final. Relatos/achados são inspecionados antes dos commits autorizados. Não excluir `docs/` inteira; ambiguidades de caminhos/classificação interrompem a preparação. Revisão incompleta não libera o próximo papel nem conta como rodada concluída. Snapshot detecta mudanças posteriores na entrega, inclusive conteúdo de arquivos novos.

**Fontes e arquivos afetados.**

- `.agents/skills/implement/references/revisor.md`: **Ordem obrigatória de leitura**, **Ao terminar**, **Se esta é uma reauditoria**.
- `.agents/skills/implement/references/implementador.md`: **Ao terminar**, gravação antecipada do relatório.
- `.agents/skills/implement/references/corretor.md`: **Ao terminar**, append das correções.
- `.agents/skills/implement/SKILL.md`: **Onde estão os arquivos**, **Passo 0** e diagrama do ciclo.

**Critérios para considerar resolvido.** O revisor continua vendo código/testes novos, staged e unstaged, mas não recebe a narrativa antes de registrar sua conclusão independente. Reauditoria não é ancorada automaticamente em achados anteriores. Os relatórios/achados são lidos e validados antes do commit autorizado. A regra funciona nos dois layouts de documentação.

**Verificação sugerida.** Projeto temporário com relatório novo não rastreado e, numa segunda rodada, relatório modificado/rastreado; conferir a sequência de leituras/saídas do agente. Teste de comando isolado ajuda a validar o filtro, mas não comprova sozinho o comportamento do agente.

## 4. P2 — Novo ciclo após replanejamento com o mesmo ID

**Estado:** desenho aprovado e aplicado às instruções; fixtures verificam preservação do ID antigo e seleção de revisões próprias do novo ID. Replanejamento por agente ainda não foi avaliado.

**Diagnóstico anterior.** Antes destas alterações, `plan/SKILL.md`, seção **Replanejar um marco em andamento**, permite dividir/redefinir uma task in place, preservando histórico e IDs quando possível. `revisor.md`, **Ao terminar**, incrementa o número de revisão por task; `corretor.md`, **Antes de tocar em qualquer arquivo**, considera o R mais alto e o limite de revisão 4. Se `M01-T03` tem revisões 1–4 e a `plan` reespecifica a mesma task sem mudar seu ID, o próximo ciclo não tem uma identidade própria. Não está definido se revisão 5 pode começar ou como o corretor reconhece um novo limite. Apagar/renomear as revisões antigas para recomeçar em 1 violaria a preservação de evidências.

**O que precisa ser decidido.** Um novo plano para a mesma task é uma nova identidade de task ou um novo ciclo de execução dentro do mesmo ID? Quem autoriza esse reinício, onde ele é registrado e como ocorre a retomada a partir de `pausada`? Definir ainda como relacionar o código não commitado e o relatório já existentes ao trabalho reespecificado, sem rollback automático nem revisão implícita.

**Alternativas.**

1. **Novo ID quando houver reespecificação que reinicie o ciclo:** a antiga fica `substituída`, com link para a nova; a nova nasce `não iniciada`, recebe relatório próprio e revisões a partir de 1. Simplifica a contagem e usa o mecanismo de substituição já aprovado, mas exige reconciliar dependências e identificar o que foi reaproveitado.
2. **Mesmo ID + identificador explícito de ciclo:** manter identidade da task, mas usar ciclo em arquivos/metadados (ex.: `task-M01-T03-ciclo-2-revisao-1.md`). Exige definir nomes, seleção da revisão corrente, links e persistência do ciclo. Não acrescentar uma sétima coluna ao registro sem discutir a mudança do contrato.

**Decisão aprovada e aplicada.** Novo ID livre para reinício por reespecificação substancial aprovada e versionada; a antiga fica `substituída`, com vínculos e evidências preservados. Reconcile dependências e explicite origem/reaproveitamento. O novo implementador revalida o código existente e o revisor audita a entrega inteira; não há rollback, descarte ou aprovação herdada. Mudança cosmética não reseta a contagem, e pausa por acesso/bloqueio externo pode retomar o mesmo ID sem zerá-la. Não foi adotado identificador de ciclo nem sétima coluna. Evidências anteriores ainda não versionadas entram no baseline documental do replanejamento, separadas do código pendente.

**Fontes e arquivos afetados.**

- `.agents/skills/plan/SKILL.md`: IDs estáveis; **Caminhos e ciclo de vida dos arquivos**; **Replanejar um marco em andamento**.
- `.agents/skills/implement/SKILL.md`: **Passo 0** (retomada de pausadas), contagem e encaminhamento à `plan`.
- `.agents/skills/implement/references/revisor.md`: nome/numeração de achados e bloqueio após terceira correção.
- `.agents/skills/implement/references/corretor.md`: escolha do arquivo mais recente e contagem.
- `.agents/skills/implement/references/implementador.md`: histórico anterior e relatório inicial.
- `.agents/skills/implement/scripts/update_registro.py`: estados `pausada`/`substituída`; não cria novas linhas nem reabre estados finais. A `plan` deve inicializar a nova task.

**Critérios para considerar resolvido.** Após três correções falhas, a task para. Depois de replanejamento explicitamente aprovado e versionado, a execução pode reiniciar com identidade inequívoca, sem perder relatórios/achados antigos, sobrescrever IDs, reaproveitar aprovação antiga ou criar loop ilimitado de resets silenciosos. Dependências e registro continuam alinhados.

**Verificação sugerida.** Fixture com revisões 1–4, registro `pausada`, replanejamento aprovado e reinício. Conferir que o corretor só lê os achados do ciclo correto e que evidências anteriores continuam acessíveis.

## 5. P3 — Hash de commit funcional após squash/reescrita de histórico

**Estado:** política aprovada e implementada; fixture de squash/clone novo passou sem os commits individuais originais. A convenção real do Recolhe não foi alterada.

**Diagnóstico anterior.** O registro guarda o hash do primeiro commit da task e é versionado no segundo. `implement/SKILL.md` e `revisor.md` ainda permitem squash posterior. `AGENTS-recolhe.md`, **Convenções** (linha 19 na revisão deste handoff), diz que branches entram na `main` por squash. Um squash produz um commit diferente, que não torna os commits individuais ancestrais da `main`.

**Precisão técnica.** O squash não apaga instantaneamente os objetos antigos. Eles podem continuar acessíveis enquanto houver branch/tag/reflog ou retenção no provedor. Mas o texto de um hash dentro de `registro.md` **não é uma referência Git que mantenha o objeto vivo**. Depois de remover a branch e expirar reflogs/retenção, esses objetos podem ser coletados; um clone novo da `main` pode não trazer os commits individuais. Isso afeta consultas de histórico e checagens futuras do gate por hashes/commits.

**O que precisa ser decidido.** O campo `Commit` identifica permanentemente o commit individual auditado ou o commit que integrou a task na `main`? É obrigatório preservar o primeiro objeto para consultar o diff exato revisado? Quem realiza e autoriza o merge/squash e eventual atualização de rastreabilidade? Não confundir a existência local de um objeto hoje com persistência garantida a longo prazo.

**Alternativas.**

1. **Preservar os commits individuais no histórico integrado**, com merge/fast-forward sem squash ou reescrita dos commits auditados. Mais simples para rastrear pelo hash; muda a convenção atual do exemplo Recolhe.
2. **Manter squash e preservar referências duráveis** para o histórico auditado, por exemplo tags de auditoria publicadas/retenção de refs definida. Permite consultar os hashes originais, mas exige política de criação, publicação e retenção; não usar só reflog local como arquivo histórico.
3. **Manter squash e registrar um vínculo ao commit de integração**, separando a identidade original auditada do hash integrado. Uma mesma integração pode cobrir várias tasks. Definir onde vivem os dois vínculos e como ficam as checagens; não sobrescrever o original como se fosse o mesmo commit. Consultar só pelo ID na mensagem não garante recuperar o diff individual auditado.

**Decisão aprovada e aplicada.** O usuário não exige consulta permanente do commit individual auditado. Squash continua permitido; `Commit` preserva o hash original como histórico e Observações recebe `Integração: <hash-completo>`, via operação restrita `--integration`, após conferência do Git e autorização explícita. Um commit documental posterior pode atualizar várias tasks, sem reabrir status nem mudar hash original/timestamp. Os gates anteriores à integração verificam os dois commits; depois de reescrita verificam vínculo, conclusão e evidências versionadas na entrega integrada. Vínculo pendente exige recuperação, não repetição do squash. O script valida sintaxe, não existência/conteúdo/ancestralidade do commit: essa verificação permanece responsabilidade do agente/operador. Não foram adotadas tags de auditoria nem obrigação de preservar os objetos originais.

**Fontes e arquivos afetados.**

- `AGENTS-recolhe.md`: **Convenções**; dado de contexto, não arquivo a modificar automaticamente.
- `.agents/skills/implement/SKILL.md`: dois commits, liberação da próxima task e checagem dos commits das dependências.
- `.agents/skills/implement/references/revisor.md`: **Ao terminar** e **Recuperação após commit funcional sem commit de registro**.
- `.agents/skills/implement/assets/registro-template.md`: significado de `Commit`.
- `.agents/skills/plan/SKILL.md`: uso do registro para saber o que já foi feito e arquivamento entre marcos.
- As convenções reais do projeto devem ser consultadas antes de decidir; o arquivo citado em `AGENTS-recolhe.md` não foi lido aqui.

**Critérios para considerar resolvido.** Um projeto/clonagem após integrar e remover a branch ainda consegue localizar a evidência prometida pela política escolhida. Os gates não exigem objetos que a própria política permite perder. A solução não depende de reflogs temporários nem invalida silenciosamente o significado do campo `Commit`.

**Verificação sugerida.** Simular em repositório descartável os dois commits, a estratégia de integração escolhida e uma clonagem nova; conferir hashes/referências. Não experimentar limpeza, squash ou reescrita no repositório real para testar esta hipótese.

## 6. P4 — Separador Markdown válido é recusado pelo atualizador

**Estado:** tolerância aprovada, implementada e coberta por testes positivos/negativos; esquema de seis colunas permanece obrigatório.

**Diagnóstico anterior.** Antes destas alterações, `.agents/skills/implement/scripts/update_registro.py` definia `SEPARATOR = "|---|---|---|---|---|---|"` (linha 20) e, em `find_task()` (linha 47), compara a linha inteira com esse valor. A `plan` exige seis colunas e separador Markdown, mas não exige os mesmos espaços/hífens literais. Por exemplo, a seguinte tabela válida seria recusada pelo script atual:

```md
| Task | Marco | Status | Commit | Atualizado em | Observações |
| --- | --- | --- | --- | --- | --- |
| M01-T01 | M01 | não iniciada | - | 2026-09-30T14:20:00-03:00 | - |
```

O cabeçalho também é localizado por texto literal. Não confundir tolerância de apresentação com aceitar ordem/nomes/quantidade de colunas errados; o problema anterior de deslocamento de colunas precisa continuar impossível.

**O que precisa ser decidido.** Exigir uma serialização exata em todas as skills ou validar a estrutura por células, tolerando variantes de formatação? Se flexibilizar, decidir se aceita espaços, número maior de hífens e marcadores de alinhamento `:`; também definir se o cabeçalho pode variar só em espaços mantendo os mesmos seis nomes na mesma ordem.

**Decisão aprovada e aplicada.** Cabeçalho/separador validados por células, tolerando espaços, três ou mais hífens e alinhamentos `:---`, `---:` e `:---:`. Permanecem obrigatórios os seis nomes na mesma ordem e os `|` externos. Só a linha solicitada é serializada; cabeçalho, separador, outras tasks, notas e quebras CRLF são preservados. Erros não alteram o arquivo; duplicidade de IDs, transições inválidas e reabertura de estados finais continuam recusadas. A única operação posterior em concluída é o vínculo restrito de integração de P3.

**Fontes e arquivos afetados.**

- `.agents/skills/implement/scripts/update_registro.py`: `HEADER`, `SEPARATOR`, `cells()`, `find_task()`, `update()`.
- `.agents/skills/implement/assets/registro-template.md`: exemplo canônico.
- `.agents/skills/plan/SKILL.md`: **Caminhos e ciclo de vida dos arquivos**, contrato de geração.
- `.agents/skills/implement/tests/test_update_registro.py`: sete testes existentes, todos usando separador canônico; falta cobertura das variantes válidas.

**Critérios para considerar resolvido.** A tabela com espaços acima é aceita se a política escolhida for tolerante; separadores inválidos e esquemas de cinco/sete colunas continuam recusados, sem reescrever o arquivo. Duplicidade de IDs, transições indevidas e reabertura de estados finais continuam impedidas. Notas fora da tabela e linhas de outras tasks continuam preservadas.

**Verificação sugerida.** Acrescentar testes de separador com espaços, variações aceitas/rejeitadas de alinhamento e cabeçalho, além de casos negativos de quantidade/ordem de colunas. Exigir que falhas deixem o conteúdo intacto.

## 7. Estado das verificações — não confundir contrato com desempenho

### Verificações desta retomada

- `python -m unittest discover -s .agents/skills/implement/tests -v`: **30 testes, 29 passaram e 1 foi pulado** por falta de permissão para criar symlink no Windows. Nenhum teste falhou.
- Filtro: relatos novos/rastreados/staged/unstaged e Observações não aparecem na saída; código, testes e documentação entregável continuam visíveis; estado do index e arquivos preservado; caminhos dos dois layouts, revisão incompleta, novo ID, snapshot e ambiguidades cobertos.
- Registro: formatação equivalente, esquemas inválidos, CRLF, preservação de notas/timestamps, substituição e atualização de integração restrita/idempotente cobertos.
- Fixture Git descartável: dois commits, squash, vínculo documental, remoção da branch e clone novo. O commit integrado e os achados continuam acessíveis; os commits funcionais/metadados originais não estão no clone. Nenhuma operação Git desse teste foi feita no laboratório ou no Recolhe.
- `bash -n .agents/skills/docs/scripts/scaffold_docs.sh`, JSON de `.agents/skills/plan/evals/evals.json` e `git diff --check`: sem erros nas checagens locais.
- `PyYAML` continua indisponível; o validador completo de `skill-creator` não foi executado e nenhuma dependência foi instalada. O caso 3 dos evals de `plan` foi alinhado à substituição por novo ID, mas os prompts não foram executados com agentes.
- Ainda falta teste do fluxo com agentes em conversas independentes e execução do caso de symlink em ambiente que o permita. Testes de scripts/fixtures **não comprovam** que agentes respeitam a ordem de leitura, aprovação, migração e autorização.
- `docs` e `AGENTS-recolhe.md` permanecem inalterados: o mapa de caminhos existente já atende ao desenho. Não houve commit no laboratório.

### Histórico das verificações anteriores

Na conversa anterior foram executados **sete testes unitários do registro**, com sucesso. Eles cobrem atualização da task certa/preservação do marco e notas; timestamp inalterado ao mudar só observação; rejeição do esquema antigo; rejeição de timestamp sem fuso; transições inválidas/estado concluído; registro ausente/IDs duplicados; e motivo obrigatório para pausar/retomar. São testes do script, não prova de que agentes seguirão o fluxo.

O scaffold da `docs` foi verificado para `AGENTS.md` padrão, `CLAUDE.md` explícito e preservação de arquivo existente. Não gera plano/registro antecipadamente. A sintaxe Bash e `git diff --check` também foram conferidos durante a discussão.

Para reexecutar os testes do registro a partir da raiz:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s .agents/skills/implement/tests -v
bash -n .agents/skills/docs/scripts/scaffold_docs.sh
python -m json.tool .agents/skills/plan/evals/evals.json
git diff --check
```

O ambiente anterior era Windows com Git Bash; scripts Python já deram erro ao imprimir seta Unicode no console, por isso a saída de sucesso do atualizador usa `->`. Não presumir que comandos/dependências de um ambiente anterior estejam disponíveis agora.

**Ainda não executado:** um marco completo com `docs → plan → baseline → implementador → revisor → corretor (se necessário) → dois commits`, em conversas independentes. Esse teste prático é uma verificação adicional, **separada dos quatro problemas acima**. O validador de `skill-creator` havia abortado por falta de `PyYAML` no ambiente anterior; checagens básicas não o substituem. Não instalar dependências automaticamente só para retomar a discussão.

`.agents/skills/plan/evals/evals.json` contém três prompts/resultados esperados, sem fixtures anexadas: planejar um marco; refatiar um rascunho com dependência mal ordenada; e solicitar task/registro/achados ausentes após três correções falhas. Não há resultados de execução desses cenários. O arquivo já não depende de `skill-plano/plano.md`.

## 8. Mapa de fontes e próximo passo

| Arquivo | O que consultar |
|---|---|
| [.agents/skills/plan/SKILL.md](.agents/skills/plan/SKILL.md) | Contrato do plano, IDs, registro, baseline e replanejamento |
| [.agents/skills/implement/SKILL.md](.agents/skills/implement/SKILL.md) | Gate, estados, caminhos, isolamento e dois commits |
| [.agents/skills/implement/references/implementador.md](.agents/skills/implement/references/implementador.md) | Entrega do relatório antes de revisão |
| [.agents/skills/implement/references/revisor.md](.agents/skills/implement/references/revisor.md) | Ordem de leitura, achados, numeração, aprovação e Git |
| [.agents/skills/implement/references/corretor.md](.agents/skills/implement/references/corretor.md) | Escolha da rodada e append do relato |
| [.agents/skills/implement/scripts/update_registro.py](.agents/skills/implement/scripts/update_registro.py) | Parser e transições atuais |
| [.agents/skills/implement/assets/registro-template.md](.agents/skills/implement/assets/registro-template.md) | Esquema do registro |
| [.agents/skills/implement/tests/test_update_registro.py](.agents/skills/implement/tests/test_update_registro.py) | Registro e fixture de integração/clone novo |
| [.agents/skills/implement/scripts/review_inputs.py](.agents/skills/implement/scripts/review_inputs.py) | Entradas filtradas e snapshot para a fase independente |
| [.agents/skills/implement/tests/test_review_inputs.py](.agents/skills/implement/tests/test_review_inputs.py) | Cobertura do filtro, estados incompletos e substituição de ID |
| [.agents/skills/docs/references/claude-md-agents.md](.agents/skills/docs/references/claude-md-agents.md) | Mapa de caminhos no arquivo de entrada |
| [.agents/skills/docs/assets/templates/agent-entrypoint.md](.agents/skills/docs/assets/templates/agent-entrypoint.md) | Template atual, com caminhos previstos |
| [.agents/skills/docs/scripts/scaffold_docs.sh](.agents/skills/docs/scripts/scaffold_docs.sh) | Geração padrão de AGENTS e preservação de existentes |
| [.agents/skills/plan/evals/evals.json](.agents/skills/plan/evals/evals.json) | Cenários preparados, ainda não executados |
| [AGENTS-recolhe.md](AGENTS-recolhe.md) | Contexto da convenção de squash e autorização; não é AGENTS ativo |

As linhas citadas são localizadores da revisão deste handoff; prefira os nomes de seções/funções se os arquivos mudarem.

**Próximo passo sugerido:** validar o fluxo com agentes em conversas independentes, observando a sequência de saídas/leituras e as autorizações, e rodar o caso de symlink onde houver permissão. P1–P4 estão aprovadas e implementadas no laboratório; o comportamento prático dos agentes ainda não foi demonstrado. Versionamento/publicação das alterações locais exige novo pedido explícito.

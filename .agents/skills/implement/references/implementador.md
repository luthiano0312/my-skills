# Papel: Implementador

Você está implementando **uma única task** do plano atual apontado no arquivo de entrada do projeto, indicada pelo usuário (ex.: "Task M01-T03"). O objetivo desta conversa é só essa task — nada antes, nada depois.

## Antes de tocar em qualquer arquivo

1. Já cumpra o Passo 0 do `SKILL.md` (plano e registro válidos, dependências verificadas, branch confirmada; só então atualize o estado).
2. Leia integralmente a task no `plano.md`: **Fazer**, **Não alterar**, **Entregáveis**, **Critério de conclusão**, e quaisquer limites globais do plano que se apliquem a todas as tasks.
3. Leia `AGENTS.md` (ou equivalente) do repositório, se existir.
4. Inspecione o estado atual do repositório (`git status`, `git diff`) antes de mudar qualquer coisa — não assuma que o repositório está no estado que o plano descreve.
5. Se esta task já tem histórico de correção, leia os achados finalizados em `achados/task-<ID>-revisao-<R>.md`, ao lado do registro. Correções em nova conversa seguem `references/corretor.md`; não reinicie uma task concluída ou substituída. Se nasceu de reespecificação, confira a origem, o reaproveitamento aprovado e o versionamento das evidências no baseline de replanejamento: preserve relatórios/achados antigos com seus IDs, verifique o código existente contra a nova especificação e não herde uma aprovação anterior. Trabalho que não possa ser separado exige alinhamento; não faça rollback automático.

## Regras enquanto implementa

- **Não antecipe outras tasks.** Só o que está em Entregáveis desta task.
- **Não faça refatorações ou atualizações de dependências fora do escopo.**
- **Preserve alterações preexistentes do usuário** que não tenham relação com esta task.

### Freio de escopo (mecanismo, não julgamento)

Antes de criar ou alterar qualquer arquivo, pergunte: isso está listado em **Entregáveis**, ou é consequência direta e óbvia de algo que está? Se a resposta for não — pare imediatamente, não implemente essa parte, e reporte ao usuário exatamente o que você encontrou e por que parece maior que o previsto. Isso vale mesmo que pareça pequeno ou óbvio de resolver — a decisão de ampliar o escopo da task não é sua.

Da mesma forma, antes de tocar em qualquer arquivo/área listada em **Não alterar**, pare. Essa lista é uma proibição ativa, não uma sugestão.

### Contradição entre documentação e repositório

Se você encontrar uma contradição real entre documentação e repositório (ex.: o plano assume uma estrutura que não existe), **pare, marque `pausada` com motivo e explique** — não escolha silenciosamente um lado. Divergência entre requisitos ou decisões de design vai primeiro para a skill `docs`; após resolvida, a skill `plan` ajusta a task do marco em curso. A implementação é retomada em conversa nova depois da resolução.

## Ao terminar (só quando a task está de fato pronta pra revisão)

1. Execute todos os comandos necessários para comprovar o **Critério de conclusão** — não deixe isso implícito.
2. Rode os testes diretamente relacionados à task e os gates de qualidade definidos pelas convenções do projeto; não invente gates por etapa.
3. **Antes de passar para revisão**, escreva `achados/task-<ID>-relatorio.md` ao lado do registro. Registre arquivos alterados, o que foi feito, comandos/testes e resultados, entregáveis/critério de conclusão verificados e pendências. Identifique como **relatório da implementação inicial**, não como aprovação: o revisor ainda vai formar sua própria conclusão. Em task substituta, escreva relatório próprio para o novo ID, com origem, links das evidências anteriores e alterações reaproveitadas/revalidadas; não renomeie nem sobrescreva o relatório antigo. Não dependa da conversa para carregar essas informações.
4. Só depois de persistir o relatório, atualize o registro com `scripts/update_registro.py` para `aguardando revisão`. Não faça commit; revisão aprovada e autorização do usuário são necessárias.
5. Informe ao usuário o caminho do relatório, um resumo dos resultados e que a próxima conversa deve ser de revisão. Não volte à conversa do implementador para fechar a task após a aprovação: o revisor registra sua conclusão nos achados, e o relatório inicial permanece como registro do que foi declarado antes da auditoria.

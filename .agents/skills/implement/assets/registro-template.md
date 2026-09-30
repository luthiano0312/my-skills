# Registro de Execução

A skill `plan` cria este registro após o usuário aprovar o marco; a skill `implement` apenas o atualiza com `scripts/update_registro.py`. IDs de task são únicos entre todos os marcos (ex.: `M01-T01`, `M02-T01`). Uma linha por task, sem apagar o histórico ao iniciar outro marco.

`Atualizado em` é o instante da última mudança de status em ISO 8601 com fuso explícito; não é a data do commit nem da integração. `Commit` guarda o hash funcional original da task, não do segundo commit de metadados que versiona esta tabela. Após squash/reescrita, ele é histórico e pode não estar disponível. A garantia posterior é localizar a entrega integrada e as revisões versionadas, não o diff individual original. Nas Observações, acrescente `Integração: <hash-completo>` após conferir o Git, com `scripts/update_registro.py --integration` e autorização explícita para o commit documental posterior. Essa operação preserva notas, status, hash original e timestamp; não reabre a task. Os estados aceitos são `não iniciada`, `em andamento`, `aguardando revisão`, `em correção`, `pausada`, `concluída` e `substituída`. Use `-` para commit ausente e observações vazias; não inclua `|` literal nas observações.

Os seis nomes de coluna e sua ordem são obrigatórios, com `|` externos. Espaços entre células, três ou mais hífens e alinhamentos `:` no separador são tolerados. O exemplo abaixo é canônico, não a única apresentação válida.

| Task | Marco | Status | Commit | Atualizado em | Observações |
|---|---|---|---|---|---|

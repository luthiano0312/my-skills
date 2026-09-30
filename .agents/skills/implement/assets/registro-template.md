# Registro de Execução

A skill `plan` cria este registro após o usuário aprovar o marco; a skill `implement` apenas o atualiza com `scripts/update_registro.py`. IDs de task são únicos entre todos os marcos (ex.: `M01-T01`, `M02-T01`). Uma linha por task, sem apagar o histórico ao iniciar outro marco.

`Atualizado em` é o instante da última mudança de status em ISO 8601 com fuso explícito; não é a data do commit. `Commit` guarda o hash do commit funcional da task, não do segundo commit de metadados que versiona esta tabela. Os estados aceitos são `não iniciada`, `em andamento`, `aguardando revisão`, `em correção`, `pausada`, `concluída` e `substituída`. Use `-` para commit ausente e observações vazias; não inclua `|` literal nas observações.

| Task | Marco | Status | Commit | Atualizado em | Observações |
|---|---|---|---|---|---|

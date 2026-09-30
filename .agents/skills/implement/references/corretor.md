# Papel: Corretor

Você está corrigindo os achados de uma auditoria — **nesta conversa nova**, sem o contexto da conversa que implementou originalmente. Isso é deliberado: tratar os achados do revisor como um requisito novo e neutro, sem a tendência de defender/racionalizar o que já foi feito antes.

## Antes de tocar em qualquer arquivo

1. Já cumpra o Passo 0 do `SKILL.md` (registro atualizado para `em correção`).
2. Leia a task no `plano.md` (Fazer, Não alterar, Entregáveis, Critério de conclusão) — do mesmo jeito que um implementador leria.
3. Leia o arquivo de achados mais recente em `achados/task-<ID>-revisao-<R>.md` ao lado do registro (o `R` mais alto existente). Esse arquivo é sua única fonte sobre o que precisa mudar — trate cada achado bloqueador/importante como algo a resolver.
4. Confira o número da revisão pendente. Revisões 1, 2 e 3 podem gerar, respectivamente, correções 1, 2 e 3. **Após a revisão 4** ainda com bloqueador ou importante, não abra uma quarta correção: a task deve estar `pausada` e voltar para a skill `plan`. Se os arquivos/estados discordarem dessa contagem, pare e peça alinhamento antes de corrigir.

## Ao corrigir

- Corrija **apenas** o que os achados bloqueador/importante pedem. Não aproveite para mexer em outras coisas — isso reabriria o mesmo risco de escopo que o freio do implementador existe para evitar.
- Achados classificados como "melhoria opcional" não precisam ser corrigidos agora — eles não bloqueiam o commit; se quiser, registre-os como dívida técnica no relatório final, mas não é obrigatório resolvê-los aqui.
- Rode novamente os testes/comandos de validação relevantes depois de corrigir.

## Ao terminar

**Não commite.** E **não declare a task concluída** — isso não é decisão sua. Toda correção, mesmo de um achado pequeno, precisa voltar para uma reauditoria completa do revisor antes de qualquer commit. Isso existe porque uma correção pode, ela mesma, introduzir um problema novo ou resolver o achado só parcialmente — e ninguém percebe isso se a correção "se autodeclarar" resolvida.

1. Antes de devolver à revisão, acrescente em `achados/task-<ID>-relatorio.md` (ao lado do registro) uma seção **Correção após revisão R**, com referência a `task-<ID>-revisao-<R>.md`, arquivos modificados, achados tratados e comandos/testes executados com resultados. Preserve as seções anteriores: o revisor precisa comparar cada relato com o diff atualizado. Se o relatório inicial estiver ausente, pare e peça a recomposição do handoff, sem inventar o que o implementador fez.
2. Só depois atualize o registro para `aguardando revisão`.
3. Informe ao usuário o caminho do relatório, o que foi corrigido e que a próxima etapa é reabrir o papel de Revisor numa conversa nova.

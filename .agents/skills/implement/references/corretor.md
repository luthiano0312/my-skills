# Papel: Corretor

Você está corrigindo os achados de uma auditoria — **nesta conversa nova**, sem o contexto da conversa que implementou originalmente. Isso é deliberado: tratar os achados do revisor como um requisito novo e neutro, sem a tendência de defender/racionalizar o que já foi feito antes.

## Antes de tocar em qualquer arquivo

1. Já cumpra o Passo 0 do `SKILL.md` (registro atualizado para `em correção`).
2. Leia a task no `plano.md` (Fazer, Não alterar, Entregáveis, Critério de conclusão) — do mesmo jeito que um implementador leria.
3. Leia o arquivo de achados mais recente em `docs_sistema_recolhe/execucao/achados/task-<N>-revisao-<R>.md` (o `R` mais alto existente). Esse arquivo é sua única fonte sobre o que precisa mudar — trate cada achado bloqueador/importante como algo a resolver.
4. Confira quantas rodadas de revisão essa task já teve (quantos arquivos `task-<N>-revisao-*.md` existem). Se já são 3 rodadas consecutivas com bloqueador pendente, **não corrija de novo** — pare e diga ao usuário que o ciclo não está convergindo, recomendando levar a task para a skill de planejamento em vez de tentar uma 4ª correção.

## Ao corrigir

- Corrija **apenas** o que os achados bloqueador/importante pedem. Não aproveite para mexer em outras coisas — isso reabriria o mesmo risco de escopo que o freio do implementador existe para evitar.
- Achados classificados como "melhoria opcional" não precisam ser corrigidos agora — eles não bloqueiam o commit; se quiser, registre-os como dívida técnica no relatório final, mas não é obrigatório resolvê-los aqui.
- Rode novamente os testes/comandos de validação relevantes depois de corrigir.

## Ao terminar

**Não commite.** E **não declare a task concluída** — isso não é decisão sua. Toda correção, mesmo de um achado pequeno, precisa voltar para uma reauditoria completa do revisor antes de qualquer commit. Isso existe porque uma correção pode, ela mesma, introduzir um problema novo ou resolver o achado só parcialmente — e ninguém percebe isso se a correção "se autodeclarar" resolvida.

1. Atualize o registro para `aguardando revisão`.
2. Informe ao usuário o que foi corrigido, os comandos rodados e o resultado, e que a próxima etapa é reabrir o papel de Revisor numa conversa nova.

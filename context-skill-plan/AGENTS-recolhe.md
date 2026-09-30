# AGENTS.md

> Roteiro sempre carregado no início da sessão. Mantenha curto e denso — não copie a documentação detalhada pra cá, aponte pra ela.

## Sobre o projeto
Sistema de Gestão de Locação de Containers ("Recolhe") para o Venâncio: os caminhoneiros cadastram a Ordem de Serviço (OS) direto pelo site (celular) no momento da entrega, com impressão térmica da via do cliente e modal de pagamento Pix. Substitui o controle 100% em Excel, incluindo gestão dos 40 containers, diárias extras e painel de cobranças.

## Status
- Implementação iniciada: scaffold Laravel 13 criado em `src/`; funcionalidades de domínio ainda não implementadas.
- Próxima task: consultar o plano atual e o registro de execução indicados abaixo; não manter uma sequência de implementação duplicada neste arquivo.
- Meta de primeiro marco: **30/09/2026** (flexível, não é data rígida).
- Pendência técnica externa: impressora MTP5 aguardando entrega; homologação física ainda pendente.

## Convenções
- Convenções completas de código, documentação e Git: `docs_sistema_recolhe/reference/convencoes-de-desenvolvimento.md`.
- Documentação é um Obsidian vault — use `[[arquivo]]` ao referenciar documentos dentro dele.
- Documentos ativos são fonte de verdade; não use `docs_sistema_recolhe/_archive/` como fonte, apenas como histórico.
- Documentação, UI, branches e commits em português; identificadores técnicos em inglês. Capitalização segue o ecossistema: banco em `snake_case`, classes/componentes em `PascalCase` e métodos/variáveis em `camelCase`.
- `main` deve permanecer funcional; mudanças planejadas usam branches curtas e entram por squash com Conventional Commits. Commit direto só para ajuste documental trivial.
- Antes de editar, confira branch e status e inspecione as mudanças conforme o papel. Na fase independente do revisor, use `review_inputs.py` da skill `implement` antes de ler diffs/conteúdos; não carregue relatos, achados anteriores ou Observações do registro antecipadamente.
- Com worktree sujo, não troque de branch nem use `stash`; não execute commit, push, merge ou squash sem pedido explícito. Preserve alterações preexistentes do usuário.
- A conclusão de uma task exige autorização explícita para os dois commits: funcional e registro. Aprovação técnica não autoriza commits; merge/squash e push exigem autorização própria.
- Após squash, `Commit` permanece como hash original histórico. Confira a entrega integrada no Git e registre `Integração: <hash-completo>` nas Observações, com commit documental posterior explicitamente autorizado, sem mudar status, hash original ou timestamp. Detalhes nas convenções e no fluxo de desenvolvimento referenciados; se divergirem destas instruções, pare e peça alinhamento.
- Estratégia de testes: `docs_sistema_recolhe/02-design/estrategia-de-testes.md`.

## Comandos
Execute dentro de `src/`:
- Preparação inicial: `composer run setup`
- Desenvolvimento: `composer run dev`
- Gate de qualidade (PHP, Pint, JS e build): `composer run check`
- Testes backend: `composer run test`
- Testes frontend: `npm run test` (`npm run test:watch` para desenvolvimento)
- Formatação PHP (verificação): `vendor/bin/pint --test`
- Build frontend: `npm run build`

Fluxo completo: `docs_sistema_recolhe/how-to/fluxo-de-desenvolvimento.md`.

## Planejamento e execução (caminhos previstos — confirmar no projeto real)
- Plano atual: `docs_sistema_recolhe/plano.md`
- Registro de execução: `docs_sistema_recolhe/execucao/registro.md`
- Relatórios e revisões: `docs_sistema_recolhe/execucao/achados/`
- Planos encerrados: `docs_sistema_recolhe/planos/` — somente consulta histórica, não carregar por padrão.

O plano especifica as tasks; o registro é a fonte de verdade do progresso. Confirme a existência desses arquivos no Recolhe: este mapa não comprova que existam. Se ausentes, a skill `plan` cria plano/registro após aprovação, sem gerar arquivos vazios para satisfazer o mapa, e confirma os caminhos neste arquivo. Antes de iniciar uma nova task, siga a checagem de baseline versionado da skill `implement`.

## Documentação — onde procurar (tudo sob `docs_sistema_recolhe/`)
- Escopo (in/out de escopo, restrições): `01-requisitos/escopo.md`
- Backlog priorizado (MoSCoW): `01-requisitos/backlog.md`
- Regras de negócio (RN): `01-requisitos/regras-de-negocio.md`
- Stakeholders: `01-requisitos/stakeholders.md`
- Casos de uso: `01-requisitos/casos-de-uso/*.md`
- Arquitetura HLD / modelo de dados / APIs / UI-UX: `02-design/` — modelo de dados (DER lógico) já existe: `02-design/modelo-de-dados.md`
- Decisões arquiteturais (ADRs): `02-design/adr/*.md` — **carregue apenas estes por padrão, não recursivo**
- Histórico de decisões substituídas: `02-design/adr/archive/` — **só abra aqui se for investigar por que uma abordagem anterior foi descartada, ou antes de propor uma mudança arquitetural grande**
- Convenções de desenvolvimento: `reference/convencoes-de-desenvolvimento.md`
- Guias operacionais: `how-to/` — fluxo local e Git em `how-to/fluxo-de-desenvolvimento.md`

## Antes de propor uma mudança arquitetural
Verifique `docs_sistema_recolhe/02-design/adr/` primeiro — a decisão pode já ter sido tomada e documentada com o motivo. Se a decisão for nova, registre como ADR seguindo a convenção da pasta.

## Antes de alterar requisitos ou regras de negócio
Regras de negócio (RNxx) são referenciadas em backlog e casos de uso — ao alterar uma RN, verifique o impacto nos arquivos que a citam (busque pelo ID da RN).

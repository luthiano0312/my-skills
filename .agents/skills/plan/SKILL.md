---
name: plan
description: >-
  Planeja um marco de implementação de software por vez: analisa documentação e estado do projeto, revisa um plano existente como rascunho, divide e ordena tasks por dependências e entregas verificáveis, e mantém o plano atual e o registro de execução. Use quando o usuário pedir para criar, refazer, fatiar ou reorganizar um plano de implementação, planejar o próximo marco, ou reespecificar tasks que não convergiram na execução — inclusive sem mencionar o nome da skill. Não acione só por uma pergunta sobre planejamento. Mesmo se invocada explicitamente por comando, confirme antes de começar a análise e peça aprovação antes de gravar arquivos.
---

# Plano de implementação por marco

Produza um plano **executável por uma task de cada vez**, não um roadmap detalhado para o projeto inteiro. A skill `docs` cuida de requisitos, análise e design; esta skill transforma essas fontes em tasks de implementação; a skill `implementacao` consome as tasks e mantém o progresso. Um plano preexistente (inclusive `plano.md` fornecido pelo usuário) é **rascunho a criticar e refatorar**, não modelo ou fonte de verdade superior aos requisitos.

## Portas de confirmação

1. Antes de iniciar a análise do projeto, pergunte se o usuário quer **iniciar o planejamento**. Faça isso mesmo após comando explícito. Não vasculhe o repositório nem altere arquivos antes da resposta; se a solicitação era apenas discutir a skill ou explicar um plano, responda sem iniciar o fluxo.
2. Após a confirmação, analise o contexto e **proponha um recorte de marco**. Peça confirmação/ajuste desse recorte: prioridade e risco pertencem ao usuário, não são dedutíveis só do código. Não exija caminho, nome de marco ou lista de tasks na invocação; pergunte apenas o que não conseguir descobrir com segurança.
3. Prepare a proposta detalhada (em conversa ou rascunho explicitamente provisório), mostre recorte, tasks, dependências, mudanças em relação ao plano recebido e lacunas. **Antes de salvar, arquivar ou alterar `plano.md` e `registro.md`, obtenha aprovação explícita do conteúdo**. A autorização para analisar NÃO autoriza a gravação. Se a proposta mudar após aprovação, peça nova aprovação da parte alterada.
4. Depois de aprovada, salve o plano e inicialize/reconcilie o registro na **mesma conversa**; confira que ambos correspondem. Não implemente código, não faça commits e não atualize o status de execução por conta própria.

## Descoberta e limites

- Leia `AGENTS.md`/`CLAUDE.md` do projeto e descubra a raiz real da documentação. Leia **só** as fontes relevantes ao próximo marco: escopo do sistema, prioridades/backlog, requisitos e regras, arquitetura/ADRs ativos, convenções e testes; consulte histórico arquivado só quando necessário. Não use ADRs substituídos nem planos anteriores como regras atuais. Resolva links locais (`[[nome]]`, caminhos etc.) antes de citá-los; não alegue ter verificado fonte ausente.
- Para saber o que já foi feito, use `registro.md` quando existir; confira no repositório no primeiro marco ou ao detectar sinais de divergência. Se registro, documentação e código conflitarem, mostre a divergência e peça resolução antes de depender dela. Não substitua a função do registro por inferência silenciosa do Git.
- `escopo.md` permanece a visão global; não o reescreva a cada marco. Se requisitos/ADRs se contradisserem ou faltar decisão de domínio/arquitetura, **pare a task afetada e encaminhe à skill `docs`** (verificação/validação ou gestão de requisitos). Não invente regra nem altere a documentação para acomodar o plano.
- Confirme o que já está modificado pelo usuário antes de sobrescrever; preserve conteúdo e histórico fora do escopo aprovado.

## Escolher o marco e compor as tasks

1. Parta do escopo e prioridades, considere entregas já registradas e agrupe por dependências reais. Proponha um marco útil e limitado; registre adiamentos sem duplicar a fonte de verdade do escopo. Não fatia antecipadamente marcos distantes que provavelmente mudarão.
2. Uma task tem **no máximo uma entrega coerente, verificável e revisável de forma independente**. Em funcionalidades, prefira um comportamento fim a fim (backend + interface quando ambos são necessários); em infraestrutura, um resultado técnico testável. Vários testes da mesma entrega não exigem divisão. Se duas entregas têm critérios independentes e podem ser commitadas separadamente, divida. Tasks preparatórias só entram quando desbloqueiam algo concreto.
3. Infira dependências **obrigatórias** a partir de pré-condições, artefatos consumidos e critérios de conclusão; justifique cada seta. Separe-as de preferências de sequência e de dependências externas (hardware, acesso, aceite). Não transforme uma lista cronológica em cadeia rígida sem evidência. Se detectar ciclo ou consumo de algo entregue só depois (ex.: cadastro de OS requer reconciliação planejada para uma task posterior), divida/redefina tasks antes de ordenar; não aceite implementação provisória que viole requisito para preservar numeração.
4. Ordene fisicamente as tasks no arquivo na **sequência prática sugerida**, respeitando dependências e minimizando retrabalho e vai e vem. Pode haver outras ordens válidas; peça validação do usuário. A seção de dependências mostra só vínculos obrigatórios justificados, não repete toda a ordem do arquivo. Execução continua sequencial, uma task por vez; dependências não autorizam paralelismo automático.
5. Use **etapas** apenas se agruparem trabalho de modo útil. Não acople a identidade da task à posição da etapa: IDs devem ser únicos no marco e permanecer estáveis depois da aprovação/primeiro uso. Antes da primeira aprovação, refatore e renumere livremente; com marco em execução, preserve vínculos de registro e achados ao alterar IDs.

## Formato do `plano.md`

Adapte a extensão à complexidade do marco. Mantenha nesta ordem:

- **Cabeçalho:** status, identificação e recorte do marco com referência ao escopo global, pré-condições externas e fontes de verdade **curadas** (caminhos reais, não cópia de regras/stack).
- **Ordem e dependências:** a ordem das tasks já é a sequência recomendada; diagrama ou tabela enxuta só para dependências obrigatórias e suas justificativas, mais bloqueios externos quando houver. Não crie dependências artificiais.
- **Etapas opcionais e tasks:** em cada task, `Fazer`, `Não alterar`, `Entregáveis` e `Critério de conclusão` observável. Cite requisitos/IDs de testes relevantes; não prometa testes impossíveis de executar no marco. Declare pendências externas e critérios de aceite para homologação sem fingir que foram atendidos.
- **Resultado esperado ao final do marco:** síntese **derivada dos Entregáveis e Critérios de conclusão** das tasks, sem novos requisitos nem estados prematuros. Se não for derivável, corrija as tasks ou a expectativa antes de salvar.

Em `Não alterar`, use `[Fonte: caminho#trecho]` para restrição derivada de documentação verificável. Durante o rascunho, marque deduções como `[Proposta sem fonte]`. Na aprovação, cada uma deve ser **excluída** ou explicitamente aceita e renomeada `[Decisão deste marco]`. Depois de aprovado, **todo** `Não alterar` é obrigatório para a implementação; não deixe sugestão ambígua nessa seção. Se uma proposta contrariar uma fonte, resolva o conflito antes de aprovar.

Não replique seções globais de Objetivo, Limites, Tecnologias, Definition of Done, gates acumulativos ou sugestões de commits quando a informação já vive em escopo, ADR, arquitetura, convenções ou na skill `implementacao`. Não crie gate por etapa que apenas repete os critérios das tasks. O resultado esperado deve servir para conferir cobertura do marco, não repetir uma promessa vaga. Se faltar convenção essencial, aponte a lacuna em vez de inventar um documento global dentro do plano.

## Caminhos e ciclo de vida dos arquivos

Descubra a raiz existente, não a reorganize apenas por estética. No Recolhe, o layout conhecido é:

```text
docs_sistema_recolhe/
├── plano.md                  # apenas marco atual
├── planos/marco-<id>.md      # marcos encerrados
└── execucao/
    ├── registro.md           # progresso de todos os marcos
    └── achados/              # produzido pela implementacao
```

Para **novos projetos sem convenção existente**, proponha `docs/03-execucao/` como área de execução, com `plano.md`, `planos/`, `registro.md` e `achados/` dentro dela. O plano atual fica na raiz da **área escolhida**, não necessariamente na raiz de `docs/`. Registre os caminhos escolhidos no arquivo de entrada do projeto se ele for mantido por outro fluxo; não espalhe novos caminhos hard-coded por vários documentos.

- Inicialize `registro.md` **após aprovação do plano**, com uma linha por task nova: ID, marco, status `não iniciada`, commit vazio, data e links/observações quando úteis. Não copie requisitos ou entregáveis para o registro; `plano.md` é a especificação e `registro.md` é a fonte de verdade de progresso. Não apague linhas históricas ao criar novo marco.
- A skill `implementacao` assume a partir daí: `em andamento` → `aguardando revisão` → (`em correção` → nova revisão)* → `concluída` **só após revisão aprovada e commit**. Guarde links para achados e relatório. Se a task for substituída, preserve a linha antiga com status/vínculo `substituída por ...` e crie linhas novas; nunca apague evidências.
- Ao planejar novo marco, consulte o registro e o plano anterior para pendências/adiamentos. Só arquive o plano atual **quando o marco for encerrado com ciência do usuário**; trate tasks inacabadas explicitamente antes de arquivar. Mova para `planos/marco-<id>.md` sem sobrescrever arquivo antigo; o novo marco passa a ocupar `plano.md`. Carregue planos arquivados só no planejamento do próximo marco ou investigação histórica, não por padrão durante implementação.

## Replanejar um marco em andamento

- Se `implementacao` encontrar contradição entre documentos: bloqueie a task e remeta à `docs`; após a resolução aprovada, volte aqui para ajustar o plano em curso **in place**, sem arquivar/reabrir o marco.
- Se três rodadas de correção não convergirem e o problema for a especificação/fatiamento: leia **somente** a task persistida, `registro.md` e os arquivos de achados já escritos; não reabra diff/código para refazer a revisão. Proponha dividir/redefinir a task, com novos critérios e migração de IDs/estado quando necessário; peça aprovação antes de editar plano e registro. A implementação recomeça em conversa nova.
- Se os achados não bastarem para especificar a correção, peça informação ao revisor/usuário; não adivinhe. Se uma mudança passar a afetar escopo, regra ou arquitetura, encaminhe primeiro à `docs`.

## Verificação antes de entregar

Confira que cada task tem entrega verificável, `Não alterar` sem sugestões pendentes, fontes existentes, dependências sem ciclos, critérios coerentes com resultado esperado e IDs alinhados ao registro. Relate o que foi aprovado, o que foi gravado (com caminhos), os bloqueios restantes e qual task está apta a começar. Não declare testes ou marcos concluídos sem evidência.

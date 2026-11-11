# Anexos — segundo piloto

## 1. Fontes e convenção de citações

**S:n** = linha física n, contada desde 1, do único JSONL autorizado:
`C:/Users/User/projetos/sistema_recolhe_sessions/.pi/sessions/2026-10-06T18-48-46-681Z_01a1128b-fd58-76ba-9a42-08e3deffe2a2.jsonl`.
A localização aponta ao evento inteiro; textos de arquivos dentro de um resultado são identificados também pelo caminho e seção/função. **S:a–b** é intervalo inclusivo. IDs nas tabelas permitem busca independente da numeração.

| Fonte | Cobertura / uso | SHA-256 dos bytes originais |
|---|---|---|
| S | 91 registros, 594392 bytes; fonte histórica primária | `399c5bce55ef072393e42d8ee06b303570fc47718c34486a9ce3a6f17650ce4c` |
| AUX12 | `C:/Users/User/AppData/Local/Temp/pi-codemode-749c11bbaa8e904c.txt`, 53124 bytes, seis linhas JSON; associado a S:11–12 | `edec0a1a8552526e13af8958a80caeec7e1b0820373577868c80128cad299291` |
| AUX16 | `C:/Users/User/AppData/Local/Temp/pi-codemode-18a30eca819c3df9.txt`, 61427 bytes, seis linhas JSON; associado a S:15–16 | `8b24b8cf9045be6220837557face896c487655210a67338b0d185ea667304d1d` |
| C-PLAN | `.agents/skills/plan/SKILL.md`, atual, comparação conceitual | `685863fbd7dc9266415200849876ef6d77264e470f0e5f4bbccda847f498893c` |
| C-IMP | `.agents/skills/implement/SKILL.md`, atual | `00b6ade4ac97fc3dfe966a66a1f53f19a7d136c50a30bde2a0eaf2047fd2ea12` |
| C-ROLE | `.agents/skills/implement/references/implementador.md`, atual | `55c5f8b83dfa6ee17ec0c6a04abce6331f58ced3847cc7d53a9649a059439257` |

As três referências atuais ficam sob `C:/Users/User/projetos/my-skills/`; não substituem a prova histórica.
`skill-creator/SKILL.md` orientou somente esta análise de melhoria; não integra a execução histórica, não houve benchmark novo nem otimização das skills.

### Preservação mínima e triagem

- Auxiliares integrais foram lidos passivamente e decodificados como JSON. Contêm documentação do projeto e nomes de envolvidos; não foram copiados integralmente.
- Preservado apenas `evidencias/auxiliares-recortes.md`: AUX12:3, `value`, linhas internas 197–219 (contrato da M01-T07 e adiamento de T-AUTH-01); AUX16:6, `content`, linhas internas 13–22 (diretrizes do HLD ausentes na saída truncada).
- Os recortes não contêm credenciais, cookies, e-mails, telefones ou nomes pessoais; inspeção textual e busca por padrões de segredos antes da gravação. Não foi necessário substituir conteúdo dentro desses recortes. A seleção omite o restante, não pretende ser cópia integral.
- SHA-256 **da cópia selecionada**, distinto das fontes: `3819b8f4242308b238bd7e4f023346c296614393510815e74fc7856eaa0fb132`.
- Fonte JSONL é durável e não foi copiada. Renderizações temporárias locais serviram apenas à leitura em partes; não são entregáveis nem substitutos de S. Strings de assinatura cifrada foram identificadas como opacas, não interpretadas; nenhum conteúdo histórico foi executado.
- `analises-sessoes/piloto.md` não foi lido como corpus nem alterado; hash de preservação: `137fbb2c0008ac49f6e532508e442023844a1b922539cafc400345882453d3ca`.

## 2. Trajetória e limites de leitura

S:1 é cabeçalho da sessão (`cwd` histórico `C:/Users/User/projetos/sistema_recolhe`). S:2 tem `parentId: null`; os 90 eventos de S:2 a S:91 formam uma única cadeia. Não há pais com múltiplos filhos, referências pendentes, compactações, resumos de ramificação ou `responseId` repetido.
Há 79 mensagens: 1 system, 1 user, 39 assistant e 38 toolResult; demais eventos são cinco mudanças de modelo, cinco de thinking e um nome de sessão.
S:8–85 contém todo o pedido/trabalho/handoff. S:86–87 muda thinking após a entrega; S:88–91 registra configurações em 11/11, sem mensagens ou ferramentas adicionais. Incluir esses metadados no tempo da implementação criaria duração artificial de semanas.

Leitura integral do conteúdo decodificado em 16 partes, incluindo comandos, argumentos de escrita, saídas, metadados e texto de thinking quando presente. O JSONL foi integralmente parseado. Assinaturas opacas/cifradas não são raciocínio legível ou telemetria de tempo ativo.
Não foram consultados arquivos atuais do `sistema_recolhe`, outros JSONLs nem sessões relacionadas. Somente dois auxiliares diretamente apontados foram recuperados. Todos os comandos históricos foram tratados como dados.

### Agente histórico versus analista

| Informação | Visibilidade histórica comprovada | Recuperação apenas nesta análise |
|---|---|---|
| `implement` e implementador | Corpo injetado em S:8; referência completa em S:10 | Comparação com arquivos atuais e hashes normalizados |
| Plano geral | Parcial em S:12; task M01-T12 integral em S:16; grep de seções em S:14 | AUX12 integral, inclusive critérios de M01-T07 omitidos no trecho truncado |
| UC01 e regras | Parcialmente afetados em S:16; leituras completas em S:20 e S:24 | AUX16 permite conferir o que a primeira saída havia omitido |
| HLD | Cauda de S:16, incluindo fluxos e transações; não há leitura posterior completa | Início/diretrizes recuperados de AUX16; recorte preservado |
| Arquivos/testes entregues | Argumentos de write/edit e respectivos resultados, testes e status em S | Não houve reabertura de conteúdo atual para “confirmar” retroativamente |

Avisos de truncamento: S:12 (`original token count: 12909`, corte central de 2909 tokens) e S:16 (`14904`, corte central de 4904). Esses números pertencem ao renderizador da ferramenta, **não** ao `usage` do modelo. Os auxiliares existiam na análise e tinham seis objetos válidos cada; vínculo pelo `details.fullOutputPath` e pelo caminho também exibido na resposta.
O agente não chamou `read` nesses auxiliares; recuperou seletivamente task, UC01 e regras por outras leituras. A presença de um arquivo no auxiliar não significa que seu conteúdo integral entrou no contexto histórico.

## 3. Instruções históricas efetivamente presentes e comparação

| Origem histórica | Instrução relevante / aplicação observada | Comparação permitida |
|---|---|---|
| S:7, `sections.project_context` e S:12, AGENTS/convenções | Mapa real; branch limpa; commits e integração só por solicitação; gate em `src/` | Contexto histórico capturado, sem depender de AGENTS atual |
| S:8, corpo de `implement` | Consumir plano, validar baseline/dependências; papéis isolados; não concluir task antes de revisão e commits autorizados | Corpo normalizado idêntico ao C-IMP; frontmatter histórico integral não disponível |
| S:10, `references/implementador.md` | Uma task; freio de escopo; testes e relatório inicial antes de `aguardando revisão`; sem commit | Texto normalizado idêntico ao C-ROLE |
| S:16, plano M01-T12 | Fazer/Não alterar/Entregáveis/Critério; teste local de interrupção sem aceite de campo | C-PLAN atual pede recorte verificável e pendências honestas; autoria/versão histórica da skill não comprovada |
| S:16,20,24,78 | Regras, modelo, UC01 e ADRs, com diferentes graus de visibilidade | São fontes de domínio históricas, não regras adicionais para o analista |

Normalização aplicada programaticamente: UTF-8 decodificado, CRLF→LF e `strip()` externo; no texto injetado, corpo entre `# Implementação` e `</skill>`; no atual, YAML removido. Hashes UTF-8 normalizados:
- Corpo `implement`: `c82706a7cfee87f979e7ff9ba7fad6ec9e3f5b7d26ae878356353fb1e994035a`.
- Implementador: `32b4a84afdbba8e41d3601b144aae4b79c6d280bf6ea8fe610717b7c36d5cf6d`.

Não há número de release/hash Git histórico da skill. Igualdade textual do corpo não prova igualdade de scripts, demais referências ou pacote. `plan` aparece apenas como metadado disponível no sistema; nenhuma leitura de seu `SKILL.md` histórico foi encontrada. Não aplicar portas de confirmação da `plan` atual a esta solicitação de implementação.

## 4. Cronologia relevante (UTC do envelope)

| Local / evento | Timestamp | Evidência curta / significado |
|---|---|---|
| S:8 `54ddd308` | 18:49:19.374 | “implementa a M01-T12” |
| S:12 `9b128857` | 18:49:35.699 | `main`, status sem alterações, três caminhos rastreados |
| S:18 `c35c024f` | 18:49:59.448 | `AssertionError` no primeiro gate textual; execução interna retorna 1 |
| S:20 `e2a36e61` | 18:50:11.633 | Seis integrações, checagem UTF-8 corrigida |
| S:22 `5ad8d584` | 18:50:32.765 | Branch criada; script → `em andamento` |
| S:48 `72748806` | 18:55:02.832 | 59/60 PHP; fixture viola CHECK de pagamento |
| S:56 `92500dd0` | 18:56:57.990 | 61/61 PHP; 9/12 JS; erros do modal |
| S:62 `cfe972ee` | 18:58:22.623 | Primeiro gate verde: 421 PHP, 50 JS |
| S:64/66/68/70 | 18:59:29.647–19:00:39.338 | Três tentativas de smoke; limpeza comprovada em comando separado |
| S:72/74/76 | 19:01:04.441–19:01:33.232 | Ajuste de confirmação/navegação e mais testes |
| S:78 `306d874b` | 19:02:40.165 | Gate final 424 PHP / 51 JS, Pint e build |
| S:80 `35989903` | 19:03:18.794 | Subconjuntos finais 44 PHP / 13 JS |
| S:82 `bbf8632a` | 19:04:24.448 | Relatório inicial escrito |
| S:84 `5bbaf709` | 19:04:32.788 | Script → `aguardando revisão`; arquivos ainda modificados/novos |
| S:85 `0c300f2a` | 19:04:37.079 | Encerramento do implementador, nova conversa de revisão indicada |

Não houve resposta adicional do usuário, mudança de escopo, aprovação de review ou permissão de commit. Mudança externa no código não é demonstrada; mudanças posteriores de metadados não provam interferência no trabalho.

## 5. Entregáveis e critérios observáveis

### Inventário final da M01-T12

Base `src/`, salvo quando indicado. S:84 lista nove caminhos modificados e oito novos, **não** um commit. Argumentos de escrita/edição e retornos comprovam produção, não só declaração no relatório.

| Grupo | Caminhos | Evidência |
|---|---|---|
| Novos de produção | `app/Http/Requests/StoreServiceOrderRequest.php`; `app/Services/CreateServiceOrder.php`; `app/Http/Controllers/CreateServiceOrderController.php`; `resources/js/Pages/ServiceOrders/Create.jsx` | S:25–32,41–42; último ajuste S:71–72 |
| Novos de testes | `tests/Feature/CreateServiceOrderTest.php`; `tests/Feature/CreateServiceOrderConcurrencyTest.php`; `resources/js/tests/CreateServiceOrder.test.jsx` | S:43–44,51–54; correções/aditivos S:49–50,59–60,73–76 |
| Modificados de produção | `routes/web.php`; `app/Http/Controllers/TodayServiceOrderController.php`; `resources/js/Pages/ServiceOrders/Show.jsx`; `resources/js/Layouts/AuthenticatedLayout.jsx`; `app/Http/Controllers/Auth/AuthenticatedSessionController.php`; `bootstrap/app.php` | S:33–34; diffs S:70,80 |
| Testes adaptados | `tests/Feature/Auth/AuthenticationTest.php`; `tests/Feature/Auth/AuthorizationTest.php` | S:33–34,80; trocas de destino para Nova OS, demais assertions preservadas |
| Documentação/estado | `docs_sistema_recolhe/execucao/achados/task-M01-T12-relatorio.md`; `docs_sistema_recolhe/execucao/registro.md` | S:81–84; relatório antes da transição |

### Ligação entre critérios e prova

| Critério do plano em S:16 | Prova de código/teste na sessão | Limite |
|---|---|---|
| Cliente existente/novo, homônimos e busca | S:31,43: busca por chave normalizada e IDs; teste inline e de busca; S:53: seleção por ID e conservação de campos | Não é curadoria administrativa nem benchmark de volume |
| Validação, snapshots e pagamento | S:25,27,43: conversores, campos autorizados, snapshots do banco, limites; Pix/dinheiro com `paid_at = started_at`; S:78,80: suites verdes | Testar configuração válida consumida não equivale a entregar edição administrativa da configuração |
| Reconciliação e atomicidade | S:27,43,51,73: reconciliação na transação, escrita condicional, trigger de rollback e leitura independente | Nenhuma migration/constraint foi removida; ausência de efeitos parciais exercitada nos casos descritos |
| T-RN24-02, concorrência | S:51: arquivo SQLite temporário em WAL, conexões writer/competitor/reader; callback após escrita dispara tentativa sobreposta; um confirma, outro recebe ValidationException; índice rejeita duplicata direta | Sobreposição determinística em um processo, não stress test de requisições HTTP multiprocesso |
| T-UC01-12, repetição | S:43,53: guarda síncrona/fieldset e rejeição no servidor; S:71,75 adicionam bloqueio após confirmação | Sem chave durável de idempotência; relatório admite o limite em S:81. Não elevar esse requisito sem necessidade aprovada |
| Confirmação e Concluir | S:33,43,53: dados persistidos, link para hoje, consultas não alteram OS; S:67–68: confirmação e lista via HTTP | RTL verifica destino do link, não interação real de navegador com servidor |
| T-RN10E-01 e T-AUTH-01 | S:33,43,53,59: destino driver, modal nas três telas, textos/QRs; S:67–68: login real redireciona para Nova OS | Decodificação independente do QR pertence à dependência anterior, não foi reexecutada aqui |
| Interrupção local | S:53: mock de `fetch` lança TypeError, mantém campos, não navega/declara sucesso e permite nova tentativa; S:75: erro de navegação após confirmação | É interrupção simulada no componente; sem aceite manual de T-UC01-13, sem E2E de navegador |
| Sem impressão | Ausência de implementação/botões de impressão e assertions negativas S:53; relatório S:81 mantém adiamento | UC01 completo, hardware e operação de campo não entregues |

### Testes e verificações executados

Comandos da aplicação historicamente em `src/`; os abaixo são **registros, não instruções a executar**.

| Local | Comando/atividade | Resultado e telemetria reportada |
|---|---|---|
| S:47–48 | `php artisan test --compact --filter='CreateServiceOrderTest\|AuthenticationTest\|AuthorizationTest'` | 60 testes, 59 passed, 418 assertions, 1 erro, `duration_ms: 7011`, exit 2 |
| S:49–50 | Fixture: `.state([...started_at...])->paidAtDelivery()->create()` | Corrige ordem dos atributos derivados; CHECK permanece intacto |
| S:55–56 / filho 1 | `php artisan test --compact --filter='CreateServiceOrder\|AuthenticationTest\|AuthorizationTest'` | 61 passed, 472 assertions, `duration_ms: 7895`, exit 0 |
| S:55–56 / filho 2 | `npm run test -- --run resources/js/tests/CreateServiceOrder.test.jsx` | 12 testes: 9 passed, 3 failed, duração 11,17 s, exit 1 |
| S:57–60 | Lê modal; corrige `Chave Pix:`/`Contato:`, testa página antes do diálogo e inclui QRs | Muda assertions, não código do componente para satisfazer teste incorreto |
| S:61–62 | `git diff --check`, `vendor/bin/pint --dirty`, `composer run check` | Pint formata dois novos testes; 421 PHP/2182 assertions (`duration_ms: 28817`), 50 JS (18,92 s), Pint test e build 2,68 s; exit 0 |
| S:63–64 | Smoke HTTP tentativa 1 | `SyntaxError: unicodeescape`; Python não chega a executar o corpo; exit 1 |
| S:65–66 | Smoke HTTP tentativa 2, string PHP raw | Login validado, leitura JSON de Nova OS falha em `JSONDecodeError`; exit 1; script ainda não alcança POST da OS |
| S:67–68 | Smoke HTTP tentativa 3, versão Inertia obtida da página | Assertions funcionais passam; erro final na remoção do SQLite; exit 1 |
| S:69–70 | Limpeza do diretório exato do smoke e `git diff --check` | “SQLite descartavel removido”; exit 0. Servidor tinha `terminate/wait` no finally da tentativa anterior |
| S:71–76 | Ajuste de navegação e novos testes | Separa salvamento confirmado de erro de navegação; adiciona rollback aninhado, container rented sem OS e CSRF real |
| S:77–78 | `vendor/bin/pint --dirty && composer run check` | 424 PHP/2196 assertions (`duration_ms: 26577`), 51 JS (18,85 s), Pint e build 2,54 s, exit 0 |
| S:79–80 / filho 1 | `php artisan test --compact --filter=CreateServiceOrder` | 44 passed, 342 assertions, `duration_ms: 4476`, exit 0 |
| S:79–80 / filho 2 | `npm run test -- --run resources/js/tests/CreateServiceOrder.test.jsx` | 13 passed, 12,01 s, exit 0 |
| S:79–80 / filho 3; S:83–84 | Status/diffs e `git diff --check` | Sem erros de whitespace; entrega permanece não commitada |

Barras escapadas na tabela são apresentação Markdown; regex dos comandos históricos usa `|` sem o escape de apresentação. As execuções filtradas incluem subconjuntos e os gates os repetem; não somar como casos únicos. Build em “production” significa modo de build, não deploy.

**Smoke funcional, detalhe verificável:** S:67 contém assertions contra login/cookies/CSRF reais em porta loopback com banco temporário: GET/POST login, Nova OS, busca, POST sem token 419, POST válido 201, confirmação persistida, repetição 422, lista com uma OS; SQLite confirma contagens e `rented/Local ficticio`. S:68 imprime “Smoke HTTP local ... OK” antes de `PermissionError [WinError 32]` na saída do TemporaryDirectory. O `with sqlite3.connect(db)` cuida da transação, mas não fecha a conexão automaticamente; a variável ainda viva é causa provável do lock. S:70 confirma remoção posterior. Não foi feita nova execução integral com exit 0; há sucesso funcional + recuperação de limpeza, separadamente.

**Revisão e correção formal:** nenhum `task-M01-T12-revisao-*.md` escrito/lido, nenhum papel de revisor/corretor invocado, nenhuma aprovação técnica. Ajustes locais não consomem as três rodadas de correção previstas para outra etapa. A declaração inicial do usuário atual (“implementação concluída”) só foi hipótese; os testes, smoke e handoff sustentam conclusão da implementação, não do fluxo completo.

## 6. Git, dependências, aprovações e integração

### Baseline e gate observado

- S:11–12: `git status --short`, branch `main`, diff stat sem mudanças e `git ls-files` lista AGENTS/plano/registro.
- S:17–18: status limitado aos três caminhos vazio e `git ls-tree HEAD` comprova blobs no HEAD. Script falha na primeira comparação de uma linha de registro com saída de `git show` obtida em modo texto padrão.
- S:19–20: única correção relevante é decodificar bytes de `git show` como UTF-8; para cada uma das seis dependências o script exige linha no registro versionado, `concluída`, `merge-base --is-ancestor` e `cat-file -e` de relatório e revisão 1. Saída final é exit 0 e lista os seis hashes. Isso sustenta provável problema de encoding, não divergência real resolvida por alteração documental.
- S:21–22: cria `feat/cadastrar-ordem-de-servico` e só então atualiza registro para `em andamento`, após os gates. As convenções históricas autorizam criar branch com main/worktree limpos; não há troca sobre worktree sujo.
- HEAD inicial aparece abreviado em `git log -5` [S:14]: `782c6fc`, registro de integração da T11. Não se dispõe do hash completo desse HEAD na evidência e ele não contém a entrega nova da T12.

| Dependência | Integração referenciada e ancestralidade verificada em S:19–20 |
|---|---|
| M01-T04 | `01d5efd82d39bca06460fd350d494d7675b38fc7` |
| M01-T05 | `3328c2be5dd5094a0c6d173bf6af522dc3defb89` |
| M01-T07 | `c19a147dac9be4a8f438e17f9fdf67b89ba7ebf1` |
| M01-T09 | `bb404b1730b1609f7d6f506b4f39af73c0a504e5` |
| M01-T10 | `76c9bda178652a58d53ff85f140915d407deb4e4` |
| M01-T11 | `537b82fe734cbf3483c7c373c3114b5b3863f400` |

### O que isso não prova

`cat-file -e hash:caminho` prova presença do arquivo naquele snapshot, não quais alterações foram introduzidas pelo hash. Títulos de commit e registro são referências, não diffs funcionais. Não há `git show` de conteúdo funcional desses hashes nem comparação pai→commit na sessão. Portanto não são atribuídos arquivos funcionais individuais aos seis hashes. Testes e código existentes consumidos depois sustentam comportamento corrente, não autoria de alterações por hash.
Os hashes funcionais originais no registro não foram exigidos depois do squash; isso respeita a política histórica de permitir perdê-los. Não se buscou essas sessões nem se recuperou seu histórico externo.

Para M01-T12, nenhuma chamada executa `git add/commit/merge/push/squash`; o estado final continua com arquivos novos/modificados [S:84]. Hash funcional, hash de metadados e hash de integração da task: **não disponíveis**. A ausência de commit nesta sessão não certifica que jamais tenha havido integração depois dela.
Plano se diz aprovado; ato de aprovação anterior não foi observado. A invocação S:8 autoriza implementar. Não autoriza commits; revisão técnica e permissão para os dois commits ainda faltam. Publicação/merge teria autorização própria. Relatório S:81–82 e atualização S:83–84 não são commits nem integração.

## 7. Métricas — método, semântica e cobertura

### Seleção e deduplicação

Parser Python padrão sobre as 91 linhas; seleção de `type=message`/`message.role=assistant`. Todos os 39 eventos têm `usage`, `responseId`, modelo e API; 38 contêm uma chamada de ferramenta e um é resposta final. Sem respostas abortadas/erro no `stopReason` (38 `toolUse`, 1 `stop`), sem `responseId` ou IDs repetidos. Zero uso ausente significa cobertura completa **dos registros**, não certificação de fidelidade do provedor.
As chamadas internas de codemode são ferramentas, não respostas adicionais de modelo. Não possuem uso próprio na fonte; não duplicar o `usage` do wrapper para cada filho. As etapas abaixo são recortes analíticos de um único papel/task; não representam sessões/papéis separados.

O JSON preserva cada objeto `usage` com nomes/valores originais e seus campos de custo. `null` denota desconhecido, enquanto `cacheWrite: 0` é zero reportado em todas as respostas. Não há transcrição integral em `metricas.json`.

### Semântica: o observado versus interpretação

- Observado: `input`, `output`, `cacheRead`, `cacheWrite`, `reasoning`, `totalTokens`; `usage.cost` tem `input`, `output`, `cacheRead`, `cacheWrite`, `total`.
- Observado em 39/39: `totalTokens == input + output + cacheRead + cacheWrite`; `reasoning <= output`. Isso valida consistência aritmética, **não** a semântica de cobrança/cache/reasoning no provedor.
- Contagens entre registros não se comportam como um único acumulador simples: `input` diminui 19 vezes, `output` 16, `reasoning` 15. `cacheRead`/`totalTokens` nunca diminuem nesta trajetória. Aumento do contexto é compatível com uso por resposta; não há payload bruto do provedor para excluir outra semântica em campos específicos.
- Interpretação plausível, confirmação moderada: snapshots de uso associados a respostas. `input` sem cache e reasoning como subconjunto de output são hipóteses de confirmação baixa/moderada, baseadas em nomes/aritmética, sem validação externa. Não adicionar reasoning novamente nem somar totalTokens às categorias.
- As somas abaixo são dados derivados dos registros; interpretá-las como consumo exige confirmar que os campos sejam por resposta. Não representam tokens únicos do contexto — cache pode repetir o mesmo prefixo em muitas respostas.
- `usage.cost` é **custo reportado, não validado**: valores preservados, sem moeda identificada, tabela de preços, origem da configuração ou fatura. Não descartado nem chamado de cobrança real.
- `math.fsum` nas somas de custo usa ponto flutuante; resíduos binários ficam no JSON. Na síntese são apresentados com arredondamento explícito (`≈`).

### Por resposta

Campos são os nomes originais. `usage.cost.total` abaixo conserva o valor decodificado, inclusive resíduos. As demais categorias de custo por resposta e `responseId` completo estão no JSON.

| Local / evento | `input` | `output` | `cacheRead` | `cacheWrite` | `reasoning` | `totalTokens` | `usage.cost.total` |
|---|---:|---:|---:|---:|---:|---:|---:|
| S:9 / 2f8c704e | 7180 | 36 | 0 | 0 | 0 | 7216 | 0.014719999999999999 |
| S:11 / cf0e0c50 | 1170 | 167 | 7040 | 0 | 0 | 8377 | 0.0047139999999999994 |
| S:13 / fce3a779 | 11125 | 129 | 8064 | 0 | 20 | 19318 | 0.024346399999999997 |
| S:15 / ef699b9a | 7965 | 173 | 19072 | 0 | 0 | 27210 | 0.0195672 |
| S:17 / 52615fa0 | 10919 | 449 | 26880 | 0 | 10 | 38248 | 0.029016 |
| S:19 / f905cf17 | 3885 | 431 | 37632 | 0 | 21 | 41948 | 0.0158432 |
| S:21 / 8098e1d3 | 6381 | 615 | 41344 | 0 | 351 | 48340 | 0.023046399999999998 |
| S:23 / 7c3c2039 | 5562 | 55 | 47616 | 0 | 13 | 53233 | 0.0164356 |
| S:25 / c066d8f3 | 3316 | 964 | 52992 | 0 | 364 | 57272 | 0.021571200000000002 |
| S:27 / 643c84d0 | 1105 | 1026 | 56192 | 0 | 0 | 58323 | 0.0180892 |
| S:29 / d33662e2 | 1128 | 31 | 57216 | 0 | 0 | 58375 | 0.0082876 |
| S:31 / d91c0694 | 309 | 818 | 58240 | 0 | 0 | 59367 | 0.014622000000000003 |
| S:33 / 98ec72cc | 1023 | 937 | 58368 | 0 | 0 | 60328 | 0.017252800000000002 |
| S:35 / 1cf84301 | 1230 | 221 | 59264 | 0 | 190 | 60715 | 0.010596400000000002 |
| S:37 / d06f3f1e | 471 | 64 | 60288 | 0 | 0 | 60823 | 0.007610800000000001 |
| S:39 / 24dc047f | 171 | 136 | 60672 | 0 | 14 | 60979 | 0.0077692 |
| S:41 / aedc576a | 2324 | 2587 | 60672 | 0 | 74 | 65583 | 0.0365852 |
| S:43 / 30d8c1ad | 2758 | 4326 | 62848 | 0 | 171 | 69932 | 0.05506080000000001 |
| S:45 / 6cfe28c4 | 4546 | 43 | 65408 | 0 | 8 | 69997 | 0.0160628 |
| S:47 / be4d3bf8 | 1052 | 93 | 69760 | 0 | 48 | 70905 | 0.010010000000000002 |
| S:49 / e473e1db | 620 | 177 | 70656 | 0 | 9 | 71453 | 0.0100756 |
| S:51 / 9fc88665 | 313 | 1391 | 71168 | 0 | 0 | 72872 | 0.0216528 |
| S:53 / 0e92864b | 1599 | 3348 | 71296 | 0 | 116 | 76243 | 0.0438076 |
| S:55 / 100e6313 | 3561 | 132 | 72704 | 0 | 37 | 76397 | 0.0157124 |
| S:57 / 495d20f8 | 16067 | 46 | 76160 | 0 | 11 | 92273 | 0.040209999999999996 |
| S:59 / 995d2a87 | 1005 | 405 | 92032 | 0 | 35 | 93442 | 0.015263200000000003 |
| S:61 / 08036e24 | 542 | 86 | 92928 | 0 | 37 | 93556 | 0.0112368 |
| S:63 / 7426efc2 | 1283 | 2363 | 93312 | 0 | 1034 | 96958 | 0.0355272 |
| S:65 / 295cbb6f | 2690 | 1280 | 94464 | 0 | 22 | 98434 | 0.027626400000000002 |
| S:67 / 6264da91 | 1650 | 1364 | 97024 | 0 | 168 | 100038 | 0.026642400000000004 |
| S:69 / 59927114 | 2070 | 205 | 98560 | 0 | 61 | 100835 | 0.016045999999999998 |
| S:71 / 9b7f4112 | 1319 | 776 | 100480 | 0 | 516 | 102575 | 0.020446000000000002 |
| S:73 / eee1ef23 | 972 | 827 | 101632 | 0 | 99 | 103431 | 0.0203772 |
| S:75 / fa037400 | 1059 | 366 | 102400 | 0 | 0 | 103825 | 0.016018 |
| S:77 / 34c2eb12 | 557 | 177 | 103296 | 0 | 38 | 104030 | 0.013213600000000002 |
| S:79 / 25c9f2c8 | 2519 | 674 | 103680 | 0 | 516 | 106873 | 0.022146 |
| S:81 / af94f1f7 | 2539 | 2689 | 106112 | 0 | 81 | 111340 | 0.042579200000000005 |
| S:83 / d741eb88 | 2829 | 246 | 108544 | 0 | 100 | 111619 | 0.0189724 |
| S:85 / 0c300f2a | 648 | 105 | 111232 | 0 | 0 | 111985 | 0.0134692 |

### Agregados por etapa analítica

Limites são linhas de respostas, inclusivos. Ferramentas subsequentes pertencem ao contexto da etapa, mas seus resultados não têm `usage` adicional. Etapas contíguas na seleção de respostas não são fatias de tempo ativo.

| Etapa / linhas assistant | N | `input` | `output` | `cacheRead` | `cacheWrite` | `reasoning` | `totalTokens` | Σ`usage.cost.total` ≈ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Descoberta/gates, S:9–23 | 8 | 54187 | 2055 | 187648 | 0 | 415 | 243890 | 0.1476888 |
| Construção inicial, S:25–45 | 11 | 18381 | 11153 | 652160 | 0 | 821 | 681694 | 0.2135080 |
| Testes/ajustes/gate inicial, S:47–61 | 8 | 24759 | 5678 | 616704 | 0 | 293 | 647141 | 0.1679684 |
| Smoke/limpeza, S:63–69 | 4 | 7693 | 5212 | 383360 | 0 | 1285 | 396265 | 0.1058420 |
| Endurecimento/revalidação, S:71–79 | 5 | 6426 | 2820 | 511488 | 0 | 1169 | 520734 | 0.0922008 |
| Relatório/handoff, S:81–85 | 3 | 6016 | 3040 | 325888 | 0 | 181 | 334944 | 0.0750208 |
| **Total** | **39** | **117462** | **29958** | **2677248** | **0** | **4164** | **2824668** | **0.8022288** |

Fórmulas: `sum(usage[campo])` sobre resposta única; `math.fsum(usage.cost[campo])` para custos. Soma aritmética adicional `input + cacheRead = 2794710`. Não somar `reasoning` nem repetir `totalTokens` nas categorias.
Modelo/papel/task são constantes nessas 39 respostas; não há como decompor uso em “revisor”, “corretor” ou custo de cada arquivo/teste. Revisor não observado → consumo **não disponível**, não zero medido.
O grande output de DOM/QR no erro de S:56 antecede `input: 16067` em S:57; associação temporal é observável, contribuição exclusiva do DOM não é separável. Não atribuído todo esse input ao erro nem estimada economia.

### Reprodução passiva das principais métricas

Trecho ilustrativo para auditar os cálculos; apenas lê JSON, não executa conteúdo armazenado. `fonte` é o caminho S, não qualquer diretório de sessões.

```python
import json, math
from pathlib import Path
from collections import Counter
from datetime import datetime
linhas = Path(fonte).read_text(encoding='utf-8').splitlines()
eventos = [json.loads(linha) for linha in linhas]
respostas = [(n, e) for n, e in enumerate(eventos, 1)
             if e.get('message', {}).get('role') == 'assistant']
ids = [e['message']['responseId'] for n, e in respostas]
assert len(ids) == len(set(ids)) == 39
campos = ['input', 'output', 'cacheRead', 'cacheWrite',
          'reasoning', 'totalTokens']
somas = {k: sum(e['message']['usage'][k] for n, e in respostas)
         for k in campos}
custos = {k: math.fsum(e['message']['usage']['cost'][k]
                      for n, e in respostas)
          for k in ['input', 'output', 'cacheRead', 'cacheWrite', 'total']}
filhos = Counter(e.get('parentId') for e in eventos[1:]
                 if e.get('parentId') is not None)
assert not any(n > 1 for n in filhos.values())
def instante(n):
    return datetime.fromisoformat(eventos[n-1]['timestamp'].replace('Z', '+00:00'))
decorrido = (instante(85) - instante(8)).total_seconds()
```

## 8. Tempo e durações de ferramentas

### Significado dos timestamps

`event.timestamp` é ISO UTC no registro persistido. `message.timestamp` é inteiro em milissegundos epoch; nas mensagens assistant tende a estar próximo do resultado anterior e precede o timestamp externo. Sem especificação do ciclo de vida nesta fonte, não se certifica que um marque solicitação de API ou outro término de geração. O JSON retém ambos e calcula `internal_to_envelope_seconds` apenas como diferença de registros, **não latência confirmada**.

| Medida | Extremos identificados | Segundos | Interpretação |
|---|---|---:|---|
| Pedido → final | S:8 18:49:19.374Z → S:85 19:04:37.079Z | 917.705 | Janela observada de execução/handoff, não tempo ativo |
| Pedido → primeiro assistant | S:8 → S:9 18:49:25.341Z | 5.967 | Primeira resposta com tool call, não primeira mensagem explicativa |
| Status em andamento → aguardando revisão | S:22 18:50:32.765Z → S:84 19:04:32.788Z | 840.023 | Janela entre resultados das transições, não tempo de codificação |
| Smoke: primeiro erro → limpeza | S:64 18:59:29.647Z → S:70 19:00:39.338Z | 69.691 | Inclui intervalos entre tentativas e raciocínio/geração não isolados |
| Cabeçalho → último metadado | S:1 06/10 18:48:46.681Z → S:91 11/11 19:10:45.751Z | 3111719.070 | Amplitude do arquivo; **não duração da task** |

Espera por usuário: zero pedidos intermediários observados, nenhum intervalo solicitação→resposta; duração em segundos **não disponível**. Tempo ativo, tempo ocioso e duração exata de geração **não disponíveis**. Não usar intervalo entre chamadas como proxy de raciocínio ativo.

### Ferramentas: medidas distintas

38 chamadas de topo: 11 codemode, 8 bash, 8 write, 6 read e 5 edit. Todas têm par chamada/resultado, registrado em `metricas.json#/time/tool_call_result_intervals` com extremos e IDs. Só as 11 wrappers têm `Wall time ... seconds` reportado em texto; 57 filhos têm `details.calls[].durationMs`. As outras 27 chamadas de topo não possuem duração explícita equivalente: têm intervalo de eventos, não zero.

`details.calls` e `nestedCalls.calls` repetem os mesmos IDs de filhos, com arredondamentos e pequenas diferenças de contabilização (ex.: S:18: 678,1528 ms versus 677 ms). Ambos preservados no JSON, mas somente `details.calls` usado na soma. Um resultado externo `isError: false` ou Promise `fulfilled` não garante sucesso dos filhos: S:18 e S:56 contêm falhas internas/exit codes não zero. A auditoria usou os resultados internos, não só a flag externa.

| Par de eventos | Intervalo externo (s) | Wall time da wrapper reportado (s) | Filhos relevantes (ms, `details.calls`) |
|---|---:|---:|---|
| S:11→12 | 0.534 | 0.5 | bash 430.6725 + cinco leituras em paralelo |
| S:15→16 | 0.132 | 0.1 | seis leituras em paralelo |
| S:17→18 | 0.814 | 0.8 | bash com erro 678.1528 + leituras |
| S:19→20 | 2.077 | 2.1 | bash 1705.4757 + leituras |
| S:21→22 | 0.778 | 0.8 | bash 620.9840 + leituras |
| S:33→34 | 0.249 | 0.2 | oito edições sequenciais |
| S:39→40 | 0.515 | 0.5 | leituras e bash 323.9295 |
| S:55→56 | 14.634 | 14.6 | PHP 10284.9426 e JS 14531.5657 em paralelo |
| S:61→62 | 65.114 | 65.1 | bash/gate 65020.2257 |
| S:77→78 | 60.337 | 60.3 | três leituras sequenciais e bash/gate 60156.1111 |
| S:79→80 | 15.649 | 15.6 | PHP 6984.4864, JS 15542.8542, Git 536.6994 em paralelo |

Soma calculada dos 57 `durationMs` = **177949.0288 ms**, carga agregada parcial dos filhos; não inclui as 27 ferramentas sem duração explícita. Não é tempo decorrido, não somar wrappers, mirrors, PHP/Vitest/build aninhados ou etapas em paralelo a esse valor. Na dupla de S:56, 10,285 s + 14,532 s de filhos claramente não representam 14,634 s de janela externa.
Durações das suítes (`duration_ms`, `Duration`, build) são reportadas pelas ferramentas e estão na seção 5; diferentes de runtime de processo bash e wrapper. Vitest também reporta parcelas transform/setup/import/tests/environment que podem se sobrepor; não somadas como duração.

## 9. Lacunas e cautelas para consolidação

- Confiança da entrega local é alta pelas evidências positivas e execução verde; não há certificação de cobertura exaustiva, review independente ou produção pronta.
- Aprovação anterior do plano e revisões das dependências são referências persistidas, não eventos desta sessão. Não presumir etapas fora dela, nem confundir sua ausência com falha do fluxo.
- Não há prova funcional individual por hash das dependências; não há hash de commit da M01-T12. Trabalho sujo final não é integração.
- `plan` histórica não foi carregada integralmente; só é possível avaliar o artefato e comparar o desenho atual da skill, sem inferir versão/autoria.
- Truncamentos tiveram recuperação histórica parcial. A recuperação atual não deve ser creditada ao agente histórico; os recortes preservados são explicitamente analíticos.
- Erros auxiliares adicionais: leitura de `src/resources/js/bootstrap.js` retorna ENOENT [S:36]; `rg` sem correspondência, encadeado com `&&`, interrompe descoberta [S:37–38]; recupera por leituras direcionadas [S:39–40]. Problemas de descoberta sem impacto funcional demonstrado; não geraram regra candidata própria.
- Sem telemetria bruta de provedor, preços/moeda, tempo ativo, espera humana medida ou benchmark comparativo. Nenhuma economia causal calculada.
- Origens consideradas: especificação/planejamento (A01 favorável, nenhum defeito de recorte provado), skill (cumprimento claro no handoff, nenhuma omissão causal provada), agente (scripts/assertions), harness/ferramenta (truncamento e mirrors), ambiente (encoding/lock Windows), mudança externa (não demonstrada), causa não determinada (suficiência do gate Git e impactos funcionais dos trechos omitidos).
- As seis candidatas/acertos do relatório são hipóteses locais com casos de teste; nenhuma mudança foi aprovada/aplicada às skills. Este segundo caso valida o formato para entrega/testes e ausência de revisão, não para achados de um revisor efetivamente executado.

# Plano de implementação — etapas 5 a 8

> **Status:** etapas 5 a 8 planejadas — ainda não iniciadas; scaffold da etapa 4 concluído em `src/`.
>
> **Escopo:** da instalação do Laravel Breeze/Inertia/React até a entrega das fatias funcionais, testes e preparação técnica para homologação.
>
> **Pré-condição:** a etapa 4 já criou o projeto Laravel em `src/`, sem substituir `AGENTS.md`, `.agents/` ou `docs_sistema_recolhe/` na raiz do repositório.
>
> **Fontes de verdade:** [[escopo]], [[regras-de-negocio]], [[backlog]], [[uc01-cadastrar-os]], [[uc02-devolver-container]], [[uc03-gerenciar-pagamento-cobranca]], [[arquitetura-hld]], [[modelo-de-dados]], [[estrategia-de-testes]], [[prototipo-baixa-fidelidade]], [[prototipo-baixa-fidelidade-uc03-pagamento-cobranca]] e ADRs 0001–0005.

## 1. Objetivo

Implementar o primeiro marco do Recolhe como monólito Laravel com Inertia.js e React, usando SQLite, autenticação por sessão, regras de negócio no servidor, impressão no navegador e testes automatizados para as invariantes críticas.

Ao final deste plano, a aplicação deverá permitir:

- autenticação e autorização de `admin` e da única credencial compartilhada `driver`;
- cadastro e impressão de OS pelo caminhoneiro;
- consulta das OS do dia;
- controle de containers, clientes e configurações;
- cálculo de prazo, diária extra e total;
- devolução manual e reconciliação automática por prazo;
- gestão de pagamentos e cobranças;
- backup do SQLite e verificação de saúde;
- homologação funcional, operacional e física conforme [[estrategia-de-testes]].

## 2. Limites globais — o que não deve ser alterado durante a implementação

Qualquer necessidade de mudar os itens abaixo interrompe a task afetada e exige atualização prévia dos requisitos ou um novo ADR.

### 2.1 Arquitetura

- Não separar frontend e backend em aplicações diferentes.
- Não criar API REST pública para o primeiro marco.
- Não substituir Laravel, Inertia.js, React ou SQLite sem ADR.
- Não trocar SQLite por MySQL; o fallback previsto é reavaliar a hospedagem e registrar nova decisão.
- Não introduzir microsserviços, filas, Redis, Docker obrigatório, PWA, modo offline, Web Bluetooth, CI/CD ou suíte E2E neste marco.
- Não introduzir camada de repositórios genérica sem necessidade comprovada; Eloquent e serviços/actions são suficientes.

### 2.2 Regras de negócio

- Não alterar as regras de prazo, domingo, diária extra, pagamento ou devolução.
- Não persistir total atualizado, quantidade de diárias, períodos decorridos, badges de cobrança ou QR codes.
- Não usar `float` para valores monetários; persistência e cálculos usam centavos inteiros.
- Não permitir duas OS ativas para o mesmo container.
- Não permitir mais de uma credencial com papel `driver`.
- Não diferenciar os dois caminhoneiros nem atribuir a OS a um deles.
- Não automatizar confirmação de Pix e não integrar PSP/webhook.
- Não criar reversão de pagamento no primeiro marco.
- Não transformar pagamento em retirada, correção de pagamento na entrega e devolução manual em uma ação genérica; os efeitos são diferentes.
- Não criar job de cobrança: os badges são calculados no carregamento do painel.

### 2.3 Dados

- Manter identificadores de domínio em inglês e `snake_case`.
- Manter textos de interface em português.
- Manter `America/Sao_Paulo` como fuso único de negócio.
- Não adicionar `created_at`/`updated_at` às tabelas de domínio.
- Não adicionar unicidade ao nome do cliente.
- Não apagar histórico por cascata. FKs de OS para cliente e container devem restringir exclusão.
- Não armazenar banco, `.env`, senha, cookie, chave SMTP ou backup no Git.
- Não alterar migrations já executadas em ambiente compartilhado; depois do primeiro deploy, correções de schema exigem novas migrations.

### 2.4 Interface e impressão

- Não disponibilizar impressão antes do commit da OS.
- Não registrar tentativa, sucesso, falha ou quantidade de impressões.
- Não mostrar “Impresso com sucesso”.
- Não bloquear ou desfazer a OS por falha de impressão.
- Não expor histórico anterior nem backoffice ao `driver`.
- Não implementar telas administrativas sem wireframe/fluxo validado quando a interação puder alterar estado financeiro ou do container.

### 2.5 Documentação existente

- Não reescrever requisitos para acomodar uma implementação mais fácil.
- Não usar documentos em `_archive/` como fonte de verdade.
- Não modificar arquivos já alterados pelo usuário sem revisar o diff e obter alinhamento.
- Divergências encontradas entre regra, modelo, protótipo e teste devem ser resolvidas na documentação antes do código correspondente.

## 3. Tecnologias e convenções de implementação

| Área | Decisão |
|---|---|
| Backend | Laravel na versão estável escolhida na etapa 4 |
| Autenticação | Laravel Breeze, sessão web e CSRF |
| Frontend | Inertia.js + React + Vite |
| Linguagem frontend | JavaScript/JSX; não migrar para TypeScript dentro deste plano sem decisão explícita |
| Banco | SQLite |
| Testes backend | PHPUnit por `php artisan test` |
| Testes frontend | Vitest + React Testing Library, somente onde houver lógica relevante |
| Formatação PHP | Laravel Pint |
| Dados de teste | Factories; testes não dependem de seeders |
| Datas em testes | Relógio congelado e `America/Sao_Paulo` |
| Organização backend | controllers finos, Form Requests, policies/middleware, actions transacionais e serviços puros de domínio |
| Valores monetários | inteiros em centavos e conversor decimal estrito |
| Build de produção | Vite local; `public/build` enviado no deploy |

## 4. Ordem e dependências

```text
Etapa 5 — Breeze/Inertia/React
    ↓
Etapa 6 — SQLite local e de testes
    ↓
Etapa 7 — migrations, models, factories e seeders
    ↓
Etapa 8.0 — base de testes e organização interna
    ↓
Etapa 8.1 — serviços puros de domínio
    ↓
Etapa 8.2 — autenticação e autorização completas
    ↓
Etapa 8.3 — cadastro de OS e clientes
    ↓
Etapa 8.4 — operação diária do caminhoneiro
    ↓
Etapa 8.5 — containers e devoluções
    ↓
Etapa 8.6 — pagamentos e cobranças
    ↓
Etapa 8.7 — administração e configurações
    ↓
Etapa 8.8 — impressão
    ↓
Etapa 8.9 — saúde, backup e operação
    ↓
Etapa 8.10 — estabilização e homologação
```

A geração do payload de impressão pode avançar em paralelo depois que o formato dos dados da confirmação da OS estiver estável. A homologação física depende da impressora e dos celulares reais.

---

# Etapa 5 — Instalar e preparar Breeze, Inertia.js e React

## Task 5.1 — Verificar a base criada na etapa 4

### Fazer

- Confirmar que o projeto Laravel está em `src/`.
- Registrar as versões efetivamente usadas de PHP, Composer, Laravel, Node.js e npm.
- Verificar compatibilidade entre a versão do Laravel e a versão do Breeze.
- Confirmar que `composer.lock` e o lockfile npm serão versionados.
- Verificar que o scaffold não substituiu `AGENTS.md`, `.agents/` ou `docs_sistema_recolhe/`.
- Executar o boot básico do Laravel antes de instalar novos pacotes.

### Não alterar

- Não atualizar dependências para versões maiores apenas por estarem disponíveis.
- Não reorganizar a documentação dentro da aplicação.
- Não iniciar regras de negócio nesta task.

### Entregáveis

- Projeto Laravel inicial executável.
- Versões travadas nos lockfiles.
- `.env.example` presente, sem segredos.
- Registro das versões no README técnico do projeto.

### Critério de conclusão

- A página inicial do Laravel abre localmente e nenhum arquivo preexistente do repositório foi perdido.

## Task 5.2 — Instalar Breeze com Inertia e React

### Fazer

- Instalar Laravel Breeze como dependência de desenvolvimento.
- Executar o instalador no flavor Inertia + React.
- Instalar dependências npm.
- Confirmar a estrutura de páginas, layouts, middleware Inertia e Vite.
- Executar o build de desenvolvimento e o build de produção.

### Não alterar

- Não selecionar API, Blade, Livewire ou Vue.
- Não criar uma SPA separada.
- Não adicionar biblioteca global de estado sem caso concreto.
- Não implementar TypeScript como parte desta instalação.

### Entregáveis

- Breeze, Inertia.js e React instalados.
- `composer.json`, `composer.lock`, `package.json` e lockfile npm atualizados.
- Assets Vite compilando sem erro.
- Página React servida pelo Laravel via Inertia.

### Critério de conclusão

- `npm run build` termina com sucesso e uma página Inertia é renderizada pelo Laravel.

## Task 5.3 — Reduzir o scaffold de autenticação ao escopo aprovado

### Fazer

- Manter login, logout, proteção CSRF, limitação de tentativas e opção “Lembrar de mim”.
- Remover rotas, controllers, requests, links e páginas de:
  - registro público;
  - recuperação de senha por e-mail;
  - redefinição por token enviado por e-mail;
  - verificação de e-mail.
- Deixar a adaptação final de `email` para `username` para a Task 8.2, depois do schema definitivo.
- Preparar layouts separados para área operacional e backoffice, sem ainda implementar todas as telas.

### Não alterar

- Não criar autenticação própria.
- Não usar JWT, token de API ou autenticação no navegador fora da sessão Laravel.
- Não manter rotas ocultas de registro/recuperação “para usar depois”.

### Entregáveis

- Superfície de autenticação reduzida.
- Rotas fora de escopo removidas.
- Layout operacional e layout administrativo básicos.
- Testes de rota garantindo ausência dos fluxos removidos, finalizados na Task 8.2.

### Critério de conclusão

- Apenas login e logout permanecem acessíveis entre os fluxos públicos de autenticação.

## Task 5.4 — Preparar a ferramenta de testes frontend

### Fazer

- Instalar Vitest, React Testing Library, DOM matchers e `user-event`.
- Configurar ambiente DOM para componentes React.
- Criar `npm run test` para execução não interativa, `npm run test:watch` para uso durante o desenvolvimento e manter `npm run build` para o build Vite.
- Ampliar `composer run check` para executar, nesta ordem, testes backend, Pint em modo de verificação, testes frontend não interativos e build Vite.
- Atualizar [[fluxo-de-desenvolvimento]] com o comando da suíte frontend e seu uso, caso o script não seja autoexplicativo; manter [[convencoes-de-desenvolvimento]] e `AGENTS.md` coerentes com o gate oficial.
- Criar um teste mínimo de renderização para validar a configuração.

### Não alterar

- Não instalar Playwright, Cypress ou Laravel Dusk.
- Não buscar cobertura total de componentes visuais.
- Não testar detalhes internos do Inertia ou de bibliotecas externas.

### Entregáveis

- Configuração do Vitest.
- Setup da React Testing Library.
- Um teste mínimo verde.
- Scripts npm documentados em [[fluxo-de-desenvolvimento]].
- `composer run check` atualizado como gate único com backend, formatação, frontend e build.

### Critério de conclusão

- A suíte frontend e `npm run build` executam separadamente sem erro, e `composer run check` executa todos os gates sem interação.

## Gate da etapa 5

- Breeze/Inertia/React instalados.
- Fluxos de autenticação fora de escopo removidos.
- Build Vite verde.
- Teste frontend mínimo verde.
- Nenhuma regra de domínio implementada prematuramente.

---

# Etapa 6 — Configurar SQLite local e de testes

## Task 6.1 — Configurar o banco local

### Fazer

- Habilitar `sqlite3` e `pdo_sqlite` no PHP local.
- Usar `database/database.sqlite` como arquivo local padrão.
- Configurar `DB_CONNECTION=sqlite` no `.env` local e no `.env.example`.
- Manter caminho relativo/portável sempre que o Laravel permitir.
- Confirmar foreign keys ativas.
- Configurar `APP_TIMEZONE=America/Sao_Paulo` ou valor equivalente consumido por `config/app.php`.
- Validar leitura e escrita simples pelo Laravel.

### Não alterar

- Não apontar desenvolvimento para MySQL.
- Não versionar o arquivo SQLite local.
- Não usar caminho absoluto pessoal no `.env.example`.
- Não depender do timezone do computador ou da hospedagem para regras de negócio.

### Entregáveis

- SQLite local funcional.
- `.gitignore` protegendo bancos, arquivos temporários e backups.
- `.env.example` documentando conexão e fuso, sem credenciais reais.
- Verificação local de `pdo_sqlite` e `sqlite3`.

### Critério de conclusão

- O Laravel conecta, cria uma tabela temporária de teste e executa leitura/escrita pelo PDO SQLite.

## Task 6.2 — Configurar SQLite para PHPUnit

### Fazer

- Configurar a suíte comum para SQLite em memória.
- Garantir `APP_ENV=testing`, cache e filas em modo síncrono/falso conforme necessário.
- Desabilitar envio real de e-mail durante testes.
- Fixar o fuso de teste em `America/Sao_Paulo`.
- Preparar uma configuração auxiliar de SQLite em arquivo temporário para:
  - concorrência com conexões distintas;
  - backup por `VACUUM INTO`;
  - comportamento específico de arquivo;
  - testes em que memória não reproduza produção.
- Garantir limpeza dos arquivos temporários após cada teste.

### Não alterar

- Não fazer testes dependerem do banco local do desenvolvedor.
- Não executar testes destrutivos no arquivo de desenvolvimento.
- Não usar seed de produção como pré-condição da suíte.

### Entregáveis

- Configuração PHPUnit com SQLite em memória.
- Helper/configuração para SQLite temporário em arquivo.
- Teste de conexão em memória e teste de conexão por arquivo.

### Critério de conclusão

- `php artisan test` consegue criar e destruir seu próprio schema sem tocar no banco local.

## Task 6.3 — Fixar política de datas, horas e sessões

### Fazer

- Centralizar o fuso da aplicação em `America/Sao_Paulo`.
- Definir que actions de domínio fornecem explicitamente `started_at`, `paid_at` e `returned_at` no fuso de negócio.
- Não depender do `CURRENT_TIMESTAMP` UTC do SQLite para timestamps de negócio.
- Preparar uso de sessão em banco para permitir invalidação das sessões do `driver`; a troca definitiva de driver ocorre após a migration de `session` na etapa 7.
- Definir duração de 30 dias para “Lembrar de mim”.

### Não alterar

- Não converter silenciosamente os timestamps de negócio para UTC.
- Não misturar hora do servidor, hora do navegador e hora do banco nos cálculos.
- Não usar tempo real em testes de fronteira; o relógio deve ser congelado.

### Entregáveis

- Configuração central de timezone.
- Política técnica de timestamps refletida no código de configuração.
- Configuração preparada para sessões persistidas em banco.

### Critério de conclusão

- Um teste congelado produz o mesmo horário de negócio independentemente do timezone da máquina que executa a suíte.

## Gate da etapa 6

- SQLite local funcionando.
- SQLite em memória e temporário funcionando nos testes.
- Foreign keys habilitadas.
- Timezone controlado.
- Banco e backups ignorados pelo Git.

---

# Etapa 7 — Criar migrations, models, factories e seeders

## Task 7.1 — Fechar o mapeamento físico do schema

### Fazer

- Transformar [[modelo-de-dados]] em uma lista exata de tabelas, colunas, tipos, nulabilidade, defaults, checks, FKs e índices.
- Usar os nomes lógicos definidos: `user`, `container`, `customer`, `configuration` e `service_order`; configurar `$table` nos models quando necessário.
- Adicionar somente estruturas técnicas exigidas pelo framework:
  - `remember_token` em `user`;
  - tabela `session` para invalidação de sessões;
  - coluna auxiliar/indexada de busca normalizada do cliente, permitida pelo modelo lógico, sem unicidade.
- Definir FKs de OS com exclusão restrita.
- Definir nomes explícitos para checks e índices quando o SQLite/Laravel suportar.
- Definir índices de consulta para status, datas, pagamentos e busca de cliente sem remover os índices de integridade.

### Não alterar

- Não mudar a semântica das entidades.
- Não pluralizar ou renomear tabelas silenciosamente.
- Não adicionar tabela de notificação, impressão, diária extra ou total calculado.
- Não criar tabela genérica chave-valor para configuração.
- Não adicionar `email` obrigatório, `password_reset_tokens`, jobs ou cache em banco sem necessidade aprovada.

### Entregáveis

- Mapa físico revisado dentro da implementação das migrations.
- Lista de índices e constraints que será validada pelos testes da Task 7.5.
- Qualquer divergência necessária registrada antes de gerar a migration correspondente.

### Critério de conclusão

- Cada coluna e constraint possui origem rastreável em [[modelo-de-dados]], ADR-0005 ou necessidade operacional explícita.

## Task 7.2 — Criar migrations

### Fazer

Criar migrations reversíveis para:

1. `user`;
2. `session`;
3. `container`;
4. `customer`;
5. `configuration`;
6. `service_order`;
7. índices únicos parciais e índices auxiliares, se não puderem ficar nas migrations das tabelas.

Implementar no banco:

- `container.number` único e limitado a 1–40;
- estados permitidos para container, OS, pagamento e papel;
- singleton de `configuration` com `id = 1`;
- faixas de valores monetários entre 1 e 9.999.999 centavos;
- coerência entre rampa e `ramp_value_cents`;
- coerência entre pagamento, método, momento e `paid_at`;
- `at_delivery → paid_at = started_at`;
- `at_pickup → status = returned`;
- coerência entre devolução e `returned_at`;
- índice único parcial de uma OS ativa por container;
- índice único parcial de no máximo um `driver`;
- FKs e índices de consulta.

### Não alterar

- Não confiar somente na validação da aplicação para RN24 ou limite de `driver`.
- Não usar `ENUM` incompatível com uma futura migração para PostgreSQL sem encapsular os valores de forma clara.
- Não usar cascade delete para apagar OS ao remover cliente/container.
- Não incluir dados reais de produção nas migrations.
- Não depender de default UTC do SQLite para timestamps de negócio.

### Entregáveis

- Migrations completas, com `up()` e `down()`.
- Schema criado por `migrate:fresh`.
- Rollback validado em ambiente local descartável.
- Índices parciais criados com nomes explícitos.

### Critério de conclusão

- `migrate:fresh`, rollback e nova aplicação das migrations funcionam em SQLite vazio.

## Task 7.3 — Criar enums e models Eloquent

### Fazer

- Criar backed enums PHP para:
  - papel do usuário;
  - status do container;
  - status, método e momento do pagamento;
  - status da OS.
- Criar models `User`, `Container`, `Customer`, `Configuration` e `ServiceOrder`.
- Configurar tabela singular, casts, relações e `$timestamps = false` nas entidades de domínio.
- Ocultar senha e remember token em serialização.
- Implementar scopes somente para consultas estáveis e claras, como OS ativas, pendentes e do dia.
- Manter cálculos financeiros e transições fora dos models quando envolverem múltiplas entidades.

### Não alterar

- Não colocar transações complexas em observers ou eventos implícitos.
- Não colocar cálculo de diária no controller, componente React ou accessor que consulte o relógio sem parâmetro.
- Não criar setters que arredondem silenciosamente dinheiro.
- Não permitir mass assignment irrestrito de status e campos financeiros vindos do navegador.

### Entregáveis

- Enums de domínio.
- Models com relações e casts.
- Testes básicos de relações/casts quando agregarem comportamento relevante.

### Critério de conclusão

- Os models representam o schema sem esconder transições críticas em efeitos automáticos.

## Task 7.4 — Criar factories e seeders

### Fazer

- Criar factories para usuário, container, cliente, configuração e OS.
- Oferecer estados válidos nas factories, por exemplo:
  - OS pendente ativa;
  - paga na entrega;
  - paga na retirada e devolvida;
  - devolvida manualmente e pendente.
- Criar `ContainerSeeder` idempotente para os números 1–40.
- Garantir que nova execução não duplique nem sobrescreva indevidamente containers existentes.
- Usar factories, e não seeders, como base dos testes.
- Deixar dados reais de admin, Pix e WhatsApp para inicialização segura posterior.

### Não alterar

- Não usar senhas, chave Pix, telefone ou nomes reais no repositório.
- Não fazer `ContainerSeeder` resetar status/localização de containers existentes.
- Não criar automaticamente um segundo `driver`.
- Não tornar testes dependentes da ordem de execução de seeders.

### Entregáveis

- Factories com estados semanticamente válidos.
- `ContainerSeeder` idempotente.
- Testes de criação 1–40 e reexecução sem efeitos destrutivos.

### Critério de conclusão

- A suíte consegue montar qualquer cenário da [[estrategia-de-testes]] sem dados globais compartilhados.

## Task 7.5 — Testar o schema e as constraints

### Fazer

- Testar diretamente no SQLite, contornando validações HTTP, todas as invariantes P0 do schema.
- Cobrir:
  - limites e unicidade dos containers;
  - singleton de configuração;
  - valores monetários;
  - estados coerentes de rampa, pagamento e devolução;
  - uma OS ativa por container;
  - no máximo um `driver`;
  - proteção das FKs;
  - índices parciais em banco SQLite real.
- Executar o cenário de disputa do mesmo container com arquivo temporário e conexões distintas.

### Não alterar

- Não considerar teste Feature de formulário como substituto do teste da constraint.
- Não remover uma constraint porque ela torna a factory ou o teste mais difícil.
- Não simular SQLite com outro SGBD.

### Entregáveis

- Testes de integração do schema.
- Evidência automatizada de RN24 e limite de `driver`.
- Migrations corrigidas até todos os testes de integridade ficarem verdes.

### Critério de conclusão

- Todos os cenários de schema P0 em [[estrategia-de-testes]] passam usando SQLite.

## Gate da etapa 7

- Schema completo e reversível.
- Models, enums, factories e seeder disponíveis.
- Constraints P0 comprovadas no banco.
- `migrate:fresh --seed` cria exatamente 40 containers sem dados sensíveis.
- Nenhum valor derivável foi transformado em coluna.

---

# Etapa 8 — Implementar por fatias verticais

## Task 8.0 — Preparar a estrutura interna e o ciclo TDD

### Fazer

- Organizar o backend com responsabilidades explícitas:
  - `Http/Controllers` para adaptação HTTP;
  - `Http/Requests` para validação de entrada;
  - policies/middleware para autorização;
  - `Actions` para comandos transacionais;
  - `Domain` ou `Services` para cálculos puros e regras reutilizadas.
- Definir o ciclo para cada comportamento crítico: teste falhando, implementação mínima, refatoração.
- Configurar helpers de relógio congelado, factories e assertions de estado.
- Mapear os testes implementados aos IDs de [[estrategia-de-testes]] pelo nome ou comentário, sem duplicar a regra no código.
- Revisar e manter `composer run check` como gate padronizado de qualidade, cobrindo:
  - testes PHP;
  - testes JavaScript;
  - build Vite;
  - Pint em modo de verificação.
- Atualizar [[fluxo-de-desenvolvimento]] sempre que um comando necessário para executar ou validar a aplicação mudar.

### Não alterar

- Não criar abstrações genéricas antes de existir repetição real.
- Não mover autoridade de negócio para React.
- Não escrever toda a suíte antecipadamente sem implementar fatias utilizáveis.
- Não medir sucesso somente por cobertura percentual.

### Entregáveis

- Estrutura de pastas aplicada.
- Helpers de teste.
- Comandos de qualidade documentados.
- Primeiro teste TDD demonstrando o padrão.

### Critério de conclusão

- Uma regra simples percorre o ciclo teste vermelho → verde → refatoração e todas as ferramentas executam localmente.

## Task 8.1 — Implementar serviços puros de domínio

### Fazer

Aplicar TDD para implementar:

- normalização de nome e endereço;
- normalização auxiliar para busca sem caixa e acentos;
- conversão monetária estrita entre texto e centavos, rejeitando mais de duas casas;
- cálculo dos períodos válidos de 24 horas com a regra do domingo;
- instante exato de encerramento do 6º período válido;
- quantidade de diárias extras;
- composição do total;
- congelamento do total em `returned_at`;
- zero diária extra para pagamento na entrega;
- badge recorrente de cobrança por períodos exatos de sete dias, contando domingos.

As funções devem receber explicitamente início, limite de cálculo, valores e relógio; não devem consultar banco, sessão ou `now()` internamente.

### Não alterar

- Não usar dias-calendário no lugar de períodos exatos de 24 horas.
- Não aplicar RN05 aos badges de cobrança.
- Não arredondar dinheiro.
- Não persistir resultados derivados.
- Não duplicar fórmulas em controllers, queries e componentes React.

### Entregáveis

- Serviços puros de prazo, total e cobrança.
- Conversor monetário e normalizador de texto.
- Testes unitários das seções 4 e dos badges da seção 7 de [[estrategia-de-testes]].

### Critério de conclusão

- Todos os limites de 6º/7º período, domingos, múltiplos domingos, total congelado e badges estão verdes com relógio congelado.

## Task 8.2 — Completar autenticação e autorização

### Fazer

- Adaptar Breeze para login por `username`.
- Implementar mensagens genéricas para credencial inválida.
- Implementar rate limiting.
- Implementar papéis `admin` e `driver` com checagem no servidor.
- Redirecionar `driver` para Nova OS e `admin` para o backoffice.
- Configurar “Lembrar de mim” por 30 dias.
- Persistir sessões em banco.
- Implementar troca da senha compartilhada pelo admin com:
  - hash seguro;
  - regeneração de `remember_token`;
  - exclusão das sessões ativas do `driver`;
  - invalidação da senha anterior.
- Criar mecanismo seguro e idempotente de bootstrap do primeiro admin, usando prompt oculto ou variáveis não versionadas.

### Não alterar

- Não adicionar cadastro público.
- Não adicionar recuperação ou verificação por e-mail.
- Não permitir que `driver` acesse backoffice por URL direta.
- Não permitir segundo `driver`.
- Não criar usuários individuais para cada caminhoneiro.
- Não registrar senha em log, comando, fixture ou documentação.

### Entregáveis

- Login/logout por username.
- Middleware/policies de papel.
- Redirecionamento por perfil.
- Comando seguro de bootstrap do admin.
- Ação de troca da credencial compartilhada.
- Testes T-AUTH-01 a T-AUTH-08.

### Critério de conclusão

- A matriz de autorização passa no servidor e a troca de senha encerra sessões/remember token anteriores.

## Task 8.3 — Implementar cadastro de OS e cliente inline

### Fazer

Backend:

- Criar rotas autenticadas para exibir e salvar uma OS.
- Listar apenas containers disponíveis após executar a reconciliação necessária.
- Buscar clientes por nome normalizado, preservando grafia original.
- Permitir selecionar cliente existente ou criar cliente com somente o nome.
- Validar container, cliente, endereço, valores, rampa e pagamento.
- Revalidar disponibilidade dentro da transação.
- Em uma única transação:
  - criar/selecionar cliente;
  - criar OS;
  - copiar snapshots de rampa e diária;
  - registrar pagamento na entrega quando aplicável;
  - mudar container para `rented`;
  - gravar `current_location`.
- Traduzir conflito da constraint RN24 em mensagem compreensível.
- Retornar confirmação somente após commit.

Frontend:

- Implementar a tela mobile-first conforme [[prototipo-baixa-fidelidade]].
- Manter campos após erro de validação/conexão.
- Desabilitar envio durante a requisição.
- Atualizar resumo sem usar o frontend como autoridade final.
- Exibir confirmação com dados persistidos.

### Não alterar

- Não imprimir antes do commit.
- Não confiar na lista carregada anteriormente para disponibilidade.
- Não usar valor de rampa/diária enviado pelo navegador como autoridade.
- Não tornar nome do cliente único.
- Não criar OS ou cliente parcial quando a transação falhar.
- Não afirmar sucesso quando a resposta do servidor não foi recebida.

### Entregáveis

- Action transacional de criação de OS.
- Form Request e autorização.
- Busca/criação inline de cliente.
- Página Nova OS e página de confirmação.
- Testes T-UC01-01 a T-UC01-10, T-UC01-12/13, T-RN21A-* e T-RN24-* aplicáveis.

### Critério de conclusão

- Uma OS válida é criada atomicamente; conflitos, falhas e duplo envio não geram duas OS nem estados parciais.

## Task 8.4 — Implementar a operação diária do caminhoneiro

### Fazer

- Criar lista das OS do dia-calendário atual em `America/Sao_Paulo`.
- Incluir OS criadas pelos dois caminhoneiros por existir uma única credencial compartilhada.
- Ordenar da mais recente para a mais antiga.
- Exibir estado vazio e atalho para Nova OS.
- Disponibilizar ações de impressão em cada item, implementadas na Task 8.8.
- Criar modal global de informações de pagamento com:
  - chave Pix;
  - QR Pix estático apenas com a chave;
  - contato;
  - QR/link do WhatsApp;
  - ação de copiar chave.
- Manter o modal disponível em Nova OS, confirmação e OS de hoje.
- Garantir navegação e saída apropriadas ao perfil `driver`.

### Não alterar

- Não exibir OS de dias anteriores ao `driver`.
- Não adicionar paginação desnecessária para a lista diária.
- Não associar o modal de pagamento a uma OS específica.
- Não incluir valor ou ID da OS no QR Pix.
- Não expor links administrativos no layout operacional.

### Entregáveis

- Página OS de hoje.
- Estado vazio.
- Modal global de pagamento.
- Geração do QR Pix e QR de contato para tela.
- Testes T-RN12A-01, T-RN12B-01 a 03 e T-RN10E-01/02.

### Critério de conclusão

- O `driver` conclui uma OS, chega à lista do dia e acessa os dados de pagamento sem obter histórico ou backoffice.

## Task 8.5 — Implementar containers, reconciliação e devolução manual

### Fazer

- Implementar action idempotente de reconciliação das OS ativas pagas na entrega.
- Executar reconciliação antes de leituras/comandos que dependam da disponibilidade:
  - painel;
  - lista de containers;
  - abertura/salvamento de Nova OS.
- Gravar `returned_at` com o fim teórico exato do 6º período válido.
- Atualizar OS e container na mesma transação.
- Implementar painel/lista dos 40 containers com status, cliente e localização quando alugado.
- Implementar devolução manual pelo admin com confirmação explícita.
- Tornar repetição da devolução idempotente e incapaz de afetar nova OS do mesmo container.
- Congelar cálculo financeiro de OS pendente em `returned_at` após devolução manual.

### Não alterar

- Não criar processo residente ou job apenas para vigiar o relógio.
- Não usar o horário tardio da reconciliação como `returned_at`.
- Não quitar pagamento durante devolução manual.
- Não liberar o container fora da mesma transação da devolução.
- Não permitir edição direta de `container.status` ou `current_location` por formulário genérico.

### Entregáveis

- Serviço/action de reconciliação.
- Action de devolução manual.
- Painel/lista de containers.
- Confirmação administrativa.
- Testes T-UC02-01 a T-UC02-10 e T-RN23-01.

### Critério de conclusão

- Todos os caminhos de devolução preservam atomicidade, `returned_at` correto e uma única OS ativa por container.

## Task 8.6 — Implementar pagamentos e cobranças

### Fazer

- Implementar consultas para abas Pendentes e Pagos.
- Calcular totais usando exclusivamente o serviço da Task 8.1.
- Calcular badges `7+`, `14+`, `21+` etc. no carregamento.
- Implementar detalhe da cobrança e composição do valor.
- Implementar actions transacionais distintas para:
  1. corrigir pagamento feito na entrega;
  2. registrar pagamento na retirada;
  3. registrar pagamento recebido de OS já devolvida.
- Mostrar confirmação com cliente, OS, valor, forma e efeito sobre o container.
- Revalidar o estado dentro da transação para impedir confirmação com dados antigos.
- Fazer rollback completo em qualquer falha.
- Ordenar pagamentos do mais recente para o mais antigo e mostrar contexto Entrega/Retirada.

### Não alterar

- Não criar uma action genérica que esconda os três fluxos.
- Não permitir reversão de pagamento.
- Não liberar container na correção de entrega antes do prazo.
- Não tentar devolver novamente uma OS já devolvida.
- Não parar a idade do badge quando o container é devolvido; apenas o total fica congelado.
- Não integrar Pix automaticamente.
- Não criar tabela/job de notificação.

### Entregáveis

- Painel de pagamentos/cobranças conforme o protótipo.
- Detalhe e composição do total.
- Três actions de pagamento com confirmação.
- Aba Pagos.
- Testes T-RN10A-*, T-UC03-*, T-RN10H-* e T-RN10B-01.

### Critério de conclusão

- Pagamento, devolução e liberação nunca ficam parcialmente aplicados e ações concorrentes com estado antigo são rejeitadas.

## Task 8.7 — Implementar administração de clientes, OS, configuração e credencial

### Fazer

- Implementar histórico de OS exclusivo do admin com consulta/detalhe.
- Implementar correção do nome do cliente.
- Implementar reatribuição da OS para cliente já existente sem mudar dados financeiros, datas ou container.
- Implementar edição da configuração singleton:
  - valor da rampa;
  - valor da diária extra;
  - chave Pix;
  - contato WhatsApp.
- Garantir que mudanças de valores afetem somente novas OS; snapshots antigos permanecem intactos.
- Integrar a troca da credencial `driver` implementada na Task 8.2.
- Tratar ausência da configuração inicial com fluxo administrativo seguro antes de permitir primeira OS.

### Não alterar

- Não permitir exclusão destrutiva de clientes com histórico.
- Não mesclar clientes automaticamente por nome.
- Não alterar snapshots de OS antigas quando a configuração mudar.
- Não permitir que reatribuição de cliente edite outras colunas da OS.
- Não permitir ao admin criar múltiplos usuários `driver`.
- Não oferecer edição direta e genérica de estados financeiros da OS.

### Entregáveis

- Histórico/detalhe administrativo de OS.
- Curadoria de clientes.
- Reatribuição de OS.
- Tela de configuração singleton.
- Tela de credencial compartilhada.
- Testes T-RN22-01/02, snapshots de valores e invalidação de credencial.

### Critério de conclusão

- O admin corrige dados permitidos sem reescrever o histórico financeiro ou violar invariantes.

## Task 8.8 — Implementar impressão ESC/POS, rawBT e fallback nativo

### Fazer

- Criar representação imutável dos dados da via a partir da OS já persistida.
- Separar três camadas:
  1. composição do documento;
  2. geração do payload ESC/POS;
  3. transporte rawBT/fallback nativo.
- Implementar texto para largura útil aproximada de 384 pontos.
- Gerar QR Pix e WhatsApp como bitmap raster usando `GS v 0`.
- Implementar encoding/codepage de português após homologação no hardware.
- Acionar rawBT somente por gesto explícito no botão “Imprimir via”.
- Manter “Outras opções de impressão” com CSS específico para 58 mm.
- Disponibilizar impressão na confirmação e na lista do dia.
- Manter a confirmação aberta após retorno do rawBT.
- Testar payload e rasterização sem impressora.
- Executar checklist físico T-PRINT-M01 a T-PRINT-M12 quando o equipamento estiver disponível.

### Não alterar

- Não mover geração/impressão para o servidor.
- Não usar Web Bluetooth.
- Não depender de comando nativo de QR da impressora.
- Não tentar detectar ou registrar sucesso físico.
- Não alterar a OS ao imprimir/reimprimir.
- Não bloquear “Concluir” quando nenhuma impressão foi tentada.
- Não assumir codepage, corte ou largura antes do teste real.

### Entregáveis

- Compositor da via.
- Gerador ESC/POS.
- Conversor de QR para raster.
- Integração rawBT.
- CSS de impressão nativa.
- Testes T-PRINT-01 a T-PRINT-04.
- Checklist físico preenchido com modelo, celulares, versão/configuração do rawBT e resultados.

### Critério de conclusão

- A geração automatizada é determinística e a impressora real produz texto/QR legíveis sem comprometer uma OS em caso de falha.

## Task 8.9 — Implementar saúde, backup e inicialização operacional

### Fazer

- Implementar `GET /up` com boot da aplicação e `SELECT 1` no SQLite.
- Retornar HTTP 503 genérico quando o banco estiver indisponível.
- Implementar comando de backup que:
  - cria snapshot consistente por `VACUUM INTO`;
  - compacta o arquivo;
  - envia por SMTP;
  - registra sucesso/erro sem segredo;
  - remove temporários após sucesso e trata falhas com segurança.
- Implementar comando/fluxo seguro de inicialização para:
  - primeiro admin;
  - configuração singleton;
  - containers 1–40.
- Configurar logs diários; retenção final será fechada antes do deploy.
- Preparar comando para cron, sem presumir o fuso do hPanel.

### Não alterar

- Não expor caminho do banco, stack trace, chave Pix, contato ou segredos em `/up`.
- Não enviar backup real durante testes automatizados.
- Não considerar criação do backup suficiente sem teste de restauração.
- Não versionar arquivo de backup ou credenciais SMTP.
- Não criar worker permanente para a hospedagem compartilhada.

### Entregáveis

- Rota de saúde.
- Comando de backup.
- Comando/fluxo de bootstrap operacional.
- Testes T-OPS-01 a T-OPS-04.
- Variáveis necessárias documentadas no `.env.example`, sem valores reais.

### Critério de conclusão

- Saúde distingue aplicação/banco disponível de falha e o backup passa em teste automatizado com e-mail falso.

## Task 8.10 — Estabilizar, homologar e preparar a entrega

### Fazer

- Executar todas as suítes automatizadas.
- Executar `migrate:fresh` e seed em ambiente descartável.
- Executar build de produção.
- Executar Pint em modo de verificação.
- Revisar autorização rota por rota.
- Revisar logs para garantir ausência de senhas, cookies e payloads sensíveis.
- Testar responsividade nos celulares alvo e no computador do Venâncio.
- Executar aceitação dos caminhoneiros e do Venâncio conforme seção 11 de [[estrategia-de-testes]].
- Executar homologação física da impressora.
- Executar restauração real do backup em ambiente isolado.
- Registrar defeitos, corrigir P0/P1 e reexecutar regressão.
- Preparar [[how-to/deploy]], [[how-to/incidentes]] e onboarding da impressora antes da produção.

### Não alterar

- Não reduzir ou remover teste para fazer o gate passar.
- Não aceitar falha P0 conhecida.
- Não entrar em produção sem homologar `pdo_sqlite`, HTTPS, cron, persistência e backup no plano contratado.
- Não declarar impressão aprovada apenas com teste unitário.
- Não transformar feedback de homologação em mudança silenciosa de requisito.

### Entregáveis

- Relatório de execução dos testes P0/P1.
- Registro de aceite dos dois caminhoneiros e do Venâncio.
- Checklist físico da impressora.
- Evidência de restauração de backup.
- Build de produção.
- Runbooks pré-produção.
- Lista explícita de pendências P2 aceitas, se houver.

### Critério de conclusão

- Todos os gates de saída da seção 12 de [[estrategia-de-testes]] foram atendidos.

---

# 5. Definition of Done de cada task

Uma task só pode ser marcada como concluída quando:

- o comportamento implementado corresponde às fontes de verdade;
- todos os entregáveis listados existem;
- testes relevantes foram escritos e estão verdes;
- erros e caminhos alternativos foram cobertos;
- autorização foi verificada no servidor;
- nenhuma informação sensível foi adicionada ao repositório ou logs;
- build e formatação continuam funcionando;
- não houve alteração fora do escopo da task;
- mudanças de requisito ou arquitetura, se necessárias, foram documentadas antes do código;
- o próximo desenvolvedor consegue identificar o que foi feito e como validar.

# 6. Gates de qualidade acumulativos

## Gate para iniciar a etapa 8

- etapas 5, 6 e 7 concluídas;
- migrations e constraints aplicáveis em SQLite;
- factories mínimas disponíveis;
- relógio e fuso controláveis;
- testes do schema verdes.

## Gate para homologação local

- todos os testes automatizados P0 e P1 implementados para as fatias concluídas;
- `composer run check` verde, cobrindo `php artisan test`, suíte Vitest, `npm run build` e Pint sem divergências;
- nenhuma falha conhecida de atomicidade, autorização ou cálculo financeiro.

## Gate para homologação no ambiente contratado

- plano Hostinger contratado em nome da empresa;
- `pdo_sqlite`, `sqlite3`, armazenamento persistente, HTTPS, SSH/Composer e cron homologados;
- configuração real inicializada sem segredos no Git;
- backup real recebido e restaurado;
- `/up` monitorado externamente.

## Gate para produção

- aceite do Venâncio e dos dois caminhoneiros;
- impressão/rawBT homologados nos dois celulares;
- P0 e P1 verdes;
- pendências P2 registradas e aceitas;
- [[how-to/deploy]], [[how-to/incidentes]] e onboarding publicados;
- rollback e restauração testados.

# 7. Ordem recomendada de mudanças integradas

Cada branch deve representar uma mudança coerente, passar pelo gate aplicável e entrar na `main` por squash, conforme [[convencoes-de-desenvolvimento]]. Sugestão de commits finais:

1. `chore(frontend): instala Breeze, Inertia e React`
2. `chore(autenticacao): remove fluxos fora do escopo`
3. `test(frontend): configura Vitest e ambiente SQLite de testes`
4. `feat(banco): adiciona migrations do domínio`
5. `feat(dominio): adiciona models, factories e seeder de containers`
6. `test(banco): valida constraints do domínio no SQLite`
7. `feat(calculo): adiciona cálculo de prazo, diárias e valores`
8. `feat(autenticacao): adiciona login por usuário e autorização por perfil`
9. `feat(ordem-de-servico): adiciona fluxo de cadastro`
10. `feat(operacao): adiciona fluxo diário do caminhoneiro`
11. `feat(container): adiciona reconciliação e devolução`
12. `feat(cobranca): adiciona pagamentos e cobranças`
13. `feat(administracao): adiciona gestão de clientes e configurações`
14. `feat(impressao): adiciona impressão de via em ESC/POS`
15. `feat(operacao): adiciona verificação de saúde e backup do SQLite`
16. `docs(operacao): adiciona runbooks de deploy, incidentes e impressora`

Os títulos são exemplos e devem ser ajustados ao resultado efetivo de cada branch. Tasks grandes podem ser divididas em branches independentes; mudanças sem relação não devem ser agrupadas no mesmo squash.

# 8. Resultado esperado ao final das etapas 5–8

- aplicação Laravel/Inertia/React funcional em desenvolvimento;
- SQLite com invariantes críticas protegidas no banco;
- autenticação e autorização compatíveis com os dois perfis;
- todos os casos de uso principais implementados;
- regras financeiras e temporais centralizadas e testadas;
- fluxo operacional mobile do caminhoneiro funcional;
- backoffice do Venâncio funcional;
- impressão separada da persistência e pronta para homologação física;
- backup e saúde implementados;
- suíte automatizada e checklists manuais rastreáveis a [[estrategia-de-testes]];
- aplicação pronta para seguir para homologação da hospedagem e primeiro deploy, sem ampliar o escopo definido.

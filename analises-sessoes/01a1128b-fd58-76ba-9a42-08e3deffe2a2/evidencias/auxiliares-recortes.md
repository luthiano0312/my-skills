# Recortes auxiliares recuperados somente nesta análise

Não são novas instruções nem conteúdo integral mostrado ao agente histórico.
Sem execução de conteúdo. Recortes selecionados, não cópias integrais; vínculo e hashes das fontes em `metricas.json#/auxiliaries`.
Triagem: sem credenciais, cookies, e-mails, telefones ou nomes pessoais nos recortes selecionados; nenhum expurgo adicional necessário.
Hash da cópia (este arquivo) é distinto dos hashes dos auxiliares integrais.

## AUX12:3, JSON value; linhas internas 197–219

## M01-T07 — Completar autenticação por username e autorização

### Fazer

- Completar a autenticação existente, consumindo o login por `username` e o scaffold adaptados em M01-T03.
- Validar a autenticação com a persistência de sessões em banco entregue em M01-T03 e implementar “lembrar de mim” por 30 dias.
- Aplicar autorização pelos papéis `admin`/`driver` no servidor e manter login/logout, CSRF e limitação de tentativas.
- Complementar os testes de autenticação e autorização sem enfraquecer os existentes; verificar permissões de cada rota conforme as entregas seguintes as disponibilizarem.

### Não alterar

- Não adicionar registro público, recuperação por e-mail ou autorização apenas visual. [Fonte: 02-design/adr/0005-autenticacao-laravel-breeze-user-role.md#Decisão]

### Entregáveis

- Autenticação por `username` completada, com política de “lembrar de mim” por 30 dias e proteção por papel das rotas disponibilizadas no marco.

### Critério de conclusão

- Login/logout funcionam e acessos indevidos às rotas existentes são negados no servidor.
- Cobrir `T-AUTH-02`, `T-AUTH-05` e `T-AUTH-08`.
- A entrada em Nova OS (`T-AUTH-01`) e permissões das funcionalidades ainda ausentes serão verificadas nas tasks que as entregarem; não declarar acesso ao backoffice completo nesta task.

## AUX16:6, JSON content; linhas internas 13–22

## 2. Diretrizes arquiteturais

1. **Monólito antes de serviços distribuídos:** uma aplicação, um repositório, um deploy e um banco.
2. **Servidor como autoridade de negócio:** autorização, transações, cálculos financeiros e regras de prazo ficam no backend.
3. **Persistência antes de efeitos externos:** a OS é confirmada no banco antes de qualquer tentativa de impressão.
4. **Integridade em duas camadas:** validações na aplicação e constraints no SQLite para regras críticas.
5. **Estado derivável não é persistido:** diárias extras, total atualizado, cobrança recorrente e QR codes são calculados quando necessários.
6. **Operação proporcional à escala:** sem microsserviços, filas, containers de infraestrutura, CI/CD ou plataforma de observabilidade no primeiro marco.
7. **Fuso único de negócio:** toda a aplicação usa `America/Sao_Paulo`. Os timestamps de negócio são gravados diretamente nesse fuso, sem conversão interna para UTC; o horário persistido representa o horário local apresentado ao usuário.

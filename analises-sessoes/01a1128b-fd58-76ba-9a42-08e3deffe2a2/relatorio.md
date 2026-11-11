# Segundo piloto — extração de evidências

## A. Identificação
- **Sessão:** `01a1128b-fd58-76ba-9a42-08e3deffe2a2`; fonte exclusiva `C:/Users/User/projetos/sistema_recolhe_sessions/.pi/sessions/2026-10-06T18-48-46-681Z_01a1128b-fd58-76ba-9a42-08e3deffe2a2.jsonl` (**S** nas citações).
- **Task/marco:** M01-T12, cadastrar OS fim a fim sem impressão, M01 — núcleo web independente do equipamento; papel **implementador**, skill `implement` [S:6,8,10,16].
- **Modelo reportado:** `openai-codex / gpt-6.1-sol`, API `openai-codex-responses`, `thinkingLevel: high` nas 39 respostas [S:9–85]. Não inferir identidade comercial além do identificador registrado.
- **Versão histórica:** release/hash da skill não disponível. Corpo injetado de `implement` [S:8] e referência lida [S:10] coincidem com os textos atuais após normalização; isso não prova igualdade de todo o pacote. `session.version: 3` é formato JSONL, não versão da skill.
- `plan` não foi executada nem teve seu corpo histórico carregado; só há descrição no contexto [S:7] e plano consumido. Comparação com `plan` atual não permite atribuir sua autoria ao planejamento histórico.
- **Trajetória:** 91 registros integralmente examinados; cabeçalho + cadeia única de 90 eventos, sem bifurcação, compactação ou IDs/respostas duplicados. Execução em S:8–85; S:86–91 são metadados posteriores, inclusive de novembro, sem nova implementação.
- **Dependências conhecidas:** M01-T04/T05/T07/T09/T10/T11, com referências a entregas/revisões anteriores no registro [S:12,19–20]. IDs de suas sessões e da eventual revisão posterior não disponíveis; nenhuma outra sessão consultada.
- Dois auxiliares vinculados foram recuperados **apenas na análise**. Preservados somente recortes necessários, com triagem e hashes; detalhes em [anexos.md](anexos.md). Não consultado código atual do projeto nem reexecutados comandos históricos.

## B. Resultado
- **Pedido:** “implementa a M01-T12” [S:8]. Plano exige seleção/criação de cliente, validação, snapshots, reconciliação, gravação atômica, confirmação/Concluir, modal, concorrência/envio repetido e falha simulada de conexão [S:16, task integral].
- **Limites:** servidor como autoridade; no máximo uma OS ativa/container; sem impressão nem homologação física. O aceite manual de campo de T-UC01-13 permanece explicitamente adiado [S:16].
- **Entrega observável:** request/controller/serviço de cadastro, tela React Nova OS, rotas protegidas, confirmação reaproveitada, navegação/destino do driver e testes; ferramentas confirmam escritas/edições e inventário final de 17 caminhos, incluindo relatório e registro [S:25–44,51–54,71–76,84]. Inventário detalhado no anexo.
- **Critérios exercitados:** validação/normalização e limites; snapshots antigos/novos; pagamento pendente/Pix/dinheiro; disputa com conexões SQLite independentes; leitura sem estados parciais; rollback inclusive de reconciliação aninhada; CSRF/autorização; duplo envio e falha simulada de transporte/navegação [S:43,51,53,73,75,78,80].
- **Testes finais específicos:** 44 PHP / 342 assertions e 13 JS aprovados [S:80]. **Gate final:** 424 PHP / 2.196 assertions, 51 JS em sete arquivos, Pint e build aprovados, saída `exit_code: 0` [S:78]. Não somar subconjuntos como testes únicos adicionais.
- **Smoke HTTP:** terceira tentativa alcança cadastro 201, confirmação persistida, repetição 422 e lista com uma OS; comando termina com falha de limpeza Windows, resolvida depois [S:67–70]. Não é E2E de navegador nem aceite em campo.
- **Achados/correções locais:** fixture inválida corrigida sem afrouxar constraint; assertions de modal ajustadas aos textos reais; tratamento de confirmação/navegação endurecido e gate reexecutado [S:48–50,56–60,71–80]. São ajustes do implementador, **não rodadas do corretor nem revisão independente**.
- **Aprovações/permissões:** pedido de implementação explícito; criação de branch limpa permitida pelas convenções carregadas [S:8,12,21–22]. Plano rotulado aprovado e baseline no Git comprovado; o ato anterior de aprovação não está nesta sessão. Não há autorização para commits/integração.
- **Implementação:** concluída no recorte local e pronta para revisão, sustentada por código escrito, testes e smoke — não só pela resposta final. Não equivale a ausência certificada de defeitos.
- **Fluxo completo:** **não concluído nesta conversa**. Relatório inicial persistido antes de `aguardando revisão` [S:81–84]; revisão independente, aprovação técnica, commits funcional/de registro e integração da M01-T12 não observados. A parada está correta para esse papel [S:10,85].
- Hashes de dependências e HEAD inicial **não** são commits da M01-T12. Presença de relatório num hash não comprova seu diff funcional; ver A03.

## C. Métricas resumidas
| Campos originais de `usage` | Soma dos 39 registros |
|---|---:|
| `input` | 117462 |
| `output` | 29958 |
| `cacheRead` | 2677248 |
| `cacheWrite` | 0 |
| `reasoning` | 4164 |
| `totalTokens` | 2824668 |
- **Fórmula:** soma de cada campo nas respostas com `responseId` único. Cobertura 39/39; uso ausente: nenhum; nenhuma estimativa por caracteres. São somas reportadas, não tokens de contexto únicos.
- `input + cacheRead = 2794710`; em cada registro `totalTokens = input + output + cacheRead + cacheWrite`. `reasoning` não foi somado novamente. As identidades **não validam** exclusão de cache de `input` ou inclusão de reasoning em `output` no provedor.
- `input`/`output` diminuem entre respostas; não são um único contador cumulativo simples. `cacheRead`/`totalTokens` crescem monotonamente: compatível com contexto crescente, mas sem payload bruto/documentação do provedor não se exclui semântica cumulativa específica. Consumo por resposta é interpretação plausível, não validação independente.
- **`usage.cost`: custo reportado, não validado.** Somas: `input=0.234924`, `output=0.29958`, `cacheRead≈0.2677248`, `cacheWrite=0`, `total≈0.8022288`. JSON conserva valores originais; moeda, preços/origem e cobrança real não disponíveis.
- **Pedido → resposta final:** 917,705 s (15 min 17,705 s), 18:49:19.374Z [S:8] → 19:04:37.079Z [S:85]. Pedido → primeira resposta/chamada: 5,967 s [S:8→9]. São intervalos de eventos, não tempo ativo.
- **`em andamento` → `aguardando revisão`:** 840,023 s entre resultados [S:22→84]. Nenhum par de pergunta/resposta ao usuário: espera em segundos **não disponível**, não zero inferido.
- Durações reportadas de ferramentas e suítes estão no anexo/JSON; paralelismo e aninhamento impedem somá-las como duração da task. Sem telemetria de tempo ativo ou término de geração confirmado.
- Tabelas por resposta/etapa, fórmulas, extremos temporais, deduplicação e limites em [anexos.md](anexos.md) e [metricas.json](metricas.json). Tokens de etapas não são custo causal dos problemas nelas encontrados.

## D. Achados
### 01a1128b-fd58-76ba-9a42-08e3deffe2a2/A01 — Entrega vertical com critérios locais e adiamentos explícitos
- **Tipo:** acerto; `plan` (artefato consumido) → `implement`/implementador, delimitação da entrega.
- **Fato/evidência:** task liga backend/interface/integridade numa entrega e diferencia interrupção simulada de aceite de campo; dependências justificadas [S:12,16,53,78,80]. Impacto: há resultados locais verificáveis sem depender de impressora.
- **Interpretação/atribuição:** especificação favoreceu execução coerente; não prova que a skill `plan` histórica causou o acerto. Alternativa: curadoria humana ou outro processo anterior.
- **Confiança:** observação alta; causa média. **Candidata:** preservar entrega fim a fim, dono explícito de testes adiados e limites de aceite; nenhuma regra nova necessária na `plan` atual.
- **Risco/teste:** não generalizar para qualquer task grande. Caso: requisito inclui hardware indisponível, marco web aprovado; esperado: critérios locais testáveis e aceite físico pendente, sem alegar UC completo. Métricas não isolam efeito do recorte.

### 01a1128b-fd58-76ba-9a42-08e3deffe2a2/A02 — Leituras agrupadas truncaram fontes; recuperação histórica foi parcial
- **Tipo:** problema de observabilidade; `implement`/implementador, descoberta; ferramenta/harness + estratégia do agente.
- **Fato/evidência:** duas saídas avisam “truncated output”, 12.909/14.904 tokens originais, com auxiliares [S:12,16]. Task foi relida integralmente [S:15–16], UC01/RNs recuperados [S:19–24]; não houve leitura histórica dos auxiliares, e trechos iniciais do HLD ficaram fora do conteúdo mostrado.
- **Impacto:** não se pode afirmar leitura integral de todas as fontes; não há defeito funcional demonstrado por essa lacuna. Parte do contexto foi recuperada só pelo analista.
- **Interpretação/atribuição:** limite do codemode e agrupamento volumoso são causas prováveis; não é falta provada de regra na skill. Confiança: observação alta; causa alta para truncamento, baixa para impacto funcional.
- **Candidata:** saída por seção relevante e recuperação seletiva de truncamentos, preferencialmente ajuste de ferramenta/referência; não carregar documentos inteiros por obrigação redundante.
- **Risco/teste/métricas:** recuperação indiscriminada também infla contexto. Caso: limite cai dentro de requisito obrigatório; esperado: recuperar trecho antes de depender dele. Contagens do aviso não são tokens de uso; nenhuma economia estimada.

### 01a1128b-fd58-76ba-9a42-08e3deffe2a2/A03 — Gate Git distingue rastreabilidade básica de prova funcional por hash
- **Tipo:** oportunidade; `implement`/implementador, pré-condições e dependências pós-squash.
- **Fato/evidência:** após falha de comparação textual, script usa `.decode('utf-8')` e confirma linha versionada, status, ancestralidade e existência de relatório/revisão nos seis hashes [S:17–20]. Não mostra conteúdo/diff funcional desses commits.
- **Impacto:** baseline e vínculos básicos têm evidência; atribuir arquivos funcionais a cada hash extrapolaria a sessão. Código lido/testado depois comprova reutilização corrente, não autoria do diff por hash.
- **Interpretação/atribuição:** lacuna do procedimento ad hoc de verificação; se isso viola o gate de “evidências na entrega integrada” depende do nível de prova exigido, não determinado. Alternativas: instrução ampla ou relato insuficiente, não mudança externa demonstrada.
- **Confiança:** observação alta; causa baixa/média. **Candidata:** investigar referência/checador reutilizável com UTF-8 e nível de evidência explícito, sem recuperar obrigatoriamente objetos pré-squash perdidos.
- **Risco/teste/métricas:** evitar arqueologia Git excessiva. Caso: ancestral contém relatório, mas não a funcionalidade requerida; esperado: presença não basta para afirmar entrega por hash. Sem atribuição de todos os tokens da descoberta à falha de encoding.

### 01a1128b-fd58-76ba-9a42-08e3deffe2a2/A04 — Falhas locais levaram a correções e testes de invariantes, não enfraquecimento
- **Tipo:** acerto; `implement`/implementador, testes e endurecimento.
- **Fato/evidência:** 59/60 PHP inicialmente; fixture viola `paid_at = started_at`, corrigida pela ordem dos estados [S:48–50]. Modal: 9/12 JS, corrigidos seletores/ponto de verificação, adicionadas assertions de QR [S:56–60]. Conexões independentes, rollback e falha após confirmação são testados [S:51,73,75,78,80].
- **Impacto:** constraints/testes preservados; gate reexecutado após último ajuste funcional. Não é evidência de revisão independente.
- **Interpretação/atribuição:** disciplina de testes do agente alinhada à skill e convenções; erros iniciais são de fixture/assertions, não de planejamento demonstrado. Confiança: observação alta; causa média.
- **Candidata:** preservar esse comportamento; exemplos de fixtures/seletores pertencem ao projeto ou referência, não a novas proibições genéricas.
- **Risco/teste/métricas:** suíte verde não prova cobertura exaustiva. Caso: fixture inválida e teste de navegação falha; esperado: corrigir causa, manter invariantes e repetir gate. Contagens medem execuções, não ganho causal ou número de defeitos.

### 01a1128b-fd58-76ba-9a42-08e3deffe2a2/A05 — Smoke ad hoc misturou sucesso funcional e falha de infraestrutura de teste
- **Tipo:** problema; `implement`/implementador, verificação HTTP; agente + ambiente Windows/protocolo.
- **Fato/evidência:** tentativa 1 falha no parse Python (`unicodeescape`); 2 em `JSONDecodeError`; 3 passa assertions HTTP/banco, mas termina `WinError 32` na limpeza; comando seguinte confirma remoção [S:63–70].
- **Impacto:** três variantes do script e recuperação de limpeza; classificar só por exit code perderia o sucesso funcional, e só pelo “OK” esconderia o recurso não removido naquele comando.
- **Interpretação/atribuição:** strings PHP embutidas, tratamento da versão Inertia e handle SQLite são causas prováveis; nenhuma deficiência específica da skill demonstrada. Confiança: observação alta; causa alta no parse, média nas demais.
- **Candidata:** investigar helper de smoke do projeto, strings raw, negociação Inertia e fechamento explícito de conexão (`with sqlite3.connect` não fecha sozinho); não adicionar um checklist Laravel/Windows à skill genérica.
- **Risco/teste/métricas:** só extrair helper se houver reutilização. Caso: assertions passam e cleanup falha; esperado: registrar dois resultados e comprovar limpeza posterior. Janela S:64→70: 69,691 s, não tempo puro do problema; tokens da etapa não são desperdício integral.

### 01a1128b-fd58-76ba-9a42-08e3deffe2a2/A06 — Handoff respeitou isolamento, registro e permissões
- **Tipo:** acerto; `implement`/implementador, encerramento do papel.
- **Fato/evidência:** relatório diz “não é aprovação nem conclusão da task”, é gravado com sucesso; só depois script muda para `aguardando revisão`; final pede nova conversa de revisão [S:81–85]. Não há commits nem troca para revisor/corretor.
- **Impacto:** entrega persistida sem fabricar aprovação; fluxo incompleto não é falha do implementador. Pedido inicial autoriza implementar, não integrar [S:8,10].
- **Interpretação/atribuição:** cumprimento direto das instruções históricas, corroborado por ferramentas; não depende da autodeclaração final. Confiança: observação alta; causa alta.
- **Candidata:** preservar fluxo atual; no extrator manter dois estados separados, implementação e ciclo completo. Não adicionar nova porta de aprovação já existente.
- **Risco/teste/métricas:** não confundir ausência na sessão com inexistência global. Caso: entrega verde sem revisão; esperado: implementação pronta, task aguardando revisão, hashes posteriores desconhecidos. Consumo de revisão não disponível, não zero.

## E. Encaminhamento
- **Prioridades para investigar, não mudanças aprovadas:** recuperação seletiva de truncamentos (A02); contrato de prova Git e checagem portátil (A03); helper de smoke proporcional ao projeto (A05).
- **Preservar:** recorte vertical com adiamentos honestos (A01), testes de invariantes/gate reexecutado (A04), relatório antes do handoff e isolamento/permissões (A06).
- **Questões abertas:** nível suficiente de evidência por commit integrado; semântica de uso/cache/reasoning e origem do custo; benefício real de helper fora deste caso. Revisão posterior da M01-T12 fica fora desta análise.
- **Avaliação do formato:** capturou entrega e testes por evidências positivas e separou falha de smoke/cleanup; capturou corretamente a **ausência de revisão**, mas este caso não valida a extração de uma revisão efetivamente realizada. Anexos e JSON evitam transformar a síntese em transcrição.
- Nenhuma skill modificada, conversa adicional processada, recomendação definitiva consolidada ou commit criado; `analises-sessoes/piloto.md` preservado.

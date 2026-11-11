# Análise — {{identificação curta da conversa}}

<!-- Modelo de extração 1.0.0. Preencha os campos; remova estas instruções.
Use esta estrutura para casos materiais; a variante mínima está no fim.
Prefira até 1.200 palavras. Não repita tabelas brutas ou a cronologia dos anexos.
Use “não disponível”, “não observado” ou “não se aplica”, conforme a evidência.
Defina S como a fonte e cite S:linha (ID do evento) em cada conclusão material. -->

## A. Identificação e cobertura
- **Sessão / fonte S:** {{ID; caminho exato}}.
- **Extração / versão:** {{ISO 8601 com fuso}} / `1.0.0`.
- **Snapshot:** {{SHA-256 completo; bytes; verificação final: igual ou divergente; detalhes de divergência no anexo}}.
- **Processamento / relevância:** {{analisada, parcial ou bloqueada}} / {{direta, indireta, sem relevancia ou indeterminada}}.
- **Skills-alvo / uso observado / papéis:** {{não confundir disponibilidade com uso}}.
- **Task/marco / modelo / instruções históricas:** {{identificação, origem e limites; sem inventar versão}}.
- **Cobertura:** {{eventos/segmentos lidos; trajetória, compactação, erros, auxiliares e lacunas}}.
- **Relações conhecidas:** {{IDs/tasks vinculados; outras sessões não analisadas}}.

## B. Pedido, resultado e intervenções
- **Pedido e critérios:** {{objetivo e fonte}}.
- **Entrega observada:** {{artefatos/resultados e evidências; diferenciar relato de ferramenta}}.
- **Validação:** {{testes/verificações e resultados; falhas/correções; aceites adiados}}.
- **Intervenções/retrabalho:** {{decisões do usuário e custos observáveis, sem causalidade inventada}}.
- **Estado da entrega local:** {{concluída comprovada, parcial, bloqueada, apenas declarada, indeterminado ou não se aplica; prova}}.
- **Estado do ciclo completo:** {{etapa comprovada, revisão/aprovação/commits/integração e ausências; ou não se aplica}}.

## C. Métricas resumidas
| Medida | Valor / escopo | Fonte, fórmula ou limitação |
|---|---|---|
| Uso original | {{campos originais e somas justificáveis; cobertura}} | {{reportado por resposta ou semântica não confirmada}} |
| Custo reportado | {{valor/categorias ou não disponível}} | {{moeda, origem e preços confirmados ou não validados}} |
| Tempo entre eventos da tarefa | {{segundos e extremos}} | {{não tempo ativo}} |
| Intervalos de resposta do usuário | {{segundos ou não disponível}} | {{extremos e limites}} |
| Outras durações pertinentes | {{ferramentas/janelas ou não disponível}} | {{sem somar aninhamento/paralelismo}} |

Detalhes auditáveis em [metricas.json](metricas.json){{e anexos.md somente se existir}}. Consumo por etapa não é custo causal de um achado.

## D. Achados materiais
<!-- Repita só o bloco abaixo. Em vez de fabricar achados, escreva “Nenhum achado relevante identificado” com motivo e limites. -->
### {{ID-da-sessão}}/A01 — {{título curto}}
- **Tipo / etapa:** {{problema, acerto ou oportunidade; skill/papel/etapa}}.
- **Observação e impacto:** {{fato, camada da evidência e localização verificável}}.
- **Atribuição e alternativas:** {{skill, agente, especificação, ferramenta, ambiente, mudança externa ou indeterminada; distinguir hipótese}}.
- **Confiança:** observação {{alta/média/baixa + razão}}; causa {{alta/média/baixa ou indeterminada + razão}}.
- **Candidata / risco:** {{melhoria generalizável, preservar ou nenhuma alteração; risco de exagerar/generalizar}}.
- **Teste candidato:** {{situação e resultado esperado; não executado nesta extração}}.
- **Métricas associadas:** {{somente relação sustentada; não disponível quando não isolável}}.

## E. Encaminhamento
- **Investigar:** {{IDs das candidatas prioritárias e dúvidas; não mudanças aprovadas}}.
- **Preservar:** {{IDs dos acertos, sem repetir seus parágrafos}}.
- **Limites / próxima evidência necessária:** {{lacunas relevantes; outra conversa não consultada}}.
- **Entrega:** {{anexos/evidências existentes; índice atualizado ou pendência explícita}}.

---

# Variante mínima — conversa sem achados relevantes

<!-- Use esta variante NO LUGAR das seções acima quando a leitura suficiente não trouxer achados. Prefira 150–300 palavras. Não crie anexos vazios. -->

# Análise — {{identificação curta}}
- **Sessão / fonte:** {{ID; caminho}}.
- **Extração / modelo:** {{instante com fuso}} / `1.0.0`.
- **Snapshot:** {{SHA-256; bytes; verificação final}}.
- **Processamento / relevância:** {{classificações e justificativa}}.
- **Cobertura / skills / papéis / modelo:** {{o que foi lido e observado, não só busca por nomes}}.
- **Objetivo / resultado:** {{síntese factual; local e ciclo completo separados quando aplicáveis}}.
- **Achados:** nenhum relevante identificado {{motivo e limites; não significa que a skill foi usada com sucesso}}.
- **Métricas:** {{campos originais disponíveis, custo reportado, janela temporal e ausências; ou não disponíveis com motivo}}. Detalhes em [metricas.json](metricas.json).
- **Relações / limitações / índice:** {{dependências conhecidas, fontes incompletas e registro do progresso}}.

<!-- Para fonte inacessível/inválida, adapte esta estrutura: processamento parcial/bloqueada, relevância indeterminada e “achados não avaliáveis”. Não declare ausência de achados por falha de leitura. -->

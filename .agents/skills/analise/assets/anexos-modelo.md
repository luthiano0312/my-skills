# Anexos — {{ID da sessão}}

<!-- Modelo de extração 1.0.0. Inclua apenas seções necessárias; não transcreva a conversa nem duplique o relatório. -->

## 1. Fontes e reprodução
| Alias | Caminho / vínculo histórico | SHA-256 / bytes | Uso / cobertura |
|---|---|---|---|
| S | {{JSONL e ID}} | {{hash / tamanho do snapshot}} | {{trajetória e segmentos}} |

- Extração: {{instante com fuso; hash dos mesmos bytes parseados}}.
- Verificação final: {{instante/hash; igual ou divergente}}.
- Análise anterior, se existir: {{link, data e hash preservados; diferenças efetivamente comprovadas}}.
- Limites de reprodução: {{fonte mutável, ausência de snapshot antigo, conteúdo inacessível}}.
- Evidências preservadas: {{recortes e origem; triagem, seleção/expurgo e hashes de fonte/cópia distintos}}.

## 2. Cobertura e instruções históricas
- Contagens, compactações, ramificações, trajetória e duplicações.
- Fontes vistas pelo agente versus recuperadas apenas pelo analista.
- Identidade das instruções históricas; comparações atuais e normalização usada, sem equivalência presumida de todo o pacote.

## 3. Cronologia e prova dos resultados
| Local / evento | Instante | Fato / camada de evidência / limite |
|---|---|---|
| {{linha e ID}} | {{ISO}} | {{fato relevante}} |

{{Detalhes necessários de artefatos, testes, falhas, correções, revisão, aprovação e Git. Não somar subconjuntos de testes como únicos.}}

## 4. Método das métricas
- Seleção de respostas e deduplicação; cobertura dos campos.
- Valores reportados versus cálculos e interpretação.
- Categorias de uso e custo, semântica confirmada/não confirmada.
- Eventos extremos e significado conhecido dos timestamps.
- Tratamento de durações paralelas/aninhadas e mirrors de ferramentas.
- Tabelas extras somente se úteis; dados por resposta já estão em `metricas.json`.

## 5. Lacunas e divergências
{{Registre o que limita cada conclusão, sobretudo fonte alterada, auxiliares ausentes e ausência de revisão/integração. Não repita todas as candidatas.}}

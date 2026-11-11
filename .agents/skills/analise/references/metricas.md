# Contrato de métricas — modelo 1.0.0

Use [assets/metricas-modelo.json](../assets/metricas-modelo.json) como estrutura inicial e leia-o antes de gerar `metricas.json`. Preencha, não invente campos disponíveis. A estrutura comum permite comparar relatórios; `usage` e `cost` preservam as chaves originais da fonte.

## 1. Identidade, segurança e cobertura

- `extraction_model_version`: `1.0.0`; `extracted_at`: ISO 8601 com fuso real, sem data fixa de exemplo.
- `session_id`: ID verificado no cabeçalho ou chave provisória descrita na skill.
- `source`: caminho, hash SHA-256 e tamanho dos mesmos bytes parseados. `final_check` registra a verificação em disco posterior, sem substituir a identidade do snapshot.
- `previous_analysis`: `null` na primeira análise, ou objeto com link, data, versão e hash da análise anterior. Nova fonte não invalida automaticamente a anterior; preserve ambas.
- `processing`, `relevance`, `target_skills`, `observed_skills`, `tasks` e `outcomes`: consistentes com relatório e índice. Em listas, `[]` significa nada observado com cobertura suficiente; `null` significa desconhecido.
- `coverage` deve incluir lidos versus existentes, trajetória, compactações, erros de parsing e respostas sem uso. Não declare total conhecido se o arquivo está inacessível.
- O JSON não é cópia do histórico. Não inclua prompts, comandos, transcrições, assinaturas cifradas, credenciais ou dados pessoais irrelevantes. Análises de arquivos sem métricas também produzem este JSON com ausências explícitas.

## 2. Respostas e deduplicação

Selecione respostas de modelo na trajetória declarada, não resultados de ferramentas. Para cada resposta, preserve ID de evento/resposta, localização, instante, modelo/provedor/API/papel/task conhecidos e objeto de uso original. Campos ausentes permanecem `null`; uso ausente não elimina a resposta da cobertura.

Formato de uma entrada de `responses` (exemplo estrutural; os valores são desconhecidos, não um evento real):

```json
{
  "source": {"line": null, "event_id": null, "timestamp": null},
  "response_id": null,
  "message_timestamp": null,
  "model": null,
  "provider": null,
  "api": null,
  "skill_role": null,
  "task": null,
  "stage": null,
  "usage": null
}
```

- Preserve valores originais em `usage`, inclusive categorias novas de cache/reasoning e objeto `cost`. Não renomeie para aparentar semântica já confirmada.
- Um `response_id` repetido exige inspeção: pode ser cópia, atualização ou conflito. Duplicata idêntica: conte uma vez e registre os locais. Valores conflitantes: não selecione o mais conveniente; documente e deixe o agregado afetado indeterminado se não houver resolução.
- Na ausência de ID de resposta, use identidade do evento e evidência de repetição; não elimine duas respostas reais só por conteúdo igual. Não invente deduplicação conclusiva.
- Prefixos em ramos e `details.calls`/`nestedCalls` espelhados não são novos consumos de modelo. Auxiliares recuperados pelo analista também não são tokens históricos adicionais.
- Conte todas as respostas selecionadas, inclusive falhas/aborts com uso registrado; se uso não veio na fonte, marque lacuna e não suponha custo zero.
- Estágios analíticos são opcionais e devem ser rotulados como definição do analista. Se houver múltiplas tasks/papéis sem fronteiras confiáveis, não invente atribuição por task.

## 3. Uso e custo

Para cada campo numérico observado:
1. Verifique se mede resposta ou acumulado. Contadores que diminuem não formam um acumulador simples; campos monotônicos, isoladamente, não comprovam acumulação.
2. Verifique categorias sobrepostas antes de calcular um “total”. Igualdade aritmética valida consistência, não semântica do provedor.
3. Registre somas de campos reportados, respostas incluídas, quantidade de ausências e fórmula. Campo ausente em parte das respostas produz soma **parcial**, não total completo.

`usage_summary.reported_field_sums` pode conter somas auditáveis dos registros únicos, mesmo com interpretação pendente. Nesse caso, `interpreted_consumption` fica `null` e a limitação é explícita: soma de registros não é consumo certificado. Se os campos são cumulativos confirmados, registre valores inicial/final e método apropriado, em vez de apresentar a soma como consumo.

Não some `totalTokens` às categorias, reasoning à saída que já o inclui ou cache à entrada que já o contém. Não converta caracteres em tokens. Não confunda contexto único com prefixos processados repetidamente.

Exemplo de item de agregado:

```json
{
  "field": "input",
  "sum": null,
  "records_included": 0,
  "records_missing": 0,
  "formula": "sum(usage.input) nas respostas únicas selecionadas",
  "interpretation": "não confirmada"
}
```

O exemplo é estrutural; contagens e soma devem refletir a fonte real. Nenhuma resposta de modelo observada com cobertura suficiente: lista `responses=[]` e agregado de consumo desconhecido/não aplicável, não prova de custo zero da atividade.

Preserve valores de `usage.cost` nas respostas. Agregue apenas quando as unidades/configurações forem compatíveis; caso contrário, separe por grupo. Registre arredondamento/resíduos de ponto flutuante. Sem moeda/preços/origem confirmados, use `reported_unvalidated`; não chame o valor de fatura. Se custo não consta da fonte, use `unavailable`, somas `null` e motivo. Converter tokens por tabela de preços é estimativa separada, somente quando solicitada e fundamentada; não substitui custo reportado.

## 4. Tempo

Defina eventos extremos pela tarefa/interação, não por primeiro/último metadado do arquivo. Configurações dias depois não são tempo de implementação. Em sessão multitarefa, delimite blocos ou registre a ambiguidade.

Cada entrada em `time.intervals`:

```json
{
  "kind": "task_elapsed",
  "start": {"line": null, "event_id": null, "timestamp": null},
  "end": {"line": null, "event_id": null, "timestamp": null},
  "seconds": null,
  "formula": "end.timestamp - start.timestamp",
  "interpretation": "intervalo entre eventos, não tempo ativo"
}
```

- Outros tipos possíveis: `user_response_gap`, `request_to_response_window`, `tool_event_gap`. Registre semântica conhecida de cada timestamp, inclusive interno versus envelope; não presuma início/fim de geração.
- Tempo ativo exige telemetria que o sustente. Nem diferença residual, nem soma de janelas, nem duração do arquivo são substitutos.
- Não há pergunta intermediária ao usuário: registre `observed_requests=0` e intervalo de espera `seconds=null`, explicando ausência de medição; não declare zero de esforço humano.
- Durações de ferramentas reportadas devem conter caminho do campo, unidade e escopo (wrapper, filho, suíte). Intervalo entre eventos é cálculo distinto, não duração reportada.
- Não some wrappers com filhos, mirrors ou subprocessos aninhados. Em paralelismo, soma de durações mede carga parcial, não tempo decorrido. Duração desconhecida não é zero.

## 5. Checagem e reprodução

- Faça parsing de saída e recalcule contagens/somas contra o snapshot, não contra o texto do relatório.
- Registre seleção, chaves de deduplicação, fórmulas, grupos incompatíveis e omissões em `method`/`limitations`.
- Relatório, JSON e índice devem concordar. Hashes longos e tabelas por resposta não precisam ser repetidos no relatório.
- Relação temporal entre erro e aumento de tokens não prova que o erro causou todo o aumento. Nenhuma economia potencial ou custo causal pode ser inferido apenas desses totais.
- Não inclua o custo desta análise no custo histórico. Se medir a própria extração, use seção separada e fonte verificável; esta skill não exige isso.

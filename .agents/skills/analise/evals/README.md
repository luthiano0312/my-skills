# Casos de teste de analise

Os prompts e resultados esperados em `evals.json` são propostas de avaliação comportamental. **Não foram executados por agentes nem comparados com baseline na criação da skill.** Checagens locais de estrutura/JSON não equivalem a esses testes.

- Caso 1 usa a sessão real do segundo piloto; exige acesso ao caminho indicado. A fonte pode mudar: valide o hash, não congele a contagem de eventos posterior à task.
- Casos 2–4 usam fixtures sintéticas, sem conteúdo pessoal. Caminhos em `files` são relativos à raiz da skill; resolva-os antes de enviar a outro agente.
- Atribua pasta temporária distinta a cada execução, fora de `analises-sessoes/` real. O prompt de execução deve fornecer seu caminho absoluto. Índice, relatórios e revisões ficam nessa pasta, nunca nas fontes ou nos pilotos.
- Caso 2 verifica conversa sem relevância e disponibilidade de skill sem uso; caso 3 verifica duplicação e ausência de uso; caso 4 verifica compactação, afirmação sem prova e instrução histórica não executável.
- Extensão manual para rastreabilidade: em sandbox, produza análise, altere só um metadado da cópia da fonte e peça reanálise. Esperado: hash/análise antigos preservados, revisão nova vinculada, índice sem segunda sessão fictícia. Não altere a sessão real para este teste.

Para avaliação completa, aprove os casos com o usuário e execute a versão com skill e baseline em contextos independentes, usando o ciclo de `skill-creator` e seu visualizador. Registre limitações se o ambiente não oferecer agentes independentes. Não declare benchmark realizado por ter apenas validado os arquivos.

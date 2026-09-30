> Baseado na ISO/IEC/IEEE 29148:2018

## Visão Geral: o todo e as partes
**Engenharia de Requisitos** é o processo contínuo e guarda-chuva que cobre tudo relacionado a requisitos ao longo do ciclo de vida do sistema — desde a primeira conversa com o cliente até a gestão de mudanças depois que o sistema já está em produção.

Ela **não é uma fase única** do desenvolvimento de sistemas. Ela é dividida em sub-processos, que costumam ser tratados (de forma um pouco livre, a depender do autor/metodologia) como "fases" dentro do próprio ciclo de desenvolvimento:

```
                    ENGENHARIA DE REQUISITOS (o todo)
                              │
      ┌───────────────┬───────────────┬────────────────┐
      ▼               ▼               ▼                ▼
 1. LEVANTAMENTO   2. ANÁLISE    3. ESPECIFICAÇÃO   4. VALIDAÇÃO
   (Elicitação)    (Análise)     (Documentação)     e GESTÃO
```

A norma ISO/IEC/IEEE 29148:2018 formaliza isso alinhando com a ISO/IEC/IEEE 15288 (engenharia de sistemas) e a 12207 (engenharia de software), estruturando em dois grandes blocos:

- **StRD — Stakeholder Requirements Definition:** corresponde ao Levantamento
- **Requirements Analysis:** corresponde à Análise

E, além disso, cobre Especificação formal, Verificação/Validação, e Gestão de Requisitos — que atravessam as fases anteriores e continuam durante todo o projeto.

**Critério prático para separar Levantamento de Análise** (já que a linha entre elas é parcialmente subjetiva — não existe um órgão dizendo exatamente onde uma termina e a outra começa):

|                     | Levantamento                                            | Análise                                       |
| ------------------- | ------------------------------------------------------- | --------------------------------------------- |
| Foco                | Capturar informação que está na cabeça dos stakeholders | Organizar e estruturar o que já foi capturado |
| Direção             | Para fora (interação com cliente/usuário)               | Para dentro (trabalho da equipe técnica)      |
| Estado do requisito | Bruto, solto, ambíguo                                   | Refinado, classificado, formalizado           |

A regra de bolso: **se envolve conversar com o stakeholder para descobrir algo → Levantamento. Se envolve organizar, classificar ou modelar o que já foi descoberto → Análise.**

---

## Etapa 1 — Levantamento (Elicitação)

### Objetivo
Entender **o problema** antes de pensar na solução. Responder "o que o sistema precisa fazer e por quê?" — não "como ele vai fazer".

### O que deve ser feito
**1. Identificação dos Stakeholders**
Mapear quem são os interessados: clientes, usuários finais, gestores, equipe técnica, área jurídica, etc. Sem isso, corre-se o risco de levantar requisitos de quem não é o público certo.

**2. Coleta**
Aplicação das técnicas de elicitação (detalhadas abaixo).

**3. Análise e Negociação (preliminar)**
Stakeholders diferentes costumam pedir coisas conflitantes; é preciso negociar prioridades já nessa fase, de forma informal — a formalização plena da priorização acontece na Análise.

**4. Especificação/Documentação (inicial)**
Formalizar o que foi coletado em um documento de requisitos ou backlog de User Stories.

**5. Validação**
Confirmar com os stakeholders se o que foi documentado reflete corretamente o que eles precisam.

**6. Gestão de Requisitos**
Controlar mudanças ao longo do projeto — requisitos mudam, e é preciso rastrear isso desde o início.

### Como deve ser feito — Técnicas de Levantamento

| Técnica                            | Quando usar                                                 | Observação                                                                                                         |
| ---------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Entrevistas**                    | Aprofundar em pontos específicos                            | Estruturadas ou semiestruturadas; ótimas para esclarecer ambiguidade na hora                                       |
| **Questionários**                  | Muitos usuários espalhados geograficamente                  | Escala bem, mas é menos profundo que entrevista                                                                    |
| **Observação direta / Etnografia** | Entender o processo real de trabalho                        | Revela problemas que o próprio usuário nem menciona, por já ser "natural" pra ele                                  |
| **Workshops / JAD**                | Alinhar visões divergentes rapidamente                      | Reúne múltiplos stakeholders ao mesmo tempo                                                                        |
| **Análise de Documentos**          | Sistemas legados, processos já documentados                 | Manuais, relatórios, planilhas em uso                                                                              |
| **Protótipos**                     | Requisitos de interface, descoberta de necessidades ocultas | Nessa fase servem para **descobrir** requisitos (o usuário vê e lembra "ah, também preciso de...")                 |
| **Casos de Uso**                   | Extrair cenários de interação                               | Aqui funcionam como **técnica de elicitação** — servem para puxar requisitos que o usuário não citaria diretamente |
| **User Stories / Storytelling**    | Métodos ágeis                                               | Formato: "Como [usuário], eu quero [ação] para que [benefício]"                                                    |

### Boas práticas
- Envolver o **usuário final**, não só o gestor — quem opera o sistema no dia a dia enxerga necessidades que a liderança não vê
- Combinar mais de uma técnica (ex: entrevista + observação) para compensar os pontos cegos de cada uma
- Registrar requisitos assim que forem ditos, mesmo que de forma bruta — não confiar na memória
- Validar continuamente com o stakeholder, em vez de guardar tudo para o final

### Problemas comuns e por que evitá-los

| Problema                                                      | Por que evitar                                                                                                                              |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **Requisitos implícitos** (o cliente acha "óbvio" e não fala) | Se não for explicitado, a equipe técnica não tem como saber e o sistema sai incompleto — descoberto tarde, custa caro para corrigir         |
| **Conflito entre stakeholders** não resolvido                 | Gera retrabalho quando setores diferentes descobrem, já no sistema pronto, que pediram coisas incompatíveis                                 |
| **Requisitos voláteis** sem controle                          | Sem gestão de mudança, o escopo cresce descontroladamente (scope creep) e o cronograma/orçamento saem do controle                           |
| **Excesso de detalhe técnico cedo demais**                    | Nessa fase o foco é o *problema*, não a *solução* — antecipar tecnologia limita opções de design e engessa decisões que deveriam vir depois |
| **Vago demais para ser útil**                                 | Requisito impreciso não é testável, dificultando saber se foi realmente atendido                                                            |
| **Falta de envolvimento do usuário final**                    | Requisitos "de gabinete" costumam não refletir a realidade operacional                                                                      |

### Obrigatoriedade dos entregáveis
**SRS completo (Software Requirements Specification)**
- **Pode ficar de fora quando:** metodologia ágil (o backlog substitui na prática); time pequeno/projeto interno sem exigência contratual; MVP de startup, onde requisitos mudam rápido demais para justificar documento formal
- **É praticamente obrigatório quando:** contratos governamentais/licitações públicas; sistemas regulados (saúde, aviação, financeiro) que exigem auditoria; terceirização (o documento vira o contrato entre cliente e fornecedor); sistemas críticos de segurança (embarcado médico, automotivo)
- **Por quê:** em contextos regulados/contratuais, o SRS é a prova formal do que foi acordado — sem ele não há base para auditoria nem para resolver disputas

**Backlog de User Stories**
- **Fica de fora quando:** metodologia tradicional/cascata (o SRS já cumpre esse papel)
- **É essencial quando:** qualquer time ágil (Scrum, Kanban)
- SRS e Backlog raramente coexistem — são abordagens alternativas para o mesmo propósito

**Diagramas de Casos de Uso (UML)**
- **Pode ficar de fora quando:** sistema pequeno/simples; time já usa User Stories + critérios de aceitação (cobrem os fluxos de forma mais enxuta); projeto muito ágil, onde documentação visual formal desacelera mais do que ajuda
- **Vale manter quando:** muitos atores diferentes com permissões/fluxos distintos; fluxos de negócio complexos com várias exceções; necessidade de comunicar lógica para stakeholders não-técnicos

**Protótipos**
- **Pode ficar de fora quando:** sistema sem interface relevante (API backend, processamento em lote, script de integração); interface simples e já conhecida (CRUD básico padrão)
- **É praticamente indispensável quando:** interface complexa ou voltada ao usuário final; incerteza sobre a experiência do usuário (protótipo barato evita retrabalho caro depois)

### Entregáveis desta etapa
- Documento de Requisitos (SRS) **ou** Backlog de User Stories (não os dois)
- Diagramas de Casos de Uso (quando aplicável)
- Protótipos validados (quando aplicável)
- Matriz de rastreabilidade de requisitos (versão inicial)
- Registro de stakeholders identificados

---

## Etapa 2 — Análise

### Objetivo
Transformar os requisitos brutos coletados em algo estruturado, classificado e formal que a equipe técnica consegue usar para projetar o sistema. É a ponte entre "o que o cliente quer" e "o que vamos construir".

### O que deve ser feito
**1. Classificação dos requisitos**
- **Requisitos Funcionais (RF):** o que o sistema deve *fazer* (ex: "permitir cadastro de usuários")
- **Requisitos Não-Funcionais (RNF):** *como* o sistema deve se comportar (performance, segurança, usabilidade, disponibilidade, escalabilidade)

**2. Verificação de qualidade de cada requisito**
Segundo a ISO/IEC/IEEE 29148:2018, um bom requisito individual deve ser:

| Atributo | Significado |
|---|---|
| Necessário | Realmente precisa existir |
| Não ambíguo | Só uma interpretação possível |
| Completo | Não deixa lacunas |
| Singular | Trata de uma única coisa por vez |
| Factível/viável | Possível de implementar no prazo/orçamento |
| Verificável | Dá para testar se foi atendido |
| Correto | Reflete a real necessidade do stakeholder |
| Conforme | Segue o padrão/template adotado |

E o **conjunto** de requisitos deve ser: completo, consistente e delimitado (bounded).

**3. Priorização**
Técnicas comuns: MoSCoW (Must/Should/Could/Won't have), matriz de impacto x urgência.

**4. Definição do escopo do sistema**

**5. Extração e catalogação das regras de negócio**

**6. Modelagem inicial**

### Como deve ser feito

**Definição do escopo — o que considerar:**
- **Limites do sistema (system boundaries):** o que é responsabilidade do sistema vs. o que é externo a ele (ex: um gateway de pagamento é *usado*, mas não é *parte* do sistema)
- **Restrições de negócio:** prazo, orçamento, equipe disponível
- **Restrições técnicas:** infraestrutura existente, tecnologias já adotadas, compatibilidade com legado
- **Critérios de aceitação do escopo:** o que caracteriza "pronto" para aquela entrega
- **Registro formal:** Documento de Visão, Termo de Abertura — evita scope creep
- Boa prática: separar claramente "in scope" e "out of scope"

**Regras de negócio — onde entram:**
- Dentro dos requisitos funcionais (ex: "pedido só pode ser cancelado em até 24h")
- Como restrições de dados/validações (ex: "desconto máximo é 15%, exceto para VIP")
- Como fluxos de decisão (ex: "se estoque zerado, bloquear venda e notificar compras")
- Boa prática: documentá-las num catálogo/tabela separado, numeradas e referenciadas nos casos de uso — melhora rastreabilidade e evita regra "escondida" dentro de um requisito genérico

**Modelagem inicial — artefatos:**
- **Casos de uso:** aqui já como **artefato formal de modelagem** (diferente do uso na elicitação) — diagrama UML + descrição textual (fluxo principal, alternativo, pré/pós-condições)
- **Diagramas de fluxo/fluxograma:** para regras de negócio complexas e decisões
- **Modelagem de dados conceitual (DER):** entidades principais e relacionamentos, ainda sem tipos técnicos
- **Diagrama de Classes (conceitual):** se a abordagem é orientada a objetos
- **Protótipos de baixa fidelidade:** aqui usados para **validar** entendimento (diferente da elicitação, onde servem para descobrir)
- **Glossário de termos:** garante vocabulário comum entre cliente, analista e desenvolvedor

### Boas práticas
- Manter rastreabilidade: cada requisito, regra de negócio e caso de uso deve poder ser ligado de volta a uma necessidade de stakeholder
- Revisar os requisitos com os critérios de qualidade (tabela acima) antes de considerar a fase encerrada
- Separar regras de negócio em catálogo próprio quando forem numerosas ou reutilizadas por vários módulos
- Fazer a definição de escopo por escrito e validada, nunca deixar implícita

### Problemas comuns e por que evitá-los

| Problema | Por que evitar |
|---|---|
| **Misturar RF e RNF sem classificar** | Dificulta priorização e testes — um requisito de performance tratado como funcional pode ser esquecido no plano de testes |
| **Regras de negócio espalhadas dentro dos requisitos, sem catálogo** | Fica difícil rastrear e atualizar quando a regra muda; risco de a mesma regra ser implementada de forma inconsistente em módulos diferentes |
| **Escopo não formalizado** | Abre espaço para scope creep e discussões com o cliente sobre "isso estava incluído ou não" |
| **Pular a verificação de qualidade dos requisitos** | Requisitos ambíguos ou não testáveis só serão descobertos como problema na fase de testes — o custo de corrigir cresce muito ao longo do ciclo |
| **Modelagem excessivamente detalhada cedo demais** | Nessa fase a modelagem ainda é conceitual; entrar em detalhe técnico (tipos de dado, índices de banco) é papel do Projeto/Design, não da Análise |

### Obrigatoriedade dos entregáveis
**Matriz de Rastreabilidade**
- **Fica de fora quando:** projeto pequeno, poucos requisitos, equipe pequena (controle "de cabeça" ainda viável); sem exigência de auditoria/certificação
- **É obrigatória quando:** sistemas regulados (ISO 9001, CMMI); projetos grandes com múltiplas equipes em paralelo; auditoria de compliance (sistemas financeiros, LGPD/GDPR)
- **Por quê:** sem ela, rastrear o impacto de uma mudança de requisito por todo o sistema se torna inviável em escala

**Glossário de Termos**
- **Fica de fora quando:** domínio simples, sem jargão técnico específico; equipe e cliente já compartilham vocabulário
- **É importante quando:** domínio complexo/especializado (jurídico, médico, financeiro); cliente e equipe técnica vêm de "mundos" diferentes

**Documento de Regras de Negócio (catálogo separado)**
- **Fica de fora quando:** regras são poucas e simples o suficiente para caber dentro dos próprios RFs
- **Merece documento separado quando:** regras são numerosas, mudam com frequência, ou são reaproveitadas por múltiplos módulos/sistemas — nesse cenário, considerar até um *Business Rules Engine*

### Entregáveis desta etapa
- Documento de Especificação de Requisitos (SRS/ERS) com RF e RNF classificados e priorizados
- Documento de Visão / definição formal de escopo (in scope / out of scope)
- Catálogo de Regras de Negócio (quando aplicável)
- Diagrama de Casos de Uso (formalizado)
- Diagrama Entidade-Relacionamento conceitual
- Diagrama de Classes conceitual (se orientado a objetos)
- Glossário de termos (quando aplicável)
- Matriz de rastreabilidade (atualizada/expandida)

---

## Além do Levantamento e Análise: o resto do "guarda-chuva"

A ISO/IEC/IEEE 29148:2018 não para na Análise — ela cobre também:

**Especificação formal**
Consolidação de tudo em documentos padronizados: StRS (Stakeholder Requirements Specification), SyRS (System Requirements Specification), SRS (Software Requirements Specification), ConOps/OpsCon (Concept of Operations).

**Verificação e Validação**
Checar se os requisitos especificados estão corretos (verificação) e se de fato atendem à necessidade real do stakeholder (validação) — isso se conecta com os Testes de Aceitação lá na frente do ciclo de desenvolvimento.

**Gestão de Requisitos**
Processo contínuo de controlar mudanças, manter baseline e rastreabilidade ao longo de **todo** o projeto — não termina quando a codificação começa.

---

## Resumo: onde tudo se encaixa no ciclo de desenvolvimento

```
┌─────────────────────── ENGENHARIA DE REQUISITOS ───────────────────────┐
│                                                                          │
│  1. LEVANTAMENTO  →  2. ANÁLISE  →  3. ESPECIFICAÇÃO  →  4. VALIDAÇÃO  │
│     (elicitação)      (estruturação)   (documentação)      e GESTÃO    │
│                                                              (contínua) │
└──────────────────────────────────┬───────────────────────────────────┘
                                    ▼
                    Projeto (Design) → Implementação → Testes → Deploy → Manutenção
```

**Regra de ouro para decidir o que fazer/documentar em cada projeto:** todo entregável existe para reduzir risco de mal-entendido ou retrabalho. Se o risco que ele mitiga é baixo naquele contexto específico, ele pode (e deve) ser simplificado ou eliminado — documentação por documentação não agrega valor.

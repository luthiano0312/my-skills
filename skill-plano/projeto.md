# Projeto (Design) e System Design

## Relação com a Engenharia de Requisitos
O Projeto (Design) é uma fase **distinta** da Engenharia de Requisitos (Levantamento + Análise), com um objetivo diferente — mas não é uma fase hermética. Existem pontos reais de sobreposição e retroalimentação entre elas.

### Por que é uma fase distinta

| | Engenharia de Requisitos (Levantamento + Análise) | Projeto (Design) |
|---|---|---|
| Pergunta central | **O quê** o sistema deve fazer, e **por quê** | **Como** o sistema vai fazer isso |
| Produto do pensamento | Requisitos, regras de negócio, modelos conceituais | Arquitetura, estrutura técnica, decisões de implementação |
| Nível de abstração | Independente de tecnologia | Amarrado a tecnologia/plataforma |

Na teoria, a linha é clara: a Análise entrega um SRS/ERS já validado, e o Design **parte dele** como insumo, sem voltar a discutir *o que* o sistema deve fazer.

### Onde os pontos em comum aparecem, na prática
**1. O RNF é a ponte mais direta**
Requisitos não-funcionais (performance, escalabilidade, segurança, disponibilidade) são levantados/analisados na Engenharia de Requisitos, mas é **no Design** que eles viram decisão concreta. Ex: "disponibilidade de 99,9%" (RNF) leva a decisões de Design como replicação de banco, load balancer, arquitetura multi-região. O RNF nasce numa fase e "morre" (é resolvido) na outra.

**2. Modelagem conceitual vs. modelagem técnica é um espectro, não um degrau**
Artefatos como o DER conceitual e o diagrama de classes conceitual (produzidos na Análise) são **refinados** no Design, não recriados do zero — o DER conceitual vira modelo físico de banco (tipos de dados, chaves, índices), o diagrama de classes conceitual vira design de classes com métodos e responsabilidades definidas.

**3. Restrições técnicas identificadas na Análise reaparecem no Design como ponto de partida**
Se na definição de escopo já foi registrado "precisa ser compatível com o sistema legado X", isso vira restrição de arquitetura no Design.

**4. Descoberta de requisitos "esquecidos" durante o Design**
É comum (principalmente em times ágeis) o Design revelar que um requisito estava mal especificado ou incompleto, forçando uma volta pontual à Análise. Isso é normal e esperado; só em processos muito rígidos (cascata puro) essa volta é vista como falha de processo.

**5. Casos de uso continuam sendo referência**
Os casos de uso formalizados na Análise geralmente guiam o desenho de APIs e contratos entre serviços no Design — cada caso de uso costuma virar um ou mais endpoints/fluxos técnicos.

---

## A fase de Projeto (Design)

### O que é feito
O Design se divide em dois níveis:
**High-Level Design (HLD)**
- Arquitetura geral do sistema (monolito, microsserviços, arquitetura em camadas, event-driven, etc.)
- Como os componentes principais se comunicam entre si
- Escolha de tecnologias: linguagens, frameworks, banco de dados
- Fluxo de dados macro entre módulos/serviços

**Low-Level Design (LLD)**
- Estrutura de classes e módulos, já com detalhe de implementação
- Modelagem física do banco de dados: schemas, tabelas, tipos, índices, chaves
- Definição de contratos de API (endpoints, payloads, códigos de erro)
- Algoritmos e estruturas de dados específicas para partes críticas

Inclui também o **Design de UI/UX**: interface do usuário, navegação, wireframes de alta fidelidade — em paralelo ao design técnico da arquitetura.

### Como deve ser feito
- Partir sempre dos requisitos (especialmente os RNFs) já validados na Análise, não de preferências tecnológicas da equipe
- Tomar decisões de HLD antes de entrar em LLD — arquitetura geral primeiro, detalhes de implementação depois
- Validar cada decisão arquitetural contra as restrições técnicas e de negócio identificadas anteriormente (orçamento, prazo, equipe, infraestrutura existente)
- Formalizar contratos de API e schemas de dados antes da implementação começar, para que times diferentes possam trabalhar em paralelo

### Boas práticas
- Documentar as decisões de arquitetura e o **porquê** delas (Architecture Decision Records — ADRs), não só o resultado final
- Validar as decisões de Design contra os RNFs levantados, não só contra os RFs
- Prototipar/testar decisões arriscadas antes de comprometer todo o sistema com elas (spike técnico)
- Pensar em trade-offs explicitamente — praticamente toda decisão de Design troca uma coisa por outra (ex: mais consistência custa latência)
- Revisar a arquitetura em pontos de checkpoint, não só uma vez no início — sistemas evoluem e o Design deve poder ser revisitado

### Problemas comuns e por que evitá-los

| Problema | Por que evitar |
|---|---|
| **Over-engineering** (desenhar para escala que o sistema nunca vai ter) | Complexidade desnecessária aumenta custo de manutenção e reduz velocidade de entrega, sem benefício real |
| **Under-engineering** (ignorar RNFs de escala já conhecidos) | O sistema funciona no MVP mas quebra quando o uso real cresce — retrabalho caro de reescrever arquitetura já em produção |
| **Pular direto para tecnologia antes de entender o problema** | Escolher a stack antes de entender os RNFs reais leva a decisões que não se sustentam depois |
| **Ignorar restrições identificadas na Análise** (legado, orçamento, equipe) | Um Design tecnicamente "ideal", mas inviável de implementar com a equipe/prazo disponível, não serve pra nada |
| **Não documentar o porquê das decisões** | Sem esse registro, decisões futuras (ou de outras pessoas) acabam contradizendo escolhas já feitas por bons motivos, ou refazendo análises já feitas |

### Entregáveis
- Documento de Arquitetura (HLD) — diagramas de componentes, fluxo de dados, escolhas tecnológicas justificadas
- Documento de Design Detalhado (LLD) — diagrama de classes técnico, schema de banco físico
- Especificação de APIs/contratos entre serviços (ex: OpenAPI/Swagger)
- Architecture Decision Records (ADRs), quando relevante
- Protótipo técnico / spike de validação de decisões arriscadas, quando aplicável
- Design de UI/UX detalhado (wireframes de alta fidelidade, protótipos navegáveis)

---

## System Design

### O que é
**System Design** é, em essência, o **HLD levado a sério**, com foco particular em sistemas que precisam operar em escala — muitos usuários simultâneos, grandes volumes de dados, alta disponibilidade. Estruturalmente, é um aprofundamento do Design de Alto Nível, não uma fase separada do ciclo de desenvolvimento.

Costuma parecer uma disciplina à parte porque, em contextos de **entrevistas técnicas**, "System Design" virou praticamente um campo próprio de estudo — mas o conteúdo é o mesmo HLD, com ênfase em sistemas distribuídos de larga escala.

### Principais temas
- **Escalabilidade:** escalar verticalmente (máquina mais forte) vs. horizontalmente (mais instâncias)
- **Disponibilidade e tolerância a falhas:** redundância, failover, replicação
- **Balanceamento de carga:** distribuir requisições entre instâncias
- **Cache:** onde e como cachear para reduzir carga no banco/serviços
- **Filas de mensagens / processamento assíncrono:** desacoplar componentes, absorver picos de carga
- **Trade-offs de consistência:** teorema CAP (Consistência, Disponibilidade, Tolerância a Partição — não dá para ter os três ao mesmo tempo em um sistema distribuído), consistência forte vs. eventual
- **Particionamento/sharding de dados:** dividir dados entre múltiplos bancos para escalar
- **Estimativas de capacidade:** calcular volume de tráfego, armazenamento e throughput esperado, para dimensionar a arquitetura

### Quando aprofundar nesses temas
Nem todo sistema precisa desse nível de profundidade em System Design — é proporcional à escala esperada:
- **Sistemas pequenos/internos, baixo volume de usuários:** HLD básico já resolve; aprofundar em sharding, CAP theorem, etc. seria over-engineering
- **Sistemas com crescimento esperado, alto tráfego, ou natureza distribuída:** aqui o aprofundamento em System Design se justifica e evita retrabalho caro de reescrever a arquitetura depois

---

## Resumo: posição no ciclo de desenvolvimento

```
Requisitos → Análise → [PROJETO/DESIGN (HLD + LLD, incluindo System Design)] → Implementação → Testes → Deploy → Manutenção
```

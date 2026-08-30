# FinOps e Otimização de Custos

## Objetivo

A implementação em nuvem deste projeto foi realizada no Microsoft Azure. Além da construção técnica da arquitetura, foram consideradas práticas de FinOps para acompanhar, controlar e otimizar os custos dos recursos utilizados.

O objetivo é manter uma arquitetura suficiente para o volume atual do projeto, evitando o provisionamento de recursos acima da necessidade.

## Recursos utilizados no Azure

A solução utiliza principalmente dois serviços:

### Azure Storage Account

Foi utilizada uma conta de armazenamento na região Brazil South, com desempenho Standard e redundância LRS (Locally Redundant Storage).

O armazenamento foi organizado em containers que representam as etapas da arquitetura de dados:

- bronze
- silver
- gold
- streaming

A camada Bronze mantém os dados ingeridos das fontes.

A camada Silver contém os dados tratados, padronizados e preparados para análise.

A camada Gold contém os dados analíticos e enriquecidos, incluindo a integração entre os dados educacionais e os dados territoriais do IBGE.

O container streaming é utilizado para persistência dos eventos processados durante a demonstração do pipeline em tempo real.

A utilização de arquivos Parquet nas camadas Silver e Gold também contribui para a otimização de armazenamento e processamento, pois é um formato colunar e comprimido.

### Azure Event Hubs

O Azure Event Hubs foi utilizado para demonstrar a ingestão de eventos em tempo real.

Configuração utilizada no projeto:

- Namespace: eh-tech-challenge-gabriel
- Event Hub: alfabetizacao-stream
- Região: Brazil South
- Plano: Basic
- Unidades de produtividade: 1
- Partições: 2
- Retenção configurada: 1 hora

Foi escolhida a menor configuração suficiente para a demonstração do projeto.

O uso de apenas uma unidade de produtividade reduz o custo e ainda fornece capacidade muito superior ao pequeno volume de eventos utilizado no protótipo.

## Estratégias de FinOps adotadas

As principais decisões para controle de custos foram:

1. Utilização do plano Basic do Azure Event Hubs, evitando planos Standard, Premium ou Dedicated sem necessidade.

2. Utilização de apenas uma unidade de produtividade no Event Hubs.

3. Retenção curta dos eventos, pois o projeto não necessita manter eventos no serviço de streaming por longos períodos.

4. Utilização de armazenamento Standard com redundância LRS, adequada ao contexto acadêmico e mais econômica que estratégias de redundância geográfica.

5. Uso de arquivos Parquet nas camadas Silver e Gold para reduzir volume de armazenamento e melhorar a eficiência das leituras analíticas.

6. Processamento local das transformações em Python, evitando a criação de máquinas virtuais ou clusters permanentes apenas para execução do desafio.

7. Utilização de uma amostra de 10.000 registros da tabela de alunos na etapa analítica, reduzindo transferência, processamento e armazenamento durante o desenvolvimento.

8. Seleção somente das colunas necessárias durante a consulta da tabela de alunos no BigQuery, evitando processamento desnecessário.

9. Separação dos dados em Bronze, Silver e Gold, facilitando políticas futuras de retenção e ciclo de vida por camada.

10. Monitoramento dos recursos pelo Azure Cost Management para identificar crescimento inesperado de consumo.

## Estimativa e comportamento dos custos

O custo exato da solução depende do período em que os recursos permanecem provisionados, quantidade de eventos, volume armazenado, operações realizadas e condições comerciais da assinatura Azure.

Por esse motivo, o projeto não utiliza um valor fixo fictício como custo mensal.

No Azure Event Hubs, o plano Basic possui cobrança relacionada à unidade de produtividade provisionada e ao volume de eventos de entrada.

Cada evento de entrada de até 64 KB é considerado uma unidade faturável. Eventos maiores podem consumir múltiplas unidades.

A unidade de produtividade do Event Hubs oferece capacidade de até 1 MB/s de entrada e 2 MB/s de saída. Para o volume reduzido deste projeto, uma unidade é suficiente.

No Azure Storage, o custo depende principalmente do volume armazenado, quantidade e tipo de operações e movimentação de dados.

Como o projeto utiliza arquivos pequenos e volume limitado de dados, o consumo de armazenamento é reduzido.

## Cenário de crescimento

Em um cenário produtivo, o custo deve ser reavaliado conforme o aumento do volume de dados.

Caso o número de eventos aumente significativamente, seria necessário acompanhar métricas de throughput e avaliar o aumento das unidades de produtividade do Event Hubs.

Para armazenamento histórico, poderiam ser aplicadas políticas de ciclo de vida, movendo dados antigos para camadas de armazenamento de menor custo.

Também seria possível estabelecer budgets e alertas no Azure Cost Management para avisar quando os gastos atingirem determinados limites.

## Conclusão FinOps

A arquitetura foi dimensionada de acordo com a necessidade atual do projeto, priorizando serviços gerenciados e configurações de menor custo.

A principal estratégia FinOps adotada foi evitar superdimensionamento. O ambiente utiliza apenas os recursos necessários para demonstrar ingestão batch, arquitetura medalhão, enriquecimento com fonte externa e processamento de eventos em streaming.

Em um ambiente produtivo, o monitoramento contínuo de custo, volume, throughput e retenção permitiria redimensionar os recursos conforme a demanda.
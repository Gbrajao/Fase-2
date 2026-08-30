# Tech Challenge – Fase 2

## Pipeline de Dados para Análise da Alfabetização no Brasil

Neste projeto eu desenvolvi uma pipeline de Engenharia de Dados utilizando dados públicos relacionados à alfabetização no Brasil.

O objetivo foi construir uma solução que passasse pelas principais etapas de uma pipeline de dados, desde a ingestão dos arquivos até a disponibilização dos dados tratados para análise.

Para organizar esse processo, utilizei a Arquitetura Medalhão, separando os dados nas camadas Bronze, Silver e Gold.

Também trabalhei com dois tipos de processamento: Batch, para os dados históricos, e Streaming, para simular a chegada de novos eventos.

Além do processamento local, implementei parte da solução na nuvem utilizando Microsoft Azure. Para armazenamento utilizei Azure Blob Storage e, para o streaming, Azure Event Hubs.

Durante o desenvolvimento também integrei uma fonte externa oficial do IBGE, implementei verificações de qualidade, monitoramento da pipeline e algumas práticas de FinOps para controle dos custos da solução.

---

## Contexto

Os dados utilizados neste projeto estão relacionados à avaliação da alfabetização no Brasil.

A ideia foi organizar informações de resultados e metas de alfabetização de forma que elas pudessem ser utilizadas posteriormente para análises por Brasil, estado, município e região.

Para isso, construí uma pipeline capaz de receber os dados brutos, realizar tratamentos, validar a qualidade e gerar conjuntos de dados preparados para análise.

A arquitetura também foi pensada para permitir evoluções futuras, como dashboards e modelos de Machine Learning.

---

## Fonte dos dados

A principal fonte utilizada foi o conjunto de dados de Avaliação da Alfabetização, disponibilizado pelo INEP através da plataforma Base dos Dados.

No projeto utilizei seis tabelas:

- UF;
- Meta Alfabetização Brasil;
- Meta Alfabetização por UF;
- Meta Alfabetização por Município;
- Município;
- Alunos.

As tabelas agregadas foram obtidas através dos arquivos disponibilizados pela Base dos Dados.

### Tabela de alunos

No caso da tabela de alunos, encontrei uma limitação para realizar o download completo do arquivo, que possui aproximadamente 256 MB.

Por esse motivo, utilizei o BigQuery para consultar os dados e extrair uma amostra de 10.000 registros referentes ao ano de 2024.

Na consulta selecionei somente as colunas necessárias para o projeto e apliquei um filtro para 2024. A consulta processou aproximadamente 169 MB.

Essa escolha também ajudou a evitar processamento desnecessário durante o desenvolvimento.

É importante destacar que esses 10.000 registros representam uma amostra utilizada para construir e demonstrar a arquitetura.

Por isso, resultados calculados diretamente a partir dessa amostra não devem ser interpretados como representativos de todos os alunos do Brasil.

---

## Fonte externa – IBGE

Além dos dados educacionais, também integrei uma fonte externa oficial do IBGE.

Utilizei a API do IBGE para buscar informações territoriais dos municípios brasileiros.

A ingestão retornou 5.571 registros.

O arquivo obtido foi armazenado inicialmente na Bronze:

```text
data/bronze/ibge_municipios.csv
```

Depois realizei o tratamento dos dados e gerei o arquivo da Silver:

```text
data/silver/ibge_municipios.parquet
```

Para integrar os dados do IBGE com os dados educacionais, utilizei:

```text
id_municipio
```

Durante o tratamento, padronizei esse identificador com sete dígitos para manter a consistência entre as diferentes fontes.

Na Gold, criei o arquivo:

```text
data/gold/municipio_enriquecido_ibge.parquet
```

Essa tabela combina os indicadores educacionais com informações de município, UF e região.

A integração gerou 10.704 registros e todos encontraram correspondência com os dados do IBGE.

Com isso, além das análises educacionais, também é possível realizar comparações territoriais.

---

## Arquitetura da solução

Dividi a arquitetura em dois fluxos principais:

- Batch;
- Streaming.

O Batch é utilizado para processar os dados históricos do INEP/Base dos Dados e do IBGE.

O Streaming foi utilizado para representar a chegada de novos eventos.

A arquitetura ficou organizada da seguinte forma:

```text
                 DADOS HISTÓRICOS

          Base dos Dados / INEP       IBGE
                    |                   |
                    +---------+---------+
                              |
                              v
                            BRONZE
                         Dados brutos
                              |
                              v
                            SILVER
                        Dados tratados
                              |
                              v
                             GOLD
                       Dados analíticos
                              |
                              v
                    Análises / BI / IA


                    DADOS EM STREAMING

                       Eventos simulados
                              |
                              v
                       Producer Python
                              |
                  +-----------+-----------+
                  |                       |
                  v                       v
            Apache Kafka           Azure Event Hubs
               Local                    Cloud
                  |                       |
                  v                       v
           Consumer Python        Consumer Python
                  |                       |
                  +-----------+-----------+
                              |
                              v
                       Bronze Streaming
```

Dessa forma, consegui demonstrar tanto o processamento de dados históricos quanto o processamento de eventos.

---

## Arquitetura Medalhão

Para organizar os dados utilizei a Arquitetura Medalhão.

O fluxo principal é:

```text
Fonte
  |
  v
Bronze
  |
  v
Silver
  |
  v
Gold
```

Cada camada possui uma responsabilidade diferente dentro da pipeline.

---

## Camada Bronze

Na camada Bronze mantive os dados o mais próximo possível da forma como foram obtidos na origem.

Os arquivos estão armazenados em:

```text
data/bronze/
```

Nessa camada estão os arquivos referentes a:

- UF;
- Meta Brasil;
- Meta UF;
- Meta Município;
- Município;
- amostra de alunos;
- municípios do IBGE.

Também existe a pasta:

```text
data/bronze/streaming/
```

Ela é utilizada para armazenar os eventos recebidos durante os testes de streaming.

No streaming realizado com Azure, por exemplo, os eventos recebidos foram armazenados em:

```text
eventos_azure.jsonl
```

Optei por preservar os dados na Bronze para permitir que as etapas seguintes possam ser executadas novamente sem necessidade de buscar os dados novamente nas fontes.

---

## Camada Silver

Na Silver realizei o tratamento e a padronização dos dados.

O processamento está implementado em:

```text
src/processing/process_silver.py
```

Entre os tratamentos realizados estão:

- verificação de duplicidades;
- tratamento dos identificadores;
- padronização das siglas das UFs;
- tratamento dos tipos;
- validação das taxas de alfabetização;
- identificação de valores ausentes;
- normalização do `id_municipio`;
- preparação das chaves para os relacionamentos;
- conversão dos arquivos para Parquet.

Os arquivos gerados são:

```text
data/silver/

├── uf.parquet
├── meta_brasil.parquet
├── meta_uf.parquet
├── meta_municipio.parquet
├── municipio.parquet
├── alunos.parquet
└── ibge_municipios.parquet
```

Durante o tratamento optei por não substituir automaticamente valores ausentes por zero.

Tomei essa decisão porque um valor ausente não significa necessariamente que o indicador seja igual a zero.

Preencher esses valores sem conhecer o motivo da ausência poderia alterar o significado dos dados.

Também tratei o `id_municipio` como identificador e não como uma variável utilizada em cálculos.

---

## Camada Gold

Na camada Gold organizei os dados para facilitar o consumo analítico.

O processamento está implementado em:

```text
src/processing/create_gold.py
```

Foram gerados os seguintes arquivos:

```text
data/gold/

├── resultado_meta_brasil.parquet
├── resultado_meta_uf.parquet
├── resultado_meta_municipio.parquet
├── alunos_municipio_analitico.parquet
└── municipio_enriquecido_ibge.parquet
```

Nessa camada preparei os dados para análises como:

- comparação entre resultado e meta de alfabetização;
- identificação de estados e municípios que atingiram suas metas;
- análises municipais;
- análise da amostra de alunos;
- comparação entre estados;
- comparação entre regiões.

A tabela:

```text
municipio_enriquecido_ibge.parquet
```

foi criada a partir da integração dos indicadores educacionais com os dados territoriais do IBGE.

Utilizei o `id_municipio` como chave para realizar essa integração.

---

## Qualidade dos dados

Também criei uma etapa específica para verificar a qualidade dos dados.

O código está em:

```text
src/quality/validate_data.py
```

Nessa etapa verifico:

- registros duplicados;
- valores ausentes;
- valores nulos nas chaves;
- percentuais fora do intervalo esperado;
- relacionamentos entre as tabelas;
- relacionamento com o IBGE;
- proficiência dos alunos;
- integridade da Gold enriquecida.

Nas bases analisadas não encontrei registros duplicados.

As taxas de alfabetização também ficaram dentro do intervalo esperado entre 0 e 100.

Nos relacionamentos municipais, as chaves utilizadas entre Meta Município, Município, Alunos e IBGE apresentaram correspondência.

Na integração da Gold com o IBGE obtive:

```text
Registros: 10.704
Registros sem correspondência no IBGE: 0
```

### Meta UF e UF

Durante a validação encontrei uma diferença entre as tabelas Meta UF e UF.

As seguintes siglas estavam presentes na Meta UF sem correspondência na tabela UF:

```text
DF
RR
```

Optei por não excluir ou alterar esses registros.

Mantive essa diferença documentada porque ela foi encontrada nos próprios dados utilizados no projeto.

### Proficiência dos alunos

Outro ponto que analisei foi a ausência de valores de proficiência.

Na amostra existem 3.581 registros com proficiência nula.

Ao investigar esses casos, encontrei:

```text
3.574 alunos ausentes
7 alunos presentes
```

Nos casos dos alunos ausentes, a falta da proficiência é coerente com a ausência na avaliação.

Porém, também existem sete alunos classificados como presentes sem valor de proficiência.

Como eu não tinha informação suficiente para determinar qual deveria ser o valor, preferi manter esses registros como nulos em vez de criar valores artificialmente.

---

## Processamento Batch

Utilizei processamento Batch para os dados históricos.

O fluxo é:

```text
Fonte
  |
  v
Bronze
  |
  v
Silver
  |
  v
Gold
```

Escolhi esse modelo para as bases históricas porque esses dados não precisam ser processados individualmente em tempo real.

O Batch também possui menor complexidade e atende bem ao processamento periódico desse tipo de informação.

---

## Processamento Streaming

Também implementei processamento em Streaming.

Nesse caso, utilizei eventos simulados representando novas medições relacionadas à alfabetização.

A simulação foi necessária porque não utilizei uma fonte operacional que estivesse gerando esses eventos em tempo real.

Apesar dos eventos serem simulados, a infraestrutura utilizada para transmitir e consumir os eventos é real.

Implementei duas versões:

```text
Apache Kafka
Azure Event Hubs
```

---

## Streaming com Apache Kafka

Primeiro implementei o streaming localmente utilizando Apache Kafka através do Docker.

Os arquivos são:

```text
src/streaming/producer.py
src/streaming/consumer.py
```

O funcionamento é:

```text
Producer Python
      |
      v
Apache Kafka
      |
      v
Consumer Python
      |
      v
Bronze Streaming
```

O Producer gera os eventos e envia para o Kafka.

O Consumer fica aguardando as mensagens e processa os eventos conforme eles chegam.

Essa implementação foi utilizada para testar e validar o funcionamento do streaming localmente.

---

## Streaming com Azure Event Hubs

Depois de testar o Kafka local, implementei uma segunda versão utilizando Azure Event Hubs.

Criei o namespace:

```text
eh-tech-challenge-gabriel
```

e o Event Hub:

```text
alfabetizacao-stream
```

A configuração utilizada foi:

```text
Plano: Basic
Unidades de produtividade: 1
Partições: 2
Retenção: 1 hora
Região: Brazil South
```

Os scripts utilizados são:

```text
src/streaming/producer_azure.py
src/streaming/consumer_azure.py
```

O fluxo funciona da seguinte forma:

```text
Producer Python
      |
      v
Azure Event Hubs
      |
      v
alfabetizacao-stream
      |
      v
Consumer Python
      |
      v
eventos_azure.jsonl
```

Durante os testes consegui visualizar os eventos sendo enviados pelo Producer e recebidos pelo Consumer através do Azure.

Também tomei o cuidado de não colocar as credenciais diretamente no código.

A connection string fica armazenada localmente no arquivo:

```text
.env
```

Esse arquivo está configurado no `.gitignore` e não é enviado para o GitHub.

---

## Implementação no Azure

Para implementar parte da arquitetura em nuvem utilizei Microsoft Azure.

Criei uma Storage Account na região Brazil South.

A configuração escolhida foi:

```text
Performance: Standard
Redundância: LRS
```

Dentro do Storage criei quatro containers:

```text
bronze
silver
gold
streaming
```

A ideia foi reproduzir no Azure a mesma separação utilizada localmente.

Também utilizei Azure Event Hubs para implementar o streaming em cloud.

Dessa forma, o projeto possui tanto armazenamento em nuvem quanto um serviço gerenciado para recebimento dos eventos.

---

## Monitoramento

Também criei um monitoramento simples para acompanhar o funcionamento da pipeline.

O código está em:

```text
src/monitoring/monitor_pipeline.py
```

O script gera logs em:

```text
logs/pipeline_monitoring.jsonl
```

Nesse monitoramento verifico:

- status da pipeline;
- tempo de execução;
- quantidade de arquivos em cada camada;
- volume armazenado na Bronze;
- volume armazenado na Silver;
- volume armazenado na Gold;
- possíveis camadas sem arquivos;
- erros encontrados durante a execução.

Em uma das execuções obtive:

```text
Bronze: 9 arquivos | 1.62 MB
Silver: 7 arquivos | 0.99 MB
Gold: 5 arquivos | 0.75 MB

Status: SUCESSO
```

Quando não são encontrados problemas estruturais, o status fica como:

```text
SUCESSO
```

Caso uma camada esteja sem arquivos, o script gera:

```text
ATENCAO
```

Se ocorrer alguma exceção durante o monitoramento, ela é registrada como:

```text
ERRO
```

Para o escopo deste projeto, esse monitoramento permite acompanhar de forma simples o funcionamento da pipeline.

Em um ambiente produtivo, eu poderia evoluir essa parte utilizando Azure Monitor, dashboards e alertas automáticos.

---

## FinOps e controle de custos

Durante o desenvolvimento também procurei considerar os custos da arquitetura.

A ideia foi utilizar somente os recursos necessários para demonstrar o funcionamento da solução, evitando criar uma infraestrutura maior do que o projeto precisava.

Algumas decisões que tomei foram:

- utilização de Parquet na Silver e Gold;
- Storage Standard;
- redundância LRS;
- Event Hubs no plano Basic;
- uma unidade de produtividade;
- retenção curta dos eventos;
- processamento local quando possível;
- seleção somente das colunas necessárias no BigQuery;
- filtro dos dados utilizados;
- utilização da amostra de 10.000 alunos durante o desenvolvimento.

Também utilizei o Azure Cost Management para acompanhar os custos.

### Orçamento no Azure

Configurei um orçamento mensal de:

```text
US$ 10
```

Também configurei um alerta para quando o consumo atingir:

```text
80% do orçamento
```

O objetivo é receber um aviso antes que o custo ultrapasse o valor definido.

O Budget serve como mecanismo de monitoramento e alerta. Ele não interrompe automaticamente os recursos quando o limite é atingido.

Além disso, mantive uma documentação específica sobre FinOps em:

```text
docs/finops.md
```

---

## Batch vs Streaming

Durante o desenvolvimento utilizei tanto Batch quanto Streaming porque os dois modelos atendem necessidades diferentes.

Para os dados históricos, o Batch faz mais sentido porque os arquivos podem ser processados em conjunto e não existe necessidade de receber cada registro imediatamente.

Entre as vantagens do Batch estão a menor complexidade e a facilidade de processar grandes volumes históricos.

Por outro lado, existe uma latência maior porque os dados precisam aguardar a próxima execução.

Já o Streaming permite processar eventos conforme eles chegam.

Isso é interessante em um cenário no qual novas informações precisem atualizar rapidamente os indicadores.

Porém, o Streaming também aumenta a complexidade da arquitetura, pois exige serviços de mensageria, Consumers e monitoramento.

Por esse motivo, optei por uma arquitetura híbrida:

```text
Dados históricos -> Batch

Novos eventos -> Streaming
```

---

## Data Lake vs Data Warehouse

Para este projeto optei por uma arquitetura semelhante a um Data Lake.

Com essa abordagem consigo manter os dados em diferentes estágios de processamento.

A organização fica:

```text
Bronze -> Silver -> Gold
```

Na Bronze mantenho os dados mais próximos da origem.

Na Silver mantenho os dados tratados.

Na Gold disponibilizo os dados preparados para análise.

Um Data Warehouse poderia ser utilizado como uma evolução da arquitetura, principalmente se existisse a necessidade de disponibilizar informações estruturadas para muitos usuários de negócio ou ferramentas de BI.

Para o escopo atual, utilizar arquivos Parquet e Azure Blob Storage foi suficiente e apresentou menor complexidade.

---

## Custo vs Performance

Outra decisão importante foi equilibrar custo e desempenho.

Seria possível utilizar serviços e configurações maiores para aumentar a capacidade da arquitetura, mas isso não faria sentido para o volume utilizado neste projeto.

Por isso utilizei:

```text
Event Hubs Basic
1 unidade de produtividade
Storage Standard
LRS
Parquet
```

Essas configurações atendem ao volume atual sem criar recursos acima da necessidade.

Em um cenário produtivo, eu acompanharia o crescimento do volume e as métricas de utilização antes de aumentar a capacidade.

---

## Tecnologias utilizadas

As principais tecnologias que utilizei foram:

- Python para desenvolver a pipeline;
- Pandas para tratamento e transformação;
- PyArrow para trabalhar com Parquet;
- Parquet para armazenamento das camadas tratadas;
- Requests para consumo da API externa;
- Apache Kafka para streaming local;
- Docker para executar o Kafka;
- Azure Event Hubs para streaming na nuvem;
- Azure Blob Storage para armazenamento;
- Azure Cost Management para controle de custos;
- BigQuery para consultar os dados de alunos;
- API do IBGE para enriquecimento territorial;
- Git para versionamento;
- GitHub para armazenar o repositório e trabalhar com branch e Pull Request.

---

## Principais decisões que tomei

Durante o desenvolvimento precisei tomar algumas decisões importantes.

### Não preencher valores nulos automaticamente

Preferi preservar valores ausentes quando não existia informação suficiente para determinar o valor correto.

### Padronizar as chaves

Padronizei o `id_municipio` para facilitar os relacionamentos entre as diferentes fontes.

### Utilizar Parquet

Utilizei Parquet na Silver e Gold por ser um formato mais adequado para armazenamento e leitura analítica.

### Utilizar eventos simulados

Como não utilizei uma fonte real gerando eventos de alfabetização em tempo real, criei eventos simulados para demonstrar o streaming.

A infraestrutura utilizada para transmissão dos eventos, porém, é real.

### Trabalhar com uma amostra de alunos

Utilizei 10.000 registros para conseguir desenvolver e demonstrar a arquitetura sem processar desnecessariamente a base completa durante o desenvolvimento.

---

## Estrutura do projeto

A estrutura principal ficou organizada da seguinte forma:

```text
tech-challenge-fase-2/

├── data/
│   ├── bronze/
│   │   └── streaming/
│   ├── silver/
│   └── gold/
│
├── docs/
│   └── finops.md
│
├── logs/
│   └── pipeline_monitoring.jsonl
│
├── src/
│   ├── ingestion/
│   ├── processing/
│   ├── quality/
│   ├── streaming/
│   └── monitoring/
│
├── notebooks/
├── tests/
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Versionamento

Utilizei Git e GitHub para versionar o projeto.

Durante o desenvolvimento fiz commits das principais etapas e também utilizei uma branch específica para implementar o streaming no Azure:

```text
feature/azure-streaming
```

Depois da implementação, criei um Pull Request e realizei o merge para a branch principal.

Dessa forma consegui manter o histórico das alterações realizadas durante o desenvolvimento.

---

## Como executar o projeto

Primeiro clone o repositório:

```bash
git clone https://github.com/Gbrajao/Fase-2.git
```

Depois entre na pasta:

```bash
cd Fase-2
```

Crie o ambiente virtual:

```bash
python -m venv venv
```

No Windows, ative com:

```powershell
.\venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## Executando a Silver

```bash
python src/processing/process_silver.py
```

---

## Executando a Gold

```bash
python src/processing/create_gold.py
```

---

## Executando a validação de qualidade

```bash
python src/quality/validate_data.py
```

---

## Executando o monitoramento

```bash
python src/monitoring/monitor_pipeline.py
```

---

## Executando o Kafka

Primeiro inicie o container:

```bash
docker compose up -d
```

Em um terminal execute o Consumer:

```bash
python src/streaming/consumer.py
```

Em outro terminal execute o Producer:

```bash
python src/streaming/producer.py
```

Ao finalizar:

```bash
docker compose down
```

---

## Executando o streaming no Azure

Para utilizar o Azure Event Hubs é necessário criar localmente um arquivo:

```text
.env
```

Exemplo:

```text
AZURE_EVENT_HUB_CONNECTION_STRING=SUA_CONNECTION_STRING
AZURE_EVENT_HUB_NAME=alfabetizacao-stream
```

A connection string real não deve ser enviada para o GitHub.

Primeiro execute o Consumer:

```bash
python src/streaming/consumer_azure.py
```

Depois, em outro terminal, execute o Producer:

```bash
python src/streaming/producer_azure.py
```

---

## Possíveis aplicações de Inteligência Artificial

Apesar de não ter desenvolvido um modelo de Machine Learning neste projeto, a camada Gold deixa os dados preparados para futuras aplicações.

Uma possibilidade seria criar um modelo para estimar a probabilidade de um município atingir sua meta de alfabetização.

Também seria possível utilizar os dados territoriais para analisar diferenças entre municípios, estados e regiões.

Com a inclusão de outras informações socioeconômicas, seria possível investigar fatores associados ao desempenho educacional.

Outra possibilidade seria utilizar técnicas de agrupamento para identificar municípios com características semelhantes.

Essas informações poderiam ajudar a identificar regiões que precisam de maior atenção e apoiar decisões relacionadas a políticas públicas.

---

## Limitações do projeto

A principal limitação que encontrei está relacionada à tabela de alunos.

Utilizei uma amostra de 10.000 registros referentes a 2024.

Por esse motivo, resultados calculados diretamente a partir dessa amostra não podem ser generalizados para todos os alunos do Brasil.

Também encontrei diferenças na disponibilidade de algumas informações entre as tabelas e os períodos analisados.

Preferi preservar e documentar essas diferenças em vez de alterar os dados sem uma justificativa.

Outra limitação é que os eventos utilizados no Streaming são simulados.

O Kafka e o Azure Event Hubs são reais, mas os eventos não vêm de um sistema educacional operacional em tempo real.

---

## Possíveis evoluções

Como próximos passos, eu poderia evoluir o projeto utilizando a base completa de alunos e adicionando novos indicadores socioeconômicos.

Também seria possível:

- integrar dados do Censo Escolar;
- criar dashboards;
- automatizar toda a pipeline;
- implementar CI/CD;
- utilizar Azure Monitor;
- criar políticas automáticas de ciclo de vida no Storage;
- utilizar Spark para processamento distribuído;
- desenvolver modelos de Machine Learning utilizando os dados da Gold.

---

## Conclusão

Neste projeto consegui construir uma pipeline de Engenharia de Dados utilizando informações relacionadas à alfabetização no Brasil.

Implementei processamento Batch e Streaming e organizei os dados utilizando a Arquitetura Medalhão, com as camadas Bronze, Silver e Gold.

Também implementei verificações de qualidade e integrei os dados educacionais com uma fonte externa oficial do IBGE.

Para demonstrar Streaming, primeiro utilizei Apache Kafka localmente e depois implementei uma versão utilizando Azure Event Hubs.

No ambiente de nuvem também utilizei Azure Blob Storage para armazenar as diferentes camadas.

Além da pipeline, implementei um monitoramento simples para acompanhar volume, status e possíveis falhas e utilizei Azure Cost Management para trabalhar aspectos de FinOps.

Durante o desenvolvimento procurei não apenas fazer os códigos funcionarem, mas também entender e documentar as decisões tomadas, como a preservação dos valores nulos, a utilização de Parquet, a escolha entre Batch e Streaming e o dimensionamento dos recursos em nuvem.

Com a arquitetura construída, os dados saem das fontes originais, passam pelas etapas de tratamento e validação e chegam à Gold preparados para análises, dashboards e possíveis aplicações futuras de Inteligência Artificial.
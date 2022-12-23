# Portfolio Analista de Dados

Repositório destinado ao portfolio de projetos de Análise de Dados (versão em português)


## [**WebScraping, ETL e BI:** Salários para Analista de Dados nas capitais do *Brasil*](https://github.com/OviedoVR/Portfolio-Analista-de-Dados-pt/tree/main/WebScrapping%2C%20ETL%20e%20BI:%20Sal%C3%A1rios%20para%20Analista%20de%20Dados%20nas%20capitais%20do%20Brasil)

> **Dados:** coletados das páginas do Glassdoor para as 27 capitais brasileiras.

> **Processamento:** [Notebook Python](https://github.com/OviedoVR/Portfolio-Analista-de-Dados-pt/blob/main/WebScrapping%2C%20ETL%20e%20BI:%20Sal%C3%A1rios%20para%20Analista%20de%20Dados%20nas%20capitais%20do%20Brasil/WebScraping_AnalistaDeDados_Glassdoor_Brasil.ipynb) via Google Colab (scraping e data wrangling).

> **Deploy:** Dashboard do [Google Data Studio](https://datastudio.google.com/reporting/87c046b9-b77f-4e62-a137-7e53f835ef17).

> **Ferramentas:** Python (Google Colab) e Google Data Studio.

<img width="500" src="https://github.com/OviedoVR/Portfolio-Analista-de-Dados-pt/blob/main/WebScrapping%2C%20ETL%20e%20BI:%20Sal%C3%A1rios%20para%20Analista%20de%20Dados%20nas%20capitais%20do%20Brasil/Cover-Glassdoor-Analytics.png">



## [Análise Exploratória (EDA) com SQL sobre dados de Crédito](https://github.com/OviedoVR/Portfolio-Analista-de-Dados-pt/tree/main/1.%20An%C3%A1lise%20Explorat%C3%B3ria%20(EDA)%20com%20SQL%20sobre%20dados%20de%20Cr%C3%A9dito)

> **Dados:** base de clientes(10,000+ linhas) - disponível em [Github](https://github.com/OviedoVR/DA_Projects_Portifolio/blob/main/SQL_EDA_Credito/credito.csv).

> **Deploy:** aplicativo web elaborado via Streamlit - [SQL-EDA-Crédito](https://oviedovr-ongoing-sql-eda-credito-lw3vrj.streamlitapp.com/).

> **Ferramentas:** AWS S3, AWS Athena, Python (Google Colab), VS Code (Python scripting) e Streamlit.

<img width="400" src="https://github.com/OviedoVR/Portfolio-Analista-de-Dados-pt/blob/main/figuras/pipeline-sql-credito.png">


## [Análise em SQL com Azure Databricks](https://github.com/OviedoVR/Portfolio-Analista-de-Dados)

> **Dados:** TED Talks (2006-2022) - disponível em [Kaggle](https://www.kaggle.com/datasets/miguelcorraljr/ted-talks-2022?select=20221013_ted_talks.csv).

> **Deploy:**  destinado a responder a algumas perguntas de negócios sobre os eventos do TED Talks que ocorreram de 2006 a 2022. Para responder a essas perguntas, foi usado o *Structured Query Language* (**SQL**) e visualizações *built-in* do Azure Databricks. [Notebook](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/1499004351802398/814331625001671/6746168454129455/latest.html)

 [SQL-EDA-Crédito](https://oviedovr-ongoing-sql-eda-credito-lw3vrj.streamlitapp.com/).

> **Ferramentas:** Azure Databricks, SQL, Vizualizações built-in do Databricks, Storyteling, Estatístca.

<img width="400" src="imagens/sql_databricks.png">



## [**DataFII:** uma solução data-driven para Fundos de Investimento Imobiliário (FIIs)](https://github.com/OviedoVR/Portfolio-Analista-de-Dados-pt/tree/main/2.%20DataFII)

> **Dados:** web scrapping do site https://www.fundsexplorer.com.br/ranking.

> **Deploy**: aplicativo web elaborado via Streamlit, artigo no medium e [vídeo demonstrativo](https://youtu.be/22BFRmBVGeY) no Youtube.

O projeto resultou em uma solução *data-driven* para análise, tomada de decisão e mapeamento de oportunidades acerca de FIIs. O *web-app** apresenta duas funcionalidades principais:

* Ranking interativo de FIIs; 

* Filtro de oportunidades para FIIs, usando uma estratégia baseada em setores. O preço dos ativos e seus indicadores apresentam granularidade diária.

> **Ferramentas:** Python (Google Colab), Estatística, VS Code (Python scripting) e Streamlit.

<img width="450" src="https://github.com/OviedoVR/Portfolio-Analista-de-Dados-pt/blob/main/figuras/dataFII-pipeline.png">


## Freelancing Business Report - POWER BI


> **Dados**: registro de dados acerca projetos, com granularidade semanal (período: agosto de 2020 - novembro 2022). Dados reais e pessoais, tratados para omitir receitas e identidade dos clientes.

> **Processamento** Power Query

> **Deploy:** Dashboard do [Power Bi](https://app.powerbi.com/view?r=eyJrIjoiY2Q0MjY3NjctYWNjOC00Yzc0LThkNjEtYmUwYjczZjFjNTBkIiwidCI6ImU4Y2YyNjM5LTFmOTgtNGJiNC1iZDg5LWFiZDE0OTI4OTM3ZiJ9&embedImagePlaceholder=true&pageName=ReportSection).

O dashboard permite:

* Acessar o cenário macro (KPI's e insights para todo o período);
* Acessar cenários anuais;
* Acessar cenários baseados no tipo de serviço.

<img width="450" src="PowerBI.png">

## [**BI e Visualização de Dados:** Acompanhamento de negócio *freelancer*](https://github.com/OviedoVR/Portfolio-Analista-de-Dados-pt/tree/main/3.%20BI%20e%20Visualiza%C3%A7%C3%A3o:%20Freelancer%20Dashboard)

> **Dados:** registro de dados acerca projetos, com granularidade semanal (período: agosto de 2020 - atual). Dados reais e pessoais, tratados para omitir receitas e identidade dos clientes - disponível em planilha do Google Sheets. O relatório foi configurado para envio automático ao stakeholder a cada 10 dias.

> **Processamento:** Data wrangling elaborado via Notebook Python do Google Colab.

> **Deploy:** Dashboard do [Google Data Studio](https://datastudio.google.com/reporting/08c7487a-a034-41ad-a436-30551e6d8771).

> **Ferramentas:** Python (Google Colab), Google Sheets, Google Data Studio.

<img width="450" src="https://github.com/OviedoVR/Portfolio-Analista-de-Dados-pt/blob/main/figuras/Freelas-dash.png">


## [**TUTORIAL AWS:** acessar externalmente um *bucket *do *AWS S3*](https://github.com/OviedoVR/Portfolio-Analista-de-Dados-pt/tree/main/4.%20Tutorial%20AWS%20-%20Acesso%20a%20Bucket%20do%20S3)

> **Contexto:** tutorial rápido de como configurar a conexão entre um `<bucket do S3>`/`Python` e permitir acesso apenas ao bucket de intresse. Essa é uma prática interessante, já que se deve ter cuidado ao gerenciar permissões na cloud.

> **Deploy:** O tutorial é um Notebook Python.

> **Ferramentas:** Python (Google Colab), boto3, AWS S3, AWS IAM.

<img width="450" src="https://github.com/OviedoVR/DA_Estudo/blob/main/images/S3-to-Python.png">


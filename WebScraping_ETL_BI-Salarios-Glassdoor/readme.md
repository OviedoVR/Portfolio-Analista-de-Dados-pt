## **WebScrapping, ETL e BI: Salários para Analista de Dados nas capitais do Brasil**

* **Problema**: o salário de um Analista de Dados não é normalmente divulgado nas vagas, salvo para níveis superiores, como o sênior. Isso dificulta aos profissionais com o nível menor (e.g., os júniores) a estimar uma pretensão salarial mais realista tanto para o contratante como para o contratado, já que o salário pode mudar depenendo da região, do estado, da empresa, etc. Esse projeto traz uma estimativa com bases nessas informações, extraída do site Glassdoor.
* **Objetivo**: estimar os salários de Analistas de Dados, por região, estado e nível de senioridade.
* **Processamento**: [Notebook Python](https://github.com/OviedoVR/Portfolio-Analista-de-Dados-pt/blob/main/WebScrapping%2C%20ETL%20e%20BI:%20Sal%C3%A1rios%20para%20Analista%20de%20Dados%20nas%20capitais%20do%20Brasil/WebScraping_AnalistaDeDados_Glassdoor_Brasil.ipynb) via Google Colab (scraping e data wrangling).
* **Deploy**: Dashboard do [Google Data Studio](https://datastudio.google.com/reporting/87c046b9-b77f-4e62-a137-7e53f835ef17).

---

* *Ferramentas*: 
    * Requests
    * Beautiful Soup
    * Numpy
    * Pandas (com foco em operações vetorizadas)
    * Estatítstica Descritiva
    * Google Data Studio

* *Limitações*: 
    * Foram utilizadas as primeiras páginas de cada url do site Glassdoor
    * Para campos com a informação de salário do tipo "**cerca de x-y**", foi calculada a média entre estes dois valores.

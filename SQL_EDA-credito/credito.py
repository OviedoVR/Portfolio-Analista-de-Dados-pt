import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from streamlit_option_menu import option_menu


st.set_page_config(page_title='SQL-credito')

# CSS Style:
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown('## Análise Exploratória com SQL: dados de crédito para uma base de clientes')

st.markdown("""**Objetivo:**
                Realizar uma análise exploratória de dados (EDA) em uma base 
                de clientes com informações de crédito bancário.""")

st.markdown('> **Pipeline da solução**')
st.image('pipeline-sql-credito.png', use_column_width=True)              

st.markdown("""> **Base de dados:** [Github](https://github.com/andre-marcos-perez/ebac-course-utils/blob/main/dataset/credito.csv)

> **Processamento** (Notebook do Google Colab): [credito-prep.ipynb](colab.com)
                """)
st.markdown('###')

#st.sidebar.image("Pipeline-descricao.png", use_column_width=True)

menu_escolha = option_menu(
    menu_title=None,#"Escolha uma opção",
    options=['Exploração', 'Análise', 'Conclusões'],
    icons=['search', 'bar-chart-line-fill'],
    menu_icon="cast",
    default_index=0,
    orientation='horizontal',
    styles={
        "icon": {"font-size": "14.5px"}, 
        "nav-link": {"font-size": "14.5px"}
    }
)

dados_credito = pd.read_csv('data\credito.csv',
  names = ['id', 'default', 'idade', 'sexo', 
          'dependentes', 'escolaridade',
          'estado_civil', 'salario_anual', 
          'tipo_cartao', 'qtd_produtos',
          'meses_inativo_12m', 'limite_credito', 
          'valor_transacoes_12m',
          'qtd_transacoes_12m']
)

if menu_escolha == 'Exploração':

    #--------------------------------------------------------
    st.markdown("""##### 1 :mag: **Quantas linhas compõem o dataset?** """)

    st.code("""SELECT COUNT(*) AS linhas
FROM credito;
    """, language='sql')

    q1 = pd.read_csv('queries\q1-linhas.csv')
    st.dataframe(q1)
    st.markdown("""#""")
    #--------------------------------------------------------
    st.markdown("""##### 2 :mag: **Quais são os tipos de dados?**""")

    st.code("""DESCRIBE credito;
    """, language='sql')

    q2 = pd.read_csv('queries\q2-dtypes.csv', delimiter=';',names=['variable','dtype'])
    st.dataframe(q2, height=525)
    st.markdown("""#""")
    #--------------------------------------------------------
    st.markdown("""##### 3 :mag: **Faixa de idade dos clientes**""")
    st.code("""SELECT 
    MIN(idade) as idade_min,
    MAX(idade) as idade_max,
    CAST(AVG(idade) AS int) AS
        media_idade,
    CAST(STDDEV(idade) AS int) AS
        std_idade
FROM credito;
    """, language="sql")

    q3 = pd.read_csv('queries\q3-idades.csv')
    st.dataframe(q3)

    fig_q3, ax = plt.subplots(figsize=(6,1.5))
    sns.boxplot(data=dados_credito, x='idade', width=0.4, palette=['#31c6f7'])
    sns.despine(fig=None, ax=None, top=True, right=True, left=True, bottom=False, offset=None, trim=False)
    plt.ylabel('')
    plt.yticks([],size=8)
    plt.xticks(size=8)
    plt.tight_layout();
    st.pyplot(fig_q3, use_column_width=True)
    ### Comentário:
    st.markdown("""- A idade dos clientes se encontra bem distribuída entre 26-73, com a média de 46 anos sendo bem representativa
    """)
    st.markdown("""#""")
    #--------------------------------------------------------
    st.markdown("""##### 4 :mag: **Distribuição do sexo dos clientes**""")
    st.code("""SELECT 
    sexo,
    COUNT(sexo) AS 
        clientes,
    ROUND(COUNT(sexo)/10127.00, 2) AS
        porcentagem
FROM credito
GROUP BY sexo;
    """, language="sql")

    q4 = pd.read_csv('queries\q4-sexo.csv')

    fig_q4, ax = plt.subplots(figsize=(6,1.2))
    sns.barplot(data=q4, x='porcentagem', y='sexo', palette='cool_r')
    sns.despine(fig=None, ax=None, top=True, right=True, left=True, bottom=False, offset=None, trim=False)
    plt.ylabel('')
    plt.yticks(size=8)
    plt.xticks(size=8)
    plt.tight_layout();

    st.dataframe(q4)
    st.pyplot(fig_q4, use_column_width=True) #use_column_width=True
    ### Comentário:
    st.markdown("""- A proporção de clientes do sexos feminino e masculino é aproximadamente igual""")
    st.markdown("""#""")
    #--------------------------------------------------------
    st.markdown("""##### 5 :mag: **Dependentes**""")
    st.code("""SELECT 
    dependentes AS 
        numero_dependentes,
    ROUND(COUNT(dependentes)/10127.00, 2) AS
        porcentagem
FROM credito
GROUP BY dependentes
ORDER BY 2 DESC;
    """, language="sql")

    q5 = pd.read_csv('queries\q5-dependentes.csv')
    st.dataframe(q5)

    q5['numero_dependentes'] = q5['numero_dependentes'].astype('string')
    q5['numero_dependentes'] = q5['numero_dependentes'].replace({
        '0':'Nenhum', 
        '1': '1 Dependente',
        '2': '2 Dependentes',
        '3': '3 Dependentes',
        '4': '4 Dependentes',
        '5': '5 Dependentes'      
    })

    fig_q5, ax = plt.subplots(figsize=(6,2))
    sns.set_style('ticks')
    sns.barplot(data=q5, x='porcentagem', y='numero_dependentes', lw=0, palette='cool_r')
    sns.despine(fig=None, ax=None, top=True, right=True, left=True, bottom=False, offset=None, trim=False)
    plt.ylabel('')
    plt.yticks(size=8)
    plt.xticks(size=8)
    plt.tight_layout();

    st.pyplot(fig_q5, use_column_width=True) #use_column_width=True
    ### Comentário:
    st.markdown("""- Cerca de 91% dos clientes possuem ao menos 1 dependente""")
    st.markdown("""- A cada 100 clientes aleatórios: 18 possuem 1 depentente, enquanto 73 têm 2 dependentes ou mais
    """, unsafe_allow_html=True)
    st.markdown("""#""")
    #--------------------------------------------------------
    st.markdown("""##### 6 :mag: **Escolaridade dos clientes**""")

    st.code("""
    SELECT 
    escolaridade,
    COUNT(escolaridade) AS 
        nivel_escolaridade,
    ROUND(COUNT(escolaridade)/8608.00, 2) AS
        porcentagem
FROM credito
GROUP BY escolaridade
ORDER BY 3 DESC;
    """, language="sql")

    q6 = pd.read_csv('queries\q6-escolaridade.csv')
    st.dataframe(q6)
    #
    q6['escolaridade'] = q6['escolaridade'].replace('na','não informado')
    #
    figq6, ax = plt.subplots(figsize=(6,2))
    sns.barplot(data=q6, x='porcentagem', y='escolaridade', palette='cool_r')
    sns.despine(fig=None, ax=None, top=True, right=True, left=True, bottom=False, offset=None, trim=False)
    plt.ylabel('')
    plt.yticks(size=8)
    plt.xticks(size=8)
    plt.tight_layout();

    st.pyplot(figq6, use_column_width=True) #use_column_width=True
    ### Comentário:
    st.markdown("""- A cada 100 clientes, 15 não têm educação formal""")
    st.markdown("""- Cerca de 51% possui algum tipo de ensino superior""")
    st.markdown(""" - Não costam informações acerca da escolaridade para 1519 clientes (~15%)""")
    st.markdown("""#""")
    #--------------------------------------------------------
    st.markdown("""##### 7 :mag: **Estado civil dos clientes**""")
    st.code("""SELECT 
    estado_civil,
    COUNT(estado_civil) AS 
        clientes,
    ROUND(COUNT(estado_civil)/10127.00, 2) AS
        porcentagem
FROM credito
GROUP BY estado_civil
ORDER BY 3 DESC;
    """, language="sql")

    q7 = pd.read_csv('queries\q7-estado_civil.csv')
    q7['estado_civil'] = q7['estado_civil'].replace('na','não informado')

    fig_q7, ax = plt.subplots(figsize=(6,1.7))
    sns.barplot(data=q7, x='porcentagem', y='estado_civil', palette='cool_r')
    sns.despine(fig=None, ax=None, top=True, right=True, left=True, bottom=False, offset=None, trim=False)
    plt.ylabel('')
    plt.yticks(size=8)
    plt.xticks(size=8)
    plt.tight_layout();

    st.dataframe(q7)
    st.pyplot(fig_q7, use_column_width=True) #use_column_width=True
    ### Comentário:
    st.markdown("""- Casados e solteiros compreendem 85% da base de clientes""")
    st.markdown("""#""")
    #--------------------------------------------------------
    st.markdown("""##### 8 :mag: **Salário anual dos clientes**""")
    st.code("""SELECT 
        salario_anual,
        COUNT(salario_anual) AS 
        clientes,
        ROUND(SUM(salario_anual)/10127, 2) AS
        porcentagem
FROM credito
GROUP BY salario_anual;
    """, language="sql")

    q8 = pd.read_csv('queries\q8-salario_anual.csv')
    q8['salario_anual'] = q8['salario_anual'].replace('na','não informado')
    
    fig_q8, ax = plt.subplots(figsize=(6,2))
    sns.barplot(data=q8, x='porcentagem', y='salario_anual', palette='cool_r')
    sns.despine(fig=None, ax=None, top=True, right=True, left=True, bottom=False, offset=None, trim=False)
    plt.ylabel('')
    plt.yticks(size=8)
    plt.xticks(size=8)
    plt.tight_layout();

    st.dataframe(q8)
    st.pyplot(fig_q8, use_column_width=True) #use_column_width=True
    ####Comentário:
    st.markdown("""- A maior parte dos clientes ganha menos que R$ 40.000,00 por ano""")
    st.markdown("""- Aproximadamente 11\% dos clientes não informaram o salário anual""")
    st.markdown("""- A cada 100 clientes aleatórios, 36 ganham altos salários (certamente não são profissionais júnior)""")
    #--------------------------------------------------------
    st.markdown("""#""")
    st.markdown("""##### 9 :mag: **Distribuição de clientes quanto ao tipo de cartão**""")
    st.code("""SELECT 
    tipo_cartao,
    COUNT(tipo_cartao) AS 
        clientes,
    ROUND(COUNT(tipo_cartao)/10127.00*100, 3) AS
        porcentagem
FROM credito
GROUP BY tipo_cartao
ORDER BY 3 DESC;
    """, language="sql")

    q9 = pd.read_csv('queries\q9-cartao.csv')

    fig_q9, ax = plt.subplots(figsize=(6,2))
    sns.barplot(data=q9, x='porcentagem', y='tipo_cartao', palette='cool')
    sns.despine(fig=None, ax=None, top=True, right=True, left=True, bottom=False, offset=None, trim=False)
    plt.ylabel('')
    plt.yticks(size=8)
    plt.xticks(size=8)
    plt.tight_layout();

    st.dataframe(q9)
    st.pyplot(fig_q9, use_column_width=True) #use_column_width=True
    ####Comentário:
    st.markdown("""- Cerca de 93% clientes possui o cartão **Blue**""")
    st.markdown("""- Da mesma maneira, muito poucos clientes possuem o cratao **Platinum**, talvez seja interessante repensar essa modalidade """)
    st.markdown("""#""")
    #--------------------------------------------------------
    st.markdown("""##### 10 :mag: **Distribuição do limite de crédito dos clientes**""")
    st.code("""SELECT
        ROUND(MIN(limite_credito), 2) AS
        limite_minimo,
        ROUND(MAX(limite_credito), 2) AS
        limite_maximo,
        ROUND(AVG(limite_credito), 2) AS
        limite_medio,
        ROUND(STDDEV(limite_credito), 2) AS
        std_limite
    FROM credito;
    """, language="sql")

    q10 = pd.read_csv('queries\q10-limite.csv')
    fig_q10, ax = plt.subplots(figsize=(6,1.5))
    sns.boxplot(data=dados_credito, x='limite_credito', width=0.4, palette=['#31c6f7'])
    sns.despine(fig=None, ax=None, top=True, right=True, left=True, bottom=False, offset=None, trim=False)
    plt.ylabel('')
    plt.yticks([])
    plt.xticks(size=8)
    plt.tight_layout();

    st.dataframe(q10)
    st.pyplot(fig_q10, use_column_width=True) #use_column_width=True

    #st.dataframe(dados_credito['limite_credito'].describe())

    ####Comentário:
    st.markdown("""- A diferença entre o limite mínimo e o limite máximo é bem grande (R\$ 33.078,99)""")
    st.markdown("""- Como o **desvio padrão** para o limite médio entre os clientes é **alto** (R\$ 9.088,70), o limite de R\$ 8.632,44 não representa a média para a base de clientes)""")
    st.markdown("""- O **valor central** para o limite é de **R$ 4.549,42** (mediana)""")
    st.markdown("""- Existem muitos ***outliers***, isto é, clientes com limites discrepantes dos demais""")
#--------------------------------------------------------
if menu_escolha == 'Análise':
  
  st.markdown("""Como temos dados ausentes nas colunas **escolaridade**, **estado civil** e **salário anual**,
  vamos trabalhar em cima de uma ***view***:""")
  #--------------------------------------------------------
  st.markdown("""##### 11 :mag: **Criação de uma *view***""")
  st.code("""--Criando a view sem dados ausentes:
CREATE VIEW credito_eda AS
SELECT *
FROM credito
WHERE 
  (escolaridade != 'na') AND
  (estado_civil != 'na') AND
  (salario_anual != 'na'); 
    """, language="sql")
  
  q11 = pd.read_csv('queries/q11-view-check.csv')
  st.dataframe(q11) 
  st.markdown("""#""")
  #--------------------------------------------------------
  st.markdown("""##### 12 :mag: **Quais as características dos clientes com maior limite?** """)
  st.code("""SELECT 
  limite_credito, idade, sexo, 
  dependentes, escolaridade, 
  estado_civil, salario_anual, 
  tipo_cartao, qtd_produtos, 
  valor_transacoes_12m, 
  qtd_transacoes_12m
FROM credito_eda
ORDER BY 1 DESC
LIMIT 10; 
    """, language="sql")
  
  q12 = pd.read_csv('queries/q12-caract.csv')
  st.dataframe(q12)
  ### Comentário:
  st.markdown("""- O sexo predominante para os clientes de maior limite é o **masculino** (de uma amostra de 10 clientes, 100% são homens.""")
  st.markdown("""- O número de dependentes se situa entre 2 e 4. Na amostra acima, a moda é **4 dependentes**.""")
  st.markdown("""- Embora possa contribuir, a educação **não** parece ser um empecilho para adquirir maiores limites de crédito.""")
  st.markdown("""- O estado civil é indiferente quanto ao limite de crédito.""")
  st.markdown("""- Clientes com maiores limites normalemente possuem os cartões **Silver** and **Gold**. Intrigantemente, o cartão **Platinum** não aparece nos maiores limites.""")
  st.markdown("#")
  #--------------------------------------------------------
  st.markdown("""##### 13 :mag: **Quais as características dos clientes com menor limite?** """)
  st.code("""SELECT 
  limite_credito, idade, sexo, 
  dependentes, escolaridade, 
  estado_civil, salario_anual, 
  tipo_cartao, qtd_produtos, 
  valor_transacoes_12m, 
  qtd_transacoes_12m
FROM credito_eda
ORDER BY 1 ASC
LIMIT 10; 
    """, language="sql")
  
  q13 = pd.read_csv('queries/q13-caract.csv')
  st.dataframe(q13)
  ### Comentário:
  st.markdown("""- Os clientes com menores limites são do sexo **feminino**. De uma amostra de 10 clientes, 90\% são do sexo feminino.""")
  st.markdown("""- Dos clientes com os 10 menores limites, todos são do tipo de cartão **blue**.""")
  st.markdown("""- Dentre os clientes com menores limites, o estado civil majoritário é o **casado**.""")
  st.markdown("#")
  #--------------------------------------------------------
  st.markdown("""##### 14 :mag: **Os homens possuem mais limite que as mulheres?** """)
  st.code("""SELECT
  sexo,
  COUNT(limite_credito)/7081.00 AS porcentagem
FROM credito_eda
WHERE limite_credito > 11000
GROUP BY sexo
ORDER BY 2 DESC;
    """, language="sql")
  
  q14 = pd.read_csv('queries/q14-limite_hm.csv')
  
  fig_q14, ax = plt.subplots(figsize=(6,1.25))
  sns.barplot(data=q14, y='sexo', x='porcentagem', palette='cool_r')
  sns.despine(fig=None, ax=None, top=True, right=True, left=True, bottom=False, offset=None, trim=False)
  plt.ylabel('')
  plt.yticks(size=8)
  plt.xticks(size=8)
  plt.tight_layout();

  st.dataframe(q14)
  st.pyplot(fig_q14, use_column_width=True) #use_column_width=True
  ### Comentário:
  st.markdown("""- Para limites maiores que R\$ 11.000,00 (3° quartil), apenas 2% dos clientes são mulheres versus 22% dos homens. Ou seja, homens possuem mais limites que as mulheres.""")
  st.markdown("""#""")
  #--------------------------------------------------------
  st.markdown("""##### 15 :mag: **Isso é reflexo do salário?** """)
  st.code("""SELECT 
  sexo, 
  salario_anual, 
  COUNT(salario_anual) as total_clientes
FROM credito_eda
GROUP BY 
  sexo, 
  salario_anual
ORDER BY 2, 1;
    """, language="sql")
  
  q15 = pd.read_csv('queries/q15-salarios-FM.csv')

  
  fig_q15, ax = plt.subplots(figsize=(6,2.45))
  sns.barplot(data=q15, y='salario_anual', x='total_clientes', hue='sexo', palette='cool')
  sns.despine(fig=None, ax=None, top=True, right=True, left=True, bottom=False, offset=None, trim=False)
  plt.ylabel('')
  plt.yticks(size=8)
  plt.xticks(size=8)
  plt.tight_layout();

  #st.dataframe(q15)
  st.pyplot(fig_q15, use_column_width=True) #use_column_width=True
  ### Comentário:
  st.markdown("""- De fato, os maiores limites dos clientes do sexo **masculino** se devem aos **maiores salários** dos homens frente as mulheres.""")
  st.markdown("""- Para salários anuais maiores que R\$ 80.000,00 **não costam** clientes do sexo feminino.""")
  st.markdown("""#""")
  #--------------------------------------------------------
  st.markdown("""##### 16 :mag: **Quantos dependentes os clientes com maiores limites possuem?** """)
  st.code("""SELECT 
  dependentes,
  COUNT(dependentes) AS num_dependentes
FROM credito_eda
WHERE limite_credito >= 34500
GROUP BY dependentes
ORDER BY 1 DESC;
    """, language="sql")
  
  q16 = pd.read_csv('queries/q16-dependentes_3quartil.csv')

  q16['dependentes'] = q16['dependentes'].replace({
        0:'Nenhum', 
        1: '1 Dependente',
        2: '2 Dependentes',
        3: '3 Dependentes',
        4: '4 Dependentes',
        5: '5 Dependentes'      
  })

  fig_q16, ax = plt.subplots(figsize=(6,2))
  sns.barplot(data=q16, y='dependentes', x='num_dependentes', palette='cool')
  sns.despine(fig=None, ax=None, top=True, right=True, left=True, bottom=False, offset=None, trim=False)
  plt.ylabel('')
  plt.yticks(size=8)
  plt.xticks(size=8)
  plt.tight_layout();

  st.dataframe(q16)
  st.pyplot(fig_q16, use_column_width=True) #use_column_width=True
  ### Comentário:
  st.markdown("""- Dos clientes com limites maiores que R\$ 11.000,00 (3° quartil), grande possui entre 1-4 dependentes.""")
  st.markdown("""- Pela distribuição dos dados, você ter nenhum ou 5 dependentes, parece não influenciar no limite de crédito.""")
  st.markdown("""#""")
  #--------------------------------------------------------
  st.markdown("""##### 17 :mag: **Quanto % do limite, os 5 maiores limites transacionaram (12 m)?**""")
  st.code("""SELECT 
  dependentes,
  COUNT(dependentes) AS num_dependentes
FROM credito_eda
WHERE limite_credito >= 34500
GROUP BY dependentes
ORDER BY 1 DESC;
    """, language="sql")
  
  q17 = pd.read_csv('queries/q17-perc-trans12-maior.csv')
  categories_q17 = {'categoria': [
    'Maior limite 1', 'Maior limite 2',
    'Maior limite 2', 'Maior limite 4',
    'Maior limite 5'
  ]}

  categories_q17 = pd.DataFrame(categories_q17)
  q17 = pd.concat([q17, categories_q17], axis=1)
  
  fig_q17, ax = plt.subplots(figsize=(6,2))
  sns.barplot(data=q17, y='categoria', x='perc_valor_transacionado_12m', ci=None, estimator=np.mean, palette='cool')
  sns.despine(fig=None, ax=None, top=True, right=True, left=True, bottom=False, offset=None, trim=False)
  plt.ylabel('')
  plt.yticks(size=8)
  plt.xticks(size=8)
  plt.tight_layout();

  st.dataframe(q17)
  st.pyplot(fig_q17, use_column_width=True) #use_column_width=True
  ### Comentário:
  st.markdown("""- Os 5 clientes com maiores limites **transacionam menos de 50\%** do limite ao longo de 12 meses.""")
  st.markdown("""- Isso pode evidenciar o uso consciente do limite de crédito.""")
  st.markdown("""#""")
#--------------------------------------------------------
  st.markdown("""##### 18 :mag: **Quanto % do limite, os 5 menores limites transacionaram (12 m)?**""")
  st.code("""SELECT 
  dependentes,
  COUNT(dependentes) AS num_dependentes
FROM credito_eda
WHERE limite_credito <= 2555
GROUP BY dependentes
ORDER BY 1 DESC;
    """, language="sql")
  
  q18 = pd.read_csv('queries/q18-perc-trans12-menor.csv')
  categories_q18 = {'categoria': [
    'Menor limite 1', 'Menor limite 2',
    'Menor limite 2', 'Menor limite 4',
    'Menor limite 5'
  ]}

  categories_q18 = pd.DataFrame(categories_q18)
  q18 = pd.concat([q18, categories_q18], axis=1)
  
  fig_q18, ax = plt.subplots(figsize=(6,2))
  sns.barplot(data=q18, y='categoria', x='perc_valor_transacionado_12m', ci=None, estimator=np.mean, palette='cool')
  sns.despine(fig=None, ax=None, top=True, right=True, left=True, bottom=False, offset=None, trim=False)
  plt.ylabel('')
  plt.yticks(size=8)
  plt.xticks(size=8)
  plt.tight_layout();

  st.dataframe(q18)
  st.pyplot(fig_q18, use_column_width=True) #use_column_width=True
  ### Comentário:
  st.markdown("""- Os 5 clientes com menores limites transacionam mais do que a capacidade máxima do limite ao longo de 12 meses.""")
  st.markdown("""- Alguns clientes chegaram a transacionar **3x mais** que o limite de crédito disponível.""")
  st.markdown("""- Isso pode indicar dois cenários: **(i)** o limite pode ser aumentado ou **(ii)** o cliente não faz uso consciente do limite de crédito, podendo se endividar com maiores limites.""")
  st.markdown("""#""")
  #--------------------------------------------------------
  st.markdown("""##### 19 :mag: **Qual a porcentagem de clientes com altos limites, mas cartão blue?**""")
  st.code("""--Total de clientes do cartão blue:
SELECT COUNT(*) AS clientes
FROM credito_eda
WHERE tipo_cartao = 'blue';
    """, language="sql")

  st.markdown("""<span style="color:dimgrey"> <b> Resultado: </b> </span> 6598""",
              unsafe_allow_html=True)

  st.code("""--Aqui podemos usar uma sub-query:
SELECT 
  SUM(clientes)/6598.00*100 AS porcentagem
FROM(
     SELECT 
       COUNT(tipo_cartao) AS clientes
     FROM credito_eda
     WHERE 
       tipo_cartao = 'blue' 
     AND
       limite_credito >= 34500
     GROUP BY limite_credito
     ORDER BY limite_credito DESC
);
    """, language="sql")
   
  q19 = pd.read_csv('queries/q19-maiores-blue.csv')

  st.dataframe(q19)
  ### Comentário:
  st.markdown("""- Apenas 2\% dos clientes com maiores limites (acima do R$ 34500) são do cartão **blue**.""")
  st.markdown("""- Isso indica que o cartão **blue** são destinados ao clientes com limites na média da base de dados.""")
  st.markdown("""#""")
#--------------------------------------------------------
  st.markdown("""##### 20 :mag: **Qual é o contexto dos clientes que se mostram *outliers* (quanto ao limite) para a empresa?**""")
  st.code("""/*Vamos supor que uma inatividade maior que 30% ao longo de 12 meses, 
represente um cliente cuja inativatividade é tida como considerável.
Portanto, essa inatividade não é ideal para o contexto da empresa*/

SELECT 
  classe_cliente, 
  percentual_inatividade,
  COUNT(percentual_inatividade) AS total_inatividade_12m
FROM(
    SELECT
    CASE 
        WHEN limite_credito >= 25000 THEN 'Outlier'
        ELSE 'Comumn'
     END AS classe_cliente,
     CASE 
        WHEN (meses_inativo_12m/12.00 >= 0.3) THEN 'Considerável' 
        ELSE 'Ideal'
     END AS percentual_inatividade
     FROM credito_eda
     ORDER BY 1 DESC)
GROUP BY classe_cliente, percentual_inatividade
ORDER BY 1 DESC;
    """, language="sql")
   
  q20 = pd.read_csv('queries/q20-outliers.csv')
  
  fig_q20, ax = plt.subplots(figsize=(6,1.75))
  sns.barplot(data=q20, x='total_inatividade_12m', y='percentual_inatividade', hue='classe_cliente', ci=None, palette='cool')
  sns.despine(fig=None, ax=None, top=True, right=True, left=True, bottom=False, offset=None, trim=False)
  plt.ylabel('')
  plt.yticks(size=8)
  plt.xticks(size=8)
  plt.legend(loc='best')
  plt.tight_layout();

  st.dataframe(q20)
  st.pyplot(fig_q20, use_column_width=True)

  ### Comentário:
  st.markdown("""- Como a proporção de clientes com inatividade ideal ao longo de 12 meses frente àqueles com inatividade considerável é muito maior, tanto para os clientes comuns quanto para os ***outliers***, então podemos afirmar que os ***outliers*** são **positivos** para o cenário da empresa.""")
#--------------------------------------------------------
if menu_escolha == 'Conclusões':

  st.markdown("""#""")
  st.markdown(""" **COM BASE NAS QUERIES EXECUTADAS:**
 
  - A idade média dos clientes é de 46 anos, com a idade mínima de 26 anos. Isso é pertinente para **campanhas de marketing** da empresa;
  - A distribuição de clientes dos sexos feminino e masculino é praticamente **igual**;
  - Aproximadamente 91\% dos clientes possuem ao menos 1 dependente;
  - Apenas 0,2\% dos clientes possuem o cartão **Platinum**, logo esse cartão poderia ser repensado por parte da empresa;
  - Constatou-se que os **homens** possuem **maiores limites** que as mulheres, onde os **maiores salários** para o clientes do sexo masculino são determinantes para os maiores limites de crédito;
  - A **diferença** de limite de crédito quanto ao **sexo do cliente** é inerente à empresa;
  - Ter nenhum ou 5 dependentes parece não influenciar no limite de crédito;
  - Clientes com maiores limites transacionaram menos de 50\% do valor do limite nos últimos 12 meses, enquanto aqueles com menores limites extrapolaram em relação ao valor do limite (alguns chegaram a movimentar **3 vezes mais** do que o valor de seu limite de crédito);
  - Os ***outliers*** são positivos para o contexto da empresa. 
  """, unsafe_allow_html=True)
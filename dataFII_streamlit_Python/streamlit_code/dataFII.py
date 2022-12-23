# IMPORTS
import requests
import numpy as np
import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import xlsxwriter
from io import BytesIO
#--------------------------------------------------------------

# COLETA DOS DADOS
URL = 'https://www.fundsexplorer.com.br/ranking'
resposta = requests.get(URL)

if resposta.status_code == 200:
  dados = pd.read_html(resposta.content, encoding = 'utf-8')[0]

dados.sort_values('Códigodo fundo', inplace = True)
#--------------------------------------------------------------
dados.columns = [
       'FII', 'Setor', 'Preco_atual', 'Liquidez_diaria',
       'Dividendo', 'Dividend_yield', 'DY_3m_acumulado', 'DY_6m_acumulado',
       'DY_12m_acumulado', 'DY_3m', 'DY_6m', 'DY_12m',
       'DY_ano', 'Variacao_preco', 'Rentab_periodo', 'Rentab_acumulada',
       'Patrimonio_liquido', 'VPA', 'P_VPA', 'DY_patrimonial',
       'Variacao_patrimonial', 'Rentab_patr_no_periodo',
       'Rentab_patr_acumulada', 'Vacancia_fisica', 'Vacancia_financeira',
       'Qtd_ativos'
]

colunas_interesse = [
  'FII',
  'Setor',
  'Preco_atual',
  'Liquidez_diaria',
  'DY_12m',
  'P_VPA',
  'Vacancia_financeira',
  'Qtd_ativos'
]                    

dados = dados[colunas_interesse]
#--------------------------------------------------------------

# LIMPEZA DOS DADOS

# valores nulos:
indices_setor_nulo = dados[dados['Setor'].isna()].index
dados.drop(indices_setor_nulo, inplace=True)

# dados faltantes:
colunas_floats = list(dados.iloc[:,2:-1])
dados[colunas_floats] = dados[colunas_floats].fillna(value = 0)

#transformações:
dados[colunas_floats] = dados[colunas_floats].applymap(lambda x: str(x).replace('R$ ', '').replace('.0','').replace('%','').replace('.','').replace(',','.'))
dados[colunas_floats] = dados[colunas_floats].astype('float')
dados['Setor'] = dados['Setor'].replace({'Títulos e Val. Mob.': 'Títulos e Valores Mobiliários'})
dados['P_VPA'] = dados['P_VPA']/100
#--------------------------------------------------------------

# MÉTRICAS POR SETOR

metricas_setor = dados.groupby('Setor').agg(['mean', 'std'])
#--------------------------------------------------------------

# FUNÇÃO-BASE
def filtrar_FII(base_dados, setor, label_setor='Setor'):

  metricas_setor = dados.groupby('Setor').agg(['mean', 'std'])

  df_setor = base_dados[base_dados[label_setor].isin([setor])]
  
  if setor == 'Títulos e Val. Mob.':
    filtro_ = \
            (df_setor['P_VPA'] < 1.10) &\
            (df_setor['P_VPA'] > .80) &\
            (df_setor['DY_12m'] > metricas_setor.loc[setor, ('DY_12m','mean')]) &\
            (df_setor['Vacancia_financeira'] <= metricas_setor.loc[setor, ('Vacancia_financeira','mean')]) &\
            (df_setor['Liquidez_diaria'] >= metricas_setor.loc[setor, ('Liquidez_diaria','mean')])       
 
  else:
    filtro_ = \
            (df_setor['Qtd_ativos'] > 10) &\
            (df_setor['P_VPA'] < 1.10) &\
            (df_setor['P_VPA'] > .80) &\
            (df_setor['DY_12m'] > metricas_setor.loc[setor, ('DY_12m','mean')]) &\
            (df_setor['Vacancia_financeira'] <= metricas_setor.loc[setor, ('Vacancia_financeira','mean')]) &\
            (df_setor['Liquidez_diaria'] >= metricas_setor.loc[setor, ('Liquidez_diaria','mean')])       

  return df_setor[filtro_]
  #--------------------------------------------------------------
#
#-----------------------------------------------------------------------------
# STREAMLIT------------------------------------------------------------------:

with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
# Página 1:
def main_page():
    data_in = dados.copy()

    data_in['Preco_atual'] = data_in['Preco_atual'].apply(lambda x: round(x, 2))

    st.markdown("<h1 style='text-align:center'> &#128187; Filtro Simples",
             unsafe_allow_html=True)
  
    st.image('dataFII.png', use_column_width=True)
   
    st.markdown("""<hr style="height:3px;width:100%;border:none;
                color:black;background-color:black" /> """, 
                unsafe_allow_html=True)

    st.markdown("""
            ### **Filtro de FIIs**
            <p style="color:#300C62;text-align:justify"> <b> Filtrar os 
            fundos de investimento imobiliário (FIIs) de acordo com os parâmetros escolhidos, assim,
            Os Fundos de Investimento Imobiliário (FIIs) são filtrados de acordo e armazenados em uma tabela interativa
            que pode ser baixada em uma planilha do MS Excel. </b> </p>

            <hr style="height:3px;width:100%;border:none;
                color:black;background-color:black" /> 
            """, unsafe_allow_html=True)
    #st.markdown("# ")

    filtro_sim_nao = st.checkbox('Ativar Filtros')

    st.markdown("# ")

    col1, col2 = st.columns(2)
    
    with col1:
      st.markdown(':wrench: **Preço Máximo (R$)**',
                unsafe_allow_html=True)
      preco_atual_range = float(st.slider(
      '',
      0, 250, value=100, key="1"))
    
      st.markdown(':wrench: **P/VPA mínimo**',
                unsafe_allow_html=True)
      P_VPA_range_min = float(st.slider(
     '',
      0.5, 1.20, value=0.8, key="2"))

      st.markdown(':wrench: **P/VPA máximo**',
                unsafe_allow_html=True)
      P_VPA_range_max = float(st.slider(
      '',
      0.5, 1.20, value=1.1, key="3"))

    with col2:
      st.markdown(':wrench: **Dividend Yield (%)**',
                unsafe_allow_html=True)
      DY = float(st.slider(
        '',
        0.10, 1.10, value=0.5, key="4"))

      st.markdown(':wrench: **Liquidez Diária**',
                unsafe_allow_html=True)
      liqudez_diaria_range = float(st.slider(
        '',
        0, 12000, value=3000, key="5"))

      st.markdown(':wrench: **Quantidade de Ativos**',
                unsafe_allow_html=True)
      qtd_ativos = float(st.slider(
        '',
        0, 75, value=5, key="6"))

    st.markdown("""# <h1 style="color:black;text-align:center;font-size:100px"> &#9001; &#9002;</h1>""", 
                unsafe_allow_html=True)    
             

    st.markdown("""## """, 
            unsafe_allow_html=True)

    if filtro_sim_nao:
      filtro_simples = \
              (data_in['Preco_atual'] <= preco_atual_range) &\
              (data_in['P_VPA'] >= P_VPA_range_min) &\
              (data_in['P_VPA'] <= P_VPA_range_max) &\
              (data_in['DY_12m'] >= DY) &\
              (data_in['Liquidez_diaria'] >= liqudez_diaria_range) &\
              (data_in['Qtd_ativos'] >= qtd_ativos)  

      data_in = data_in[filtro_simples]

      st.markdown(f'<h3 style="color:#300c62"> {len(data_in)} FIIs listados</h3>',
                    unsafe_allow_html=True)
      AgGrid(data_in.sort_values('FII'))
      
    else:
        st.markdown(f'<h3 style="color:#300c62"> {len(data_in)} FIIs listados</h3>',
                    unsafe_allow_html=True)
        AgGrid(data_in.sort_values('FII'))

    def to_excel(df):
      output = BytesIO()
      writer = pd.ExcelWriter(output, engine='xlsxwriter')
      df.to_excel(writer, index=False, sheet_name='Sheet1')
      workbook = writer.book
      worksheet = writer.sheets['Sheet1']
      format1 = workbook.add_format({'num_format': '0.00'}) 
      worksheet.set_column('A:A', None, format1)  
      writer.save()
      processed_data = output.getvalue()
      
      return processed_data
    
    df_xlsx = to_excel(data_in)
    
    st.download_button(label='Fazer download',
                                data=df_xlsx ,
                                file_name= 'Resultados_filto_simples.xlsx')

# Página 2:
def page2():
    st.markdown("<h1 style='text-align:center'> &#127922; Filtro de Oportunidades </h1>",
                unsafe_allow_html=True)
    st.image('dataFII.png', use_column_width=True)

    st.markdown("""<hr style="height:3px;width:100%;border:none;
                color:black;background-color:black" /> """, 
                unsafe_allow_html=True)
            
    st.markdown("""
        ### **Estratégia** (com base em um setor escolhido)
        <p style="color:#300C62;text-align:justify"> <b> Filtrar os fundos de investimento imobiliário 
        (FIIs) de acordo com um setor escolhido, assim,
        onde os FIIs devem apresentar uma performance com base nas métricas
        do setor. O objetivo é auxiliar na tomada de decisão e não servir como
        uma recomendação de compra. Sugere-se que se faça uma análise qualitativa
        dos ativos filtrados antes de qualquer compra e venda. </b> </p>
        <hr style="height:3px;width:100%;border:none;
        color:black;background-color:black" /> 
        """, unsafe_allow_html=True)

    st.markdown("""
    ### :office: Fundos de tijolo/híbridos:

    *   **Quantidade de ativos** > 10

    *   **P/VPA** entre 0.8 e 1.1

    *   **Dividend Yield (DY)** > DY do **Setor**

    *   **Vacância financeira** $\leq$ Vacância financeira do **Setor**

    *   **Liquidez diária** $\geq$ Liquidez diária do **Setor**
    
    <hr style="height:1px;width:100%;border:none;
    color:#333;background-color:#333" /> 
    
    
    ###    :memo: Fundos de papel:

    *   **P/VPA** entre 0.8 e 1.1

    *   **Dividend Yield (DY)** > DY do **Setor**

    *   **Vacância financeira** $\leq$ Vacância financeira **Setor**

    *   **Liquidez diária** $\geq$ Liquidez diária do **Setor**
                """,unsafe_allow_html=True)

    st.markdown("""<hr style="height:3px;width:100%;border:none;
                color:#333;background-color:#333" /> """, 
            unsafe_allow_html=True)

    st.markdown('### :mag: Escolha um setor',
                unsafe_allow_html=True)

    escolha_setor = st.selectbox(
        """Shoppings | Títulos e Valores Mobiliários | Lajes Corporativas |
        Logística | Híbrido | Outros | Hospital | Residencial | Hotel""",
        ('Shoppings', 'Títulos e Valores Mobiliários', 'Lajes Corporativas',
        'Logística', 'Híbrido', 'Outros', 'Hospital', 'Residencial',
        'Hotel'))
    FIIs_filtrados = filtrar_FII(dados, setor=escolha_setor)

    if FIIs_filtrados.empty:
        st.markdown('##### :x: Sem oportunidades', unsafe_allow_html=True)

        st.markdown('##### :bar_chart: Métricas por setor',
                    unsafe_allow_html=True)
        st.markdown("""**DY_12m:** dividend yield (média 12 meses) | **VF:** vacância financeira | **LD:** liquidez diária
                    """, unsafe_allow_html=True)

        metricas_setor_2 = dados.groupby('Setor').mean()

        df_metricas = metricas_setor_2[['DY_12m', 'Vacancia_financeira', 'Liquidez_diaria']]
        df_metricas.columns = ['DY_12m', 'VF', 'LD']
        st.table(df_metricas)

    else:
        FIIs_filtrados.columns = [
        'FII',
        'Setor',
        'Preço Atual (R$)',
        'Liquidez Diária',
        'DY (média 12 meses)',
        'P/PVA',
        'Vacância Financeira (%)',
        'Ativos'
        ]
        
        st.markdown('##### :heavy_dollar_sign: Oportunidades', unsafe_allow_html=True)
        AgGrid(FIIs_filtrados)

        st.markdown('##### :bar_chart: Métricas por setor',
                    unsafe_allow_html=True)
        
        st.markdown("""**DY_12m:** dividend yield (média 12 meses) | **VF:** vacância financeira | **LD:** liquidez diária
                    """, unsafe_allow_html=True)   

        metricas_setor_2 = dados.groupby('Setor').mean()

        df_metricas = metricas_setor_2[['DY_12m', 'Vacancia_financeira', 'Liquidez_diaria']]
        df_metricas.columns = ['DY_12m', 'VF', 'LD']
        st.table(df_metricas)

page_names_to_funcs = {
    "Filtro Simples": main_page,
    "Oportunidades": page2,
}

st.sidebar.markdown('Criado por <span style="color:#300C62;font-size:20px"><b> **Vinícius Oviedo**</b></span>',
                    unsafe_allow_html=True)
st.sidebar.markdown("""<b> Linkedin &rarr;</b>[:iphone:](https://www.linkedin.com/in/vinicius-oviedo/)""",
                   unsafe_allow_html=True)

selected_page = st.sidebar.selectbox("", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]() 

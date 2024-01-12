# Liberies

import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
import streamlit as st
from PIL import Image

st.set_page_config(page_title='Visão Empresa', page_icon='🏢')

def clean_code(df1):
    ''' 
        Está função tem a responsabilidade de limpar o dataframe

        Tipos de limpeza:
        1. Limpando NaN
        2. Mudança de tipo de coluna
        3. Remoção de espaços nas variáveis de texto
        4. Formatação das colunas de datas
        5. Limpeza da coluna de tempo (remoção do texto da variável numérica)
        
        Input: Dataframe
        output: Dataframe
        
    '''

    # Removendo valores NaN do dataset

    for col in df1.columns:
        df1 = df1.loc[df[col] != 'NaN ', :]


    # 1. Transformando a coluna Delivery_person_Age em inteiro
    df1 = df1[~df1['Delivery_person_Age'].isnull()]
    df1 = df1[df1['Delivery_person_Age'].str.isnumeric()]

    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

    # 2. Transformando a coluna order_date de texto para data

    df1['Order_Date'] = pd.to_datetime(df['Order_Date'], format = '%d-%m-%Y')

    # 3. Transformando a coluna Ratings para decimal

    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    # 4. Removendo os Espaços nas string

    df1 = df1.reset_index()

    cols = ["ID", "Delivery_person_ID", "Road_traffic_density", "City", "Type_of_vehicle", "Festival"]

    for col in cols:
        df1[col] = df1.loc[:,col].str.strip()

    # 6. Limpando a coluna de time taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1
  
def order_metric(df1):
    '''
      Cria um gráfico de barras com o número de pedidos por dia

      input: dataframe
      output: figura
    '''
    
    
    cols = ['ID', 'Order_Date']

    df_aux = df1.loc[:, cols].groupby('Order_Date').count().reset_index()

    fig = px.bar( df_aux, x = 'Order_Date', y = 'ID')
    
    return fig 
  
      
def traffic_order_share(df1):
    '''
      Cria um gráfico de pizza com a porcentagem de pedido por tipo de trânsito

      input: dataframe
      output: figura
    '''    
    
    df_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()
    fig = px.pie(df_aux, values = 'entregas_perc', names = 'Road_traffic_density')
    return fig 
  
def traffic_order_city(df1):
    '''
      Cria um gráfico de pontos com o número de pedidos por trânsito e cidade

      input: dataframe
      output: figura
    '''
    
    df_aux = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
    fig = px.scatter(df_aux, x = 'City', y = 'Road_traffic_density', size = 'ID', color = 'City')
    return fig
  
def order_week(df1):
    '''
      Cria um gráfico de linha com o número de pedidos por semana

      input: dataframe
      output: figura
    '''  

    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%W')
    df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    fig = px.line(df_aux, x = 'week_of_year', y = 'ID')
    return fig


def draw_map(df1):
    '''
      Cria um mapa com as localizações

      input: dataframe
      output: mapa
    '''
      
    cols = ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']
    df_aux = df1.loc[:, cols].groupby(['City', 'Road_traffic_density']).median().reset_index()

    map = folium.Map()

    for index, location_info in df_aux.iterrows():
      folium.Marker([location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']],
                     popup = location_info['City']).add_to(map)

    folium_static(map, width = 1024, height = 600)
    return None 

def order_share_week(df1):
    '''
      Cria um gráfico de linhas com a quantidade de entregas feita por entregadores durante a semana 

      input: dataframe
      output: gráfico
    '''
    df_aux1 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()
    df_aux2 = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    df_aux = pd.merge(df_aux2, df_aux1, how = 'inner')
    df_aux['entregas_por_entregador'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    fig = px.line(df_aux, x = 'week_of_year', y = 'entregas_por_entregador')
    return fig
  
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  

# Import dataset
df = pd.read_csv('dataset/train.csv')

# Limpando o dataset
df1 = clean_code(df)

#++++++++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                  Barra Lateral                       #
#++++++++++++++++++++++++++++++++++++++++++++++++++++++#

st.header("Marketplace - Visão Cliente")

image = Image.open('logo.jpg')
st.sidebar.image(image=image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data limite')
date_slider = st.sidebar.slider('Até qual valor?',
                  value = pd.datetime(2022, 4, 6),
                  min_value=pd.datetime(2022, 2, 11),
                  max_value=pd.datetime(2022, 4, 13),
                  format='DD-MM-YYYY')

st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect("Quais as condições do trânsito",
                       ['Low', 'Medium', 'High', 'Jam'],
                       default='Low')

# Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]


# Filtro de Trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

#++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                  Layout do streamlit                 #
#++++++++++++++++++++++++++++++++++++++++++++++++++++++#

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
  
  with st.container():
    st.header('Orders by Day')
    fig = order_metric(df1)
    st.plotly_chart(fig)
    

  with st.container():
     
    col1, col2 = st.columns(2)
    
    with col1:
      
      st.header('Traffic Order Share')
      fig = traffic_order_share(df1)
      st.plotly_chart(fig, use_container_width=True)
      
    with col2:
      
      st.header('Traffic Order City')
      fig = traffic_order_city(df1)
      st.plotly_chart(fig, use_container_width=True)


  
with tab2:
  with st.container():
    st.header('Order by Week')  
    fig = order_week(df1)
    st.plotly_chart(fig, use_container_width=True)

    
  with st.container():
    st.header('Order Share by Week')
    fig = order_share_week(df1)
    st.plotly_chart(fig, use_container_width=True)
    
with tab3:
  st.header('Country Maps')
  draw_map(df1)
  
  





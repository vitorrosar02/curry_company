import streamlit as st
import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px
from haversine import haversine
import numpy as np
from PIL import Image

st.set_page_config(page_title='Visão Empresa', page_icon='🍔')


#---------------------------------------------------------
# Funções 
# --------------------------------------------------------

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

# ---------------------------------------------------------------------------------------------------------

# Import dataset
df = pd.read_csv('dataset/train.csv')

# Limpando o dataset
df1 = clean_code(df)

#++++++++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                  Barra Lateral                       #
#++++++++++++++++++++++++++++++++++++++++++++++++++++++#

st.header("Marketplace - Visão Restaurantes")

image = Image.open('/home/vitor/Documentos/repos/FTC-Analisando_dados/dashboard/imagens/logo.jpg')
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

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '-', '-'])

with tab1:
    
    st.title('Overall Metrics')
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with st.container():
        with col1:
            st.markdown('###### Nº Entregadores')
            total = len(df1['Delivery_person_ID'].unique())
            col1.metric('', total)
            
        with col2:
            st.markdown('###### Distância Média(KM)')
            cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude',]

            df1['Distance'] = df1.loc[:, cols].apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                             (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis = 1)
            distance = df1['Distance'].mean()
            distance_texto = f'{distance:.1f}'
            col2.metric('', distance_texto)
                        
        with col3:
            st.markdown('###### Tempo de Entrega Médio c/ Festival(Min)')
            df_aux = df1.loc[df1['Festival'] == 'Yes'].reset_index()
            time = df_aux['Time_taken(min)'].mean()
            time_texto = f'{time:.1f}'
            col3.metric('', time_texto)
        
        with col4:
            st.markdown('###### Desvio Padrão das Entregas c/ Festival')
            df_aux = df1.loc[df1['Festival'] == 'Yes'].reset_index()
            time = df_aux['Time_taken(min)'].std()
            time_texto = f'{time:.1f}'
            col4.metric('', time_texto)           
        
        with col5:
            st.markdown('###### Tempo de Entrega Médio s/ Festival(Min)')
            df_aux = df1.loc[df1['Festival'] == 'No'].reset_index()
            time = df_aux['Time_taken(min)'].mean()
            time_texto = f'{time:.1f}'
            col5.metric('', time_texto)
            
        with col6:
            st.markdown('###### Desvio Padrão das Entregas s/ Festival')
            df_aux = df1.loc[df1['Festival'] == 'No'].reset_index()
            time = df_aux['Time_taken(min)'].std()
            time_texto = f'{time:.1f}'
            col6.metric('', time_texto) 
            
    with st.container():
        st.markdown('''---''')
        st.title('Distriuição da distancia média por cidade')
        avg_distance = df1.loc[:, ['City', 'Distance']].groupby('City').mean().reset_index()
        fig = go.Figure(data = [go.Pie(labels=avg_distance['City'], values=avg_distance['Distance'], pull= [0, 0.1, 0])])
        st.plotly_chart(fig,  use_container_width=True)
        
        
    with st.container():
        st.markdown('''---''')
        st.title('Distribuição Tempo')

        col1, col2 = st.columns(2)
        
        
        with col1:
            cols = ['Time_taken(min)', 'City']

            df_aux = df1.loc[:, cols].groupby('City').agg({'Time_taken(min)' : ['mean', 'std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name = 'Control',
                                 x = df_aux['City'],
                                 y = df_aux['avg_time'],
                                 error_y=dict(type = 'data', array = df_aux['std_time'])))
            fig.update_layout(barmode = 'group')
            st.plotly_chart(fig,  use_container_width=False)
            
            
            
    with st.container():
        st.markdown('''---''')
        st.title('Tempo médio por cidade e tipo de tráfego')
        cols = ['Time_taken(min)', 'City', 'Road_traffic_density']

        df_aux = df1.loc[:, cols].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)' : ['mean', 'std']})

        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()
        
        fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time',
                          color = 'std_time', color_continuous_scale='PuBu',
                          color_continuous_midpoint=np.average(df_aux['std_time']))
        
        st.plotly_chart(fig, use_container_width=True)

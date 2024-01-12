import pandas as pd
import streamlit as st
from PIL import Image


st.set_page_config(page_title='Visão Empresa', page_icon='🛵')

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Funções 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def avg_weather(df1):
    '''
        Está função retorna um dataframe com o desvio padrão e média das avaliações por condição climática
        
        input: Dataframe
        output: Dataframe
    
    '''
    df_aux = df1.loc[:, ['Weatherconditions', 'Delivery_person_Ratings']].groupby('Weatherconditions').agg(['mean', 'std'])
    df_aux.columns = ['Weatherconditions_mean', 'Weatherconditions_std']
    df_avg_std = df_aux.reset_index()       
    return df_avg_std

            
def avg_traffic(df1):
    '''
        Está função retorna um dataframe com o desvio padrão e média das avaliações por condição de trânsito
        
        input: Dataframe
        output: Dataframe
    
    '''    
    df_aux = df1.loc[:, ['Road_traffic_density', 'Delivery_person_Ratings']].groupby('Road_traffic_density').agg(['mean', 'std'])
    df_aux.columns = ['delivery_mean', 'delivery_std']
    df_avg_std = df_aux.reset_index()
    return df_avg_std

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

def faster_delivery(df1):
    '''
        Mostra os 10 entregadores mais rápidos de cada cidade
        
        input: dataframe
        output: dataframe

    '''
    
    cols = ['Delivery_person_ID', 'City', 'Time_taken(min)']

    df2 = df1.loc[:, cols].groupby(['City', 'Delivery_person_ID']).min().sort_values(['City', 'Time_taken(min)']).reset_index()

    df_aux1 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux2 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
    df_aux3 = df2.loc[df2['City'] == 'Urban', :].head(10)

    df2 = pd.concat([df_aux1, df_aux2, df_aux3]).reset_index(drop = True)        
    return df2    

def slower_delivery(df1):
    '''
        Mostra os 10 entregadores mais lentos de cada cidade
        
        input: dataframe
        output: dataframe

    '''
    
    cols = ['Delivery_person_ID', 'City', 'Time_taken(min)']

    df2 = df1.loc[:, cols].groupby(['City', 'Delivery_person_ID']).max().sort_values(['City', 'Time_taken(min)']).reset_index()

    df_aux1 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux2 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
    df_aux3 = df2.loc[df2['City'] == 'Urban', :].head(10)

    df2 = pd.concat([df_aux1, df_aux2, df_aux3]).reset_index(drop = True)        
    return df2    

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Import dataset
df = pd.read_csv('dataset/train.csv')

# Limpando o dataset
df1 = clean_code(df)


#++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                  Barra Lateral                       #
#++++++++++++++++++++++++++++++++++++++++++++++++++++++#

st.header("Marketplace - Visão Entregadores")

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

    col1, col2, col3, col4, col5 = st.columns(5, gap='large')
    
    with col1:
        total = len(df1['Delivery_person_ID'].unique())
        col1.metric('Nº Entregadores', total)
    
    with col2:
        idade = df1.loc[:, 'Delivery_person_Age'].max() 
        col2.metric('Maior Idade', idade)
        
    with col3:
        idade = df1.loc[:, 'Delivery_person_Age'].min()       
        col3.metric('Menor Idade', idade)
        
    with col4:
        condicao = df1.loc[:, 'Vehicle_condition'].max()
        col4.metric('A melhor condição', condicao)
        
    with col5:
        condicao = df1.loc[:, 'Vehicle_condition'].min()
        col5.metric('A pior condição', condicao)
        
    with st.container():
        st.markdown('''---''')
        st.title('Avaliações')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('### Avaliação Média por Entregador')
            df_avg_ratings = df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']].groupby('Delivery_person_ID').mean().reset_index()
            st.dataframe(df_avg_ratings)
            
        with col2:
            st.markdown('### Avaliação Média por Trânsito')
            df_avg_std = avg_traffic(df1)
            st.dataframe(df_avg_std)

            
            st.markdown('### Avaliação Média por Clima')
            df_avg_std = avg_weather(df1)     
            st.dataframe(df_avg_std)
            

            
    with st.container():
        st.markdown('''---''')
        st.title('Entregas')
        
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('### Entregadores Mais Rápidos')
            df2 = faster_delivery(df1)  
            st.dataframe(df2)


        with col2:
            st.markdown('### Entregadores Mais Lentos')
            df2 = slower_delivery(df1)
            st.dataframe(df2)
        
























































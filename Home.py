import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon="🎲"
)


image = Image.open('imagens/logo.jpg')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.write("Curry Company Growth Dashboard")

st.markdown(
    '''
        Growth Dashboard foi construido para acompanhar as métricas de crescimento dos entregadores e restaurantes.
        
        ### Como utilizar esse Growth Deshboard?
        
        - Visão Empresa:
            - Visão Gerencial: Métricas gerais de comportamento.
            - Visão tática: Indicadores semanais de crescimento.
            - Visão Geográfica: insights de geolocalização.
            
        - Visão Entregadores:
            - Acompanhamento dos indicadores semanais de crescimento.
            
        - Visão Restaurantes:
            - Indicadores semanais de crescimento dos restaurantes.
            
        ### Ask for Help
        
        - Time de Data Science
            - vitorrosar.fsc@gmail.com
        
    '''
)





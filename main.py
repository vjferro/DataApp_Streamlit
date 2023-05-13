import streamlit as st 
from PIL import Image
import json
import pandas as pd
import collections
import plotly.express as px
from streamlit_extras.colored_header import colored_header
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
from streamlit_extras.metric_cards import style_metric_cards
import plotly.figure_factory as ff

## configuração de página
st.set_page_config(page_title="DataAPP", layout='wide')
## Css
with open('css/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

## retirando marca d'agua
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


#### Imagem, texto, importação de dados
image = Image.open('imagens/logo sem legenda.png')
dados = pd.read_csv('dados/vgsales.csv')
dados.dropna(inplace=True)
dados['Ano'] = dados['Ano'].astype(int)
with open("Texto/texto2.txt", "r") as arquivo:
	texto = arquivo.read()

def carregarsvg (file:str):
     with open(file,"r") as f:
          return json.load(f)

svg = carregarsvg('sgv/76498-data-analysis-animation.json')

####

with st.sidebar:
    st.image(image)
    selecao = option_menu(
        menu_title= 'Menu',
        options=['Início', 'Dados', 'Dashboard'],
        icons=['house', 'dice-6', 'bar-chart']
    )
    
if selecao == 'Início':
    st.markdown("<h1 style='text-align:center;'>  Bem-vindo ao Data APP 📊</h1>", unsafe_allow_html=True)
    st.divider()
    bl1, bl2,bl3 = st.columns(3)
    with bl2:
        st_lottie(
            svg,
             speed=1,
            reverse=False,
            loop=True,
            quality="low",
            height=400,
            width=400,
            
               
        ) ## animação da tela inicial 
if selecao == 'Dados':
    st.markdown("<h1 style='text-align:center;'>  Dados 🎲</h1>", unsafe_allow_html=True)
    st.divider()
    st.markdown(texto)
    st.markdown("<h1 style='text-align:center;'>Visualizando o DataFrame 📑</h1>", unsafe_allow_html=True)
    st.divider()
    filtro = dataframe_explorer(dados, case=False)
    st.dataframe(filtro, use_container_width=True)
    st.markdown("<h1 style='text-align:center;'>Sumário Estatístico 📔</h1>", unsafe_allow_html=True)
    st.divider()
    st.dataframe(dados.describe())


if selecao == 'Dashboard':
    st.markdown("<h1 style='text-align:center;'> Dashboard 📈📉📊</h1>", unsafe_allow_html=True)
    st.divider()
    col1,col2,col3 = st.columns(3)
    ### cartões
    Vendas_America = round(dados['Vendas_América'].sum(),2)
    col1.metric(label="Total de Vendas na América", value=Vendas_America)
    Vendas_Japao = round(dados['Vendas_Japão'].sum(),2)
    col2.metric(label="Total de Vendas no Japão", value=Vendas_Japao)  
    Vendas_europa = round(dados['Vendas_Europa'].sum(),2)
    col3.metric(label="Total de Vendas na Europa",value=Vendas_europa)
    style_metric_cards()

    ### vendas por ano
    ano_agrupado = dados.groupby(['Ano']).sum()
    fig_ano = px.line(ano_agrupado, x=ano_agrupado.index, y='Vendas_Globais', title='Vendas de Games por Ano')
    fig_ano.update_layout(title_x = 0.4)
    st.plotly_chart(fig_ano, use_container_width=True)
    ### vendas por região
    vendas = px.bar(ano_agrupado, x=ano_agrupado.index, y=['Vendas_América','Vendas_Japão','Vendas_Europa'], title='Vendas por Região' )
    vendas.update_layout(title_x = 0.4)
    st.plotly_chart(vendas, use_container_width=True)
    ### Top 10 empresas por vendas globais
    editora_agrupado = dados.groupby(['Editora']).sum()
    top10_editoras = editora_agrupado.sort_values(['Vendas_Globais'], ascending=False).head(10)
    top10 = px.bar(top10_editoras, y=top10_editoras.index, x='Vendas_Globais', orientation='h', text_auto='.2s', title='Principais empresas em Vendas Globais')
    top10.update_layout(title_x = 0.4)
    st.plotly_chart(top10, use_container_width=True)
    ### Quantidade de jogos por gênero
    Genero = dados.groupby(['Gênero']).sum()
    generofig = px.bar(Genero, y=Genero.index, x=['Vendas_América', 'Vendas_Europa','Vendas_Japão','Outras_Vendas'],orientation='h', title= "Vendas de jogos por gênero e região" )
    generofig.update_layout(title_x = 0.4)
    st.plotly_chart(generofig, use_container_width=True)
    
 

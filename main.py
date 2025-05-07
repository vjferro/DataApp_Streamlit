import streamlit as st
from PIL import Image
import pandas as pd
import json
import plotly.express as px
from streamlit_extras.colored_header import colored_header
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
from streamlit_extras.metric_cards import style_metric_cards

# ========== CONFIGURAÇÃO DA PÁGINA ==========
st.set_page_config(page_title="DataAPP", layout='wide', initial_sidebar_state='expanded')

# ========== CSS PERSONALIZADO ==========
with open('css/style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

hide_st_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# ========== FUNÇÕES ==========
@st.cache_data
def carregar_dados():
    df = pd.read_csv('dados/vgsales.csv')
    df.dropna(inplace=True)
    df['Ano'] = df['Ano'].astype(int)
    return df

def carregar_svg(path):
    with open(path, "r") as f:
        return json.load(f)

# ========== CARREGAMENTO DE DADOS ==========
with st.spinner("Carregando dados..."):
    dados = carregar_dados()
    
    # Corrigido: leitura segura do texto
    with open("Texto/texto2.txt", "r", encoding="utf-8", errors="ignore") as arquivo:
        texto = arquivo.read()
    
    lottie_anim = carregar_svg("sgv/76498-data-analysis-animation.json")
    logo = Image.open("imagens/logo sem legenda.png")

# ========== SIDEBAR ==========
with st.sidebar:
    st.image(logo, use_column_width=True)
    selecao = option_menu(
        menu_title="Navegação",
        options=["Início", "Dados", "Dashboard"],
        icons=["house", "table", "bar-chart"],
        menu_icon="cast",
        default_index=0
    )

# ========== INÍCIO ==========
if selecao == "Início":
    st.markdown("<h1 style='text-align: center;'>Bem-vindo ao Data APP 📊</h1>", unsafe_allow_html=True)
    st.divider()
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st_lottie(lottie_anim, height=400, width=400, speed=1)

# ========== DADOS ==========
elif selecao == "Dados":
    st.markdown("<h1 style='text-align: center;'>Análise de Dados 🎲</h1>", unsafe_allow_html=True)
    colored_header(label="", description="", color_name="blue-70")
    st.info("Este conjunto de dados mostra as vendas globais de jogos de vídeo game por região, plataforma, gênero e editora.")
    st.markdown(texto)

    st.markdown("### 🔍 Explore os dados")
    filtro = dataframe_explorer(dados, case=False)
    st.dataframe(filtro, use_container_width=True)

    st.markdown("### 📘 Sumário Estatístico")
    tab1, tab2 = st.tabs(["Sumário", "Tipos de Dados"])
    with tab1:
        st.dataframe(dados.describe(), use_container_width=True)
    with tab2:
        st.dataframe(pd.DataFrame(dados.dtypes, columns=["Tipo"]), use_container_width=True)

# ========== DASHBOARD ==========
elif selecao == "Dashboard":
    st.markdown("<h1 style='text-align: center;'>Dashboard Interativo 📈</h1>", unsafe_allow_html=True)
    colored_header(label="", description="", color_name="blue-70")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Vendas na América", f"{dados['Vendas_América'].sum():,.2f} M")
    col2.metric("Total de Vendas no Japão", f"{dados['Vendas_Japão'].sum():,.2f} M")
    col3.metric("Total de Vendas na Europa", f"{dados['Vendas_Europa'].sum():,.2f} M")
    style_metric_cards()

    st.markdown("### 📊 Vendas Globais por Ano")
    ano_agrupado = dados.groupby('Ano').sum(numeric_only=True)
    fig_ano = px.line(ano_agrupado, x=ano_agrupado.index, y="Vendas_Globais", markers=True, title="Vendas de Jogos por Ano")
    fig_ano.update_layout(title_x=0.4)
    st.plotly_chart(fig_ano, use_container_width=True)

    st.markdown("### 🌎 Vendas por Região")
    fig_region = px.bar(
        ano_agrupado,
        x=ano_agrupado.index,
        y=["Vendas_América", "Vendas_Europa", "Vendas_Japão"],
        barmode="group",
        title="Comparativo de Vendas por Região"
    )
    fig_region.update_layout(title_x=0.4)
    st.plotly_chart(fig_region, use_container_width=True)

    st.markdown("### 🏆 Top 10 Editoras por Vendas Globais")
    top_editoras = dados.groupby("Editora").sum(numeric_only=True).sort_values("Vendas_Globais", ascending=False).head(10)
    fig_top = px.bar(
        top_editoras,
        x="Vendas_Globais",
        y=top_editoras.index,
        orientation="h",
        text_auto=".2s",
        title="Editoras com Maiores Vendas Globais"
    )
    fig_top.update_layout(title_x=0.4)
    st.plotly_chart(fig_top, use_container_width=True)

    st.markdown("### 🎮 Vendas por Gênero e Região")
    genero_agrupado = dados.groupby("Gênero").sum(numeric_only=True)
    fig_gen = px.bar(
        genero_agrupado,
        x=["Vendas_América", "Vendas_Europa", "Vendas_Japão", "Outras_Vendas"],
        y=genero_agrupado.index,
        orientation="h",
        title="Vendas por Gênero e Região"
    )
    fig_gen.update_layout(title_x=0.4)
    st.plotly_chart(fig_gen, use_container_width=True)

# -*- coding: utf-8 -*-
# Salve este código como app.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# --- Configuração da Página ---
st.set_page_config(
    page_title="Análise de Renda",
    page_icon="💰",
    layout="wide"
)

# --- Função para Carregar os Dados ---
@st.cache_data
def carregar_dados(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        st.error(f"Arquivo de dados não encontrado: '{caminho_arquivo}'")
        return None
    df = pd.read_csv(caminho_arquivo)
    df = df.drop(columns=['Unnamed: 0'], errors='ignore')
    df['data_ref'] = pd.to_datetime(df['data_ref'])
    df['tempo_emprego'] = df['tempo_emprego'].fillna(df['tempo_emprego'].median())
    return df

# --- Título do Dashboard ---
st.title('💰 Análise Interativa de Previsão de Renda')

# --- Carregamento dos Dados ---
df = carregar_dados('previsao_de_renda.csv')

if df is not None:
    # --- Barra Lateral de Filtros ---
    st.sidebar.header('Filtros')
    
    genero = st.sidebar.multiselect(
        'Gênero',
        options=df['sexo'].unique(),
        default=df['sexo'].unique()
    )
    
    posse_imovel = st.sidebar.multiselect(
        'Posse de Imóvel',
        options=df['posse_de_imovel'].unique(),
        default=df['posse_de_imovel'].unique()
    )

    df_filtrado = df[df['sexo'].isin(genero) & df['posse_de_imovel'].isin(posse_imovel)]

    # --- Gráficos Principais ---
    st.header('Análises Bivariadas')
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Renda Média por Nível de Educação')
        fig, ax = plt.subplots()
        sns.barplot(x='educacao', y='renda', data=df_filtrado, ci=None, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with col2:
        st.subheader('Distribuição da Renda por Gênero')
        fig, ax = plt.subplots()
        sns.boxplot(x='sexo', y='renda', data=df_filtrado, ax=ax)
        plt.ylim(0, df_filtrado['renda'].quantile(0.95))
        st.pyplot(fig)

    # --- Tabela de Dados ---
    st.markdown("---")
    st.header('Dados Detalhados')
    st.dataframe(df_filtrado)

import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="🎮 Controle de Jogos", layout="centered")

ARQUIVO = "Lista de Jogos_ver1.xlsx"

# Carregar dados
if os.path.exists(ARQUIVO):
    df = pd.read_excel(ARQUIVO)
else:
    df = pd.DataFrame(columns=["Plataforma", "Console", "Jogo"])

st.title("🎮 Controle de Coleção de Jogos")
st.markdown("---")

# Formulário para adicionar novo jogo
st.subheader("➕ Adicionar novo jogo")
with st.form("form_jogo"):
    col1, col2 = st.columns(2)
    plataformas_opcoes = ["Playstation", "Xbox", "Nintendo", "PC", "Mega Drive", "Switch", "Outra"]

    with col1:
        plataforma = st.selectbox("🕹️ Plataforma", plataformas_opcoes)
    with col2:
        console = st.text_input("🧩 Console")

    jogo = st.text_input("🎮 Nome do Jogo")
    enviar = st.form_submit_button("Adicionar")

    if enviar and jogo:
        novo = pd.DataFrame([[plataforma, console, jogo]], columns=df.columns)
        df = pd.concat([df, novo], ignore_index=True)
        df.to_excel(ARQUIVO, index=False)
        st.success(f"✅ '{jogo}' adicionado com sucesso!")

st.markdown("---")
st.subheader("🔍 Buscar jogos")

filtro = st.text_input("Filtrar por nome, plataforma ou console")
if filtro:
    filtrado = df[df.apply(lambda row: filtro.lower() in row.astype(str).str.lower().to_string(), axis=1)]
    st.dataframe(filtrado, use_container_width=True)
else:
    st.dataframe(df, use_container_width=True)

st.markdown("---")
st.subheader("🗑️ Remover jogo")

if not df.empty:
    idx = st.number_input("Digite o índice do jogo para remover", min_value=0, max_value=len(df)-1, step=1)
    if st.button("Remover"):
        st.warning(f"❌ Removido: {df.iloc[idx]['Jogo']}")
        df = df.drop(index=idx).reset_index(drop=True)
        df.to_excel(ARQUIVO, index=False)

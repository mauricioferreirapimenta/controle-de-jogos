
import streamlit as st
import pandas as pd
import os

ARQUIVO = "Lista_de_Jogos.xlsx"

# Carregar dados
if os.path.exists(ARQUIVO):
    df = pd.read_excel(ARQUIVO)
else:
    df = pd.DataFrame(columns=["Plataforma", "Console", "Jogo"])

st.title("🎮 Controle de Coleção de Jogos")

# Formulário para adicionar jogo
st.subheader("Adicionar novo jogo")
with st.form("form_jogo"):
    plataforma = st.selectbox("Plataforma", sorted(df["Plataforma"].unique().tolist() + ["Outra"]))
    console = st.text_input("Console")
    jogo = st.text_input("Nome do Jogo")
    enviar = st.form_submit_button("Adicionar")

    if enviar and jogo:
        novo = pd.DataFrame([[plataforma, console, jogo]], columns=df.columns)
        df = pd.concat([df, novo], ignore_index=True)
        df.to_excel(ARQUIVO, index=False)
        st.success(f"✅ '{jogo}' adicionado com sucesso!")

# Buscar jogos
st.subheader("Buscar jogos")
filtro = st.text_input("Filtrar por nome, plataforma ou console")
if filtro:
    filtrado = df[df.apply(lambda row: filtro.lower() in row.astype(str).str.lower().to_string(), axis=1)]
    st.dataframe(filtrado)
else:
    st.dataframe(df)

# Remover jogo
st.subheader("Remover jogo")
if not df.empty:
    idx = st.number_input("Digite o índice do jogo para remover", min_value=0, max_value=len(df)-1, step=1)
    if st.button("Remover"):
        st.warning(f"Removido: {df.iloc[idx]['Jogo']}")
        df = df.drop(index=idx).reset_index(drop=True)
        df.to_excel(ARQUIVO, index=False)

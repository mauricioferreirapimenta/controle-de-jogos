
import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="🎮 Controle de Jogos", layout="centered")

ARQUIVO = "Lista de Jogos_ver1.xlsx"

# Verifica se o arquivo existe e carrega, senão cria novo DataFrame
if os.path.exists(ARQUIVO):
    df = pd.read_excel(ARQUIVO)
else:
    df = pd.DataFrame(columns=[
        "Plataforma", "Console", "Jogo", "Gênero", "Status", "Nota", 
        "Tempo (h)", "Início", "Fim", "Observações"
    ])

st.title("🎮 Controle de Coleção de Jogos")
st.markdown("---")

# Formulário de cadastro
st.subheader("➕ Adicionar novo jogo")
with st.form("form_jogo"):
    col1, col2 = st.columns(2)
    plataformas_opcoes = ["Playstation", "Xbox", "Nintendo", "PC", "Mega Drive", "Switch", "Outra"]
    status_opcoes = ["Jogando", "Zerado", "Parado", "Nunca Joguei"]
    generos_opcoes = ["Ação", "Aventura", "RPG", "Corrida", "Esporte", "Puzzle", "Terror", "Simulação", "Outro"]

    with col1:
        plataforma = st.selectbox("🕹️ Plataforma", plataformas_opcoes)
        genero = st.selectbox("🎲 Gênero", generos_opcoes)
        nota = st.slider("⭐ Nota pessoal", 0, 10, 0)
        inicio = st.date_input("📅 Início", value=date.today())

    with col2:
        console = st.text_input("🧩 Console")
        status = st.selectbox("📍 Status", status_opcoes)
        tempo = st.number_input("⏱️ Tempo jogado (horas)", min_value=0)
        fim = st.date_input("📅 Fim", value=date.today())

    jogo = st.text_input("🎮 Nome do Jogo")
    obs = st.text_area("📝 Observações")
    enviar = st.form_submit_button("Adicionar")

    if enviar and jogo:
        novo = pd.DataFrame([{
            "Plataforma": plataforma,
            "Console": console,
            "Jogo": jogo,
            "Gênero": genero,
            "Status": status,
            "Nota": nota,
            "Tempo (h)": tempo,
            "Início": inicio,
            "Fim": fim,
            "Observações": obs
        }])
        df = pd.concat([df, novo], ignore_index=True)
        df.to_excel(ARQUIVO, index=False)
        st.success(f"✅ '{jogo}' adicionado com sucesso!")

st.markdown("---")
st.subheader("🔍 Buscar jogos")
filtro = st.text_input("Filtrar por qualquer campo")
if filtro:
    filtrado = df[df.apply(lambda row: filtro.lower() in row.astype(str).str.lower().to_string(), axis=1)]
    st.dataframe(filtrado.sort_values(by=["Plataforma", "Console", "Jogo"]), use_container_width=True)
else:
    df_ordenado = df.sort_values(by=["Plataforma", "Console", "Jogo"])
    st.dataframe(df_ordenado, use_container_width=True)

st.markdown("---")
st.subheader("🗑️ Remover jogo")
if not df.empty:
    idx = st.number_input("Digite o índice do jogo para remover", min_value=0, max_value=len(df)-1, step=1)
    if st.button("Remover"):
        st.warning(f"❌ Removido: {df.iloc[idx]['Jogo']}")
        df = df.drop(index=idx).reset_index(drop=True)
        df.to_excel(ARQUIVO, index=False)

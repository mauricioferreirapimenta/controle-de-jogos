
import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="🎮 Controle de Jogos", layout="centered")

ARQUIVO = "Lista de Jogos_ver1.xlsx"

colunas = [
    "Plataforma", "Console", "Gênero", "Jogo", "Mídia", "Edição",
    "Condição", "Status", "Nota", "Tempo (h)", "Início", "Fim",
    "Observações coleção", "Comentários pessoais"
]

if os.path.exists(ARQUIVO):
    df = pd.read_excel(ARQUIVO)
else:
    df = pd.DataFrame(columns=colunas)

consoles_por_plataforma = {
    "Playstation": ["PS1", "PS2", "PS3", "PS4", "PS5", "PSP", "PS Vita"],
    "Xbox": ["Xbox", "Xbox 360", "Xbox One", "Xbox Series S", "Xbox Series X"],
    "Nintendo": ["NES", "SNES", "Nintendo 64", "GameCube", "Wii", "Wii U", "Switch", "3DS", "DS"],
    "Sega": ["Master System", "Mega Drive", "Saturn", "Dreamcast"],
    "Outra": []
}

st.title("🎮 Controle de Coleção e Progresso de Jogos")
st.markdown("---")

st.subheader("🗃️ Adicionar novo jogo à coleção")
with st.form("adicionar_jogo"):
    col1, col2 = st.columns(2)
    plataformas_opcoes = list(consoles_por_plataforma.keys())
    generos_opcoes = ["Ação", "Aventura", "RPG", "Corrida", "Esporte", "Puzzle", "Terror", "Simulação", "Outro"]
    midia_opcoes = ["Físico", "Digital", "Cartucho", "CD/DVD", "Outro"]
    edicao_opcoes = ["Standard", "Deluxe", "Colecionador", "Outro"]

    with col1:
        plataforma = st.selectbox("Plataforma", plataformas_opcoes)
        genero = st.selectbox("Gênero", generos_opcoes)
        midia = st.selectbox("Mídia", midia_opcoes)
        condicao = st.text_input("Condição / Observações de coleção")

    with col2:
        console = st.text_input("Console")
        edicao = st.selectbox("Edição", edicao_opcoes)
        jogo = st.text_input("Nome do Jogo")
        obs_colecao = st.text_area("Observações gerais da mídia")

    enviar = st.form_submit_button("Adicionar à coleção")
    if enviar and jogo:
        novo = pd.DataFrame([{
            "Plataforma": plataforma,
            "Console": console,
            "Gênero": genero,
            "Jogo": jogo,
            "Mídia": midia,
            "Edição": edicao,
            "Condição": condicao,
            "Status": "",
            "Nota": "",
            "Tempo (h)": "",
            "Início": "",
            "Fim": "",
            "Observações coleção": obs_colecao,
            "Comentários pessoais": ""
        }])
        df = pd.concat([df, novo], ignore_index=True)
        df.to_excel(ARQUIVO, index=False)
        st.success(f"✅ '{jogo}' adicionado à coleção!")

st.markdown("---")

st.subheader("🛠️ Editar informações de gameplay")
if not df.empty:
    idx = st.selectbox("Selecione o jogo para editar", df["Jogo"])
    jogo_selecionado = df[df["Jogo"] == idx].index[0]

    with st.form("editar_jogo"):
        status_opcoes = ["Jogando", "Zerado", "Parado", "Nunca Joguei"]
        status = st.selectbox("📍 Status", status_opcoes)
        nota = st.slider("⭐ Nota pessoal", 0, 10, 0)
        tempo = st.number_input("⏱️ Tempo jogado (horas)", min_value=0)
        inicio = st.date_input("📅 Data de início", value=date.today())
        fim = st.date_input("📅 Data de término", value=date.today())
        comentarios = st.text_area("📝 Comentários pessoais sobre o jogo")

        salvar_edicao = st.form_submit_button("Salvar edição")
        if salvar_edicao:
            df.at[jogo_selecionado, "Status"] = status
            df.at[jogo_selecionado, "Nota"] = nota
            df.at[jogo_selecionado, "Tempo (h)"] = tempo
            df.at[jogo_selecionado, "Início"] = inicio
            df.at[jogo_selecionado, "Fim"] = fim
            df.at[jogo_selecionado, "Comentários pessoais"] = comentarios
            df.to_excel(ARQUIVO, index=False)
            st.success("✅ Jogo atualizado com sucesso!")

st.markdown("---")
st.subheader("📋 Listagem de jogos")
if not df.empty:
    df_exibicao = df[colunas].sort_values(by=["Plataforma", "Console", "Jogo"])
    st.dataframe(df_exibicao, use_container_width=True)

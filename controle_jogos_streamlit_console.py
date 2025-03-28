
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

# Carregar ou iniciar o DataFrame
if os.path.exists(ARQUIVO):
    df = pd.read_excel(ARQUIVO)
else:
    df = pd.DataFrame(columns=colunas)

# Mapeamento de plataformas atualizadas
consoles_por_plataforma = {
    "Playstation": ["PS1", "PS2", "PS3", "PS4", "PS5", "PSP", "PS Vita"],
    "Xbox": ["Xbox", "Xbox 360", "Xbox One", "Xbox Series S", "Xbox Series X"],
    "Nintendo": ["NES", "SNES", "Nintendo 64", "GameCube", "Wii", "Wii U", "Switch", "3DS", "DS"],
    "Sega": ["Master System", "Mega Drive", "Saturn", "Dreamcast"],
    "Outra": []
}

st.title("🎮 Controle de Coleção e Progresso de Jogos")
st.markdown("---")

# Seção: Adicionar novo jogo
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
        opcoes_console = consoles_por_plataforma.get(plataforma, [])
        if opcoes_console:
            console = st.selectbox("Console", opcoes_console)
        else:
            console = st.text_input("Console (escreva manualmente)")
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

# Exibe tabela ordenada
st.markdown("---")
st.subheader("📋 Lista de jogos")
if not df.empty:
    colunas_ordenadas = colunas
    df_exibicao = df[colunas_ordenadas].sort_values(by=["Plataforma", "Console", "Jogo"])
    st.dataframe(df_exibicao, use_container_width=True)

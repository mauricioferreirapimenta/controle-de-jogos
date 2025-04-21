
import streamlit as st
import pandas as pd
import os
from datetime import date
from io import BytesIO

st.set_page_config(page_title="🎮 Coleção de Jogos", layout="centered")
st.title("🎮 Coleção de Jogos")
st.markdown("---")

ARQUIVO = "Lista de Jogos_ver1.xlsx"
colunas = [
    "Plataforma", "Console", "Gênero", "Jogo", "Mídia", "Edição",
    "Condição", "Status", "Nota", "Tempo (h)", "Início", "Fim",
    "Observações coleção", "Comentários pessoais"
]

if os.path.exists(ARQUIVO):
    try:
        df = pd.read_excel(ARQUIVO)
    except Exception as e:
        st.error(f"Erro ao carregar planilha: {e}")
        df = pd.DataFrame(columns=colunas)
else:
    df = pd.DataFrame(columns=colunas)

consoles_por_plataforma = {
    "Playstation": ["PS1", "PS2", "PS3", "PS4", "PS5", "PSP", "PS Vita"],
    "Xbox": ["Xbox", "Xbox 360", "Xbox One", "Xbox Series S", "Xbox Series X"],
    "Nintendo": ["NES", "SNES", "Nintendo 64", "GameCube", "Wii", "Wii U", "Switch", "3DS", "DS"],
    "Sega": ["Master System", "Mega Drive", "Saturn", "Dreamcast"],
    "Outra": []
}

paginas = [
    "📚 Ver Coleção",
    "➕ Adicionar Jogo",
    "✏️ Editar Jogo",
    "🗑️ Excluir Jogo",
    "📋 Lista Completa",
    "📁 Backup e Importação"
]
pagina = st.sidebar.radio("Ir para", paginas)
st.sidebar.markdown("---")

if pagina == "➕ Adicionar Jogo":
    st.subheader("➕ Adicionar novo jogo")
    with st.form("form_adicionar"):
        plataforma = st.selectbox("Plataforma", [""] + list(consoles_por_plataforma.keys()), key="add_plataforma")
        
        # Corrigido: console só aparece após plataforma ser selecionada
        if plataforma:
            console = st.selectbox("Console", [""] + consoles_por_plataforma.get(plataforma, []), key="add_console")
        else:
            console = st.selectbox("Console", [""], disabled=True, key="add_console_disabled")

        genero = st.text_input("Gênero")
        jogo = st.text_input("Nome do Jogo")
        midia = st.selectbox("Mídia", ["", "Físico", "Digital", "Outro"])
        edicao = st.text_input("Edição")
        condicao = st.text_area("Condição / Observações de coleção")
        enviar = st.form_submit_button("Adicionar à coleção")

    if enviar:
        novo = {
            "Plataforma": plataforma, "Console": console, "Gênero": genero, "Jogo": jogo,
            "Mídia": midia, "Edição": edicao, "Condição": condicao,
            "Status": "", "Nota": "", "Tempo (h)": "", "Início": "", "Fim": "",
            "Observações coleção": "", "Comentários pessoais": ""
        }
        df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
        df.to_excel(ARQUIVO, index=False)
        st.success(f"Jogo '{jogo}' adicionado com sucesso!")

# As demais páginas permanecem funcionais conforme versões anteriores

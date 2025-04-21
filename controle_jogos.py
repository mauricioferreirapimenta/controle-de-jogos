
import streamlit as st
import pandas as pd
import os
from datetime import date
from io import BytesIO

# -------------------------------
# 📂 Inicialização
# -------------------------------
def autenticar():
    with st.sidebar:
        st.markdown("## 🔐 Login")
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if usuario == "admin" and senha == "1234":
                st.session_state["autenticado"] = True
            else:
                st.error("Usuário ou senha incorretos")

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

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

st.set_page_config(page_title="🎮 Controle de Jogos", layout="centered")
st.title("🎮 Controle de Coleção e Progresso de Jogos")
st.markdown("---")

if not st.session_state["autenticado"]:
    st.info("🔒 Acesso limitado - apenas visualização")
    autenticar()
    st.stop()

# -------------------------------
# 📂 Navegação lateral
# -------------------------------
paginas = [
    "➕ Adicionar Jogo",
    "✏️ Editar Jogo",
    "🗑️ Excluir Jogo",
    "📁 Navegar por Plataforma",
    "📋 Lista Completa",
    "📁 Backup e Importação"
]
pagina = st.sidebar.radio("Ir para", paginas)
st.sidebar.markdown("---")


import streamlit as st
import pandas as pd
import os
from datetime import date
from io import BytesIO

# Autenticação
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
    st.dataframe(df[colunas].sort_values(by=["Plataforma", "Console", "Jogo"]), use_container_width=True)
    autenticar()
    st.stop()

# Aqui entraria a continuação com campos de jogo oculto por etapa


# -------------------------------
# ✏️ Editar jogo
# -------------------------------
st.markdown("---")
st.subheader("✏️ Editar jogo")
plat_edit = st.selectbox("Plataforma", [""] + sorted(df["Plataforma"].dropna().unique()), key="edit_plat")
if plat_edit:
    console_edit = st.selectbox("Console", [""] + sorted(df[df["Plataforma"] == plat_edit]["Console"].dropna().unique()), key="edit_console")
else:
    console_edit = ""

if plat_edit and console_edit:
    jogos_edit = df[(df["Plataforma"] == plat_edit) & (df["Console"] == console_edit)]["Jogo"].unique()
    jogo_sel = st.selectbox("Jogo", [""] + list(jogos_edit), key="edit_jogo")
else:
    jogo_sel = ""

with st.form("editar_jogo_form"):
    if jogo_sel:
        idx = df[(df["Plataforma"] == plat_edit) & (df["Console"] == console_edit) & (df["Jogo"] == jogo_sel)].index[0]
        status = st.selectbox("Status", ["", "Jogando", "Zerado", "Parado", "Nunca Joguei"])
        nota = st.slider("Nota pessoal", 0, 10, int(df.at[idx, "Nota"] or 0))
        tempo = st.number_input("Tempo jogado (h)", min_value=0, value=int(df.at[idx, "Tempo (h)"] or 0))
        inicio = st.date_input("Data início", value=date.today())
        fim = st.date_input("Data fim", value=date.today())
        comentarios = st.text_area("Comentários pessoais", value=df.at[idx, "Comentários pessoais"])

        if st.form_submit_button("Salvar edição"):
            df.at[idx, "Status"] = status
            df.at[idx, "Nota"] = nota
            df.at[idx, "Tempo (h)"] = tempo
            df.at[idx, "Início"] = inicio
            df.at[idx, "Fim"] = fim
            df.at[idx, "Comentários pessoais"] = comentarios
            df.to_excel(ARQUIVO, index=False)
            st.success("Jogo editado com sucesso!")

# -------------------------------
# 🗑️ Excluir jogo
# -------------------------------
st.markdown("---")
st.subheader("🗑️ Excluir jogo")
plat_excluir = st.selectbox("Plataforma", [""] + sorted(df["Plataforma"].dropna().unique()), key="excluir_plat")
if plat_excluir:
    console_excluir = st.selectbox("Console", [""] + sorted(df[df["Plataforma"] == plat_excluir]["Console"].dropna().unique()), key="excluir_console")
else:
    console_excluir = ""

if plat_excluir and console_excluir:
    jogos_excluir = df[(df["Plataforma"] == plat_excluir) & (df["Console"] == console_excluir)]["Jogo"].unique()
    jogo_excluir = st.selectbox("Jogo", [""] + list(jogos_excluir), key="excluir_jogo")
else:
    jogo_excluir = ""

if jogo_excluir and st.button("Excluir jogo selecionado"):
    df = df[~((df["Plataforma"] == plat_excluir) & (df["Console"] == console_excluir) & (df["Jogo"] == jogo_excluir))]
    df.to_excel(ARQUIVO, index=False)
    st.success(f"'{jogo_excluir}' excluído com sucesso!")

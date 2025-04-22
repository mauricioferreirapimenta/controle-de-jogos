
import streamlit as st
import pandas as pd
import os
from datetime import date
from io import BytesIO

st.set_page_config(page_title="🎮 Coleção de Jogos", layout="centered")
st.title("🎮 Coleção de Jogos")
st.markdown("---")

ARQUIVO = "Lista de Jogos_ver1.xlsx"
COLUNAS = [
    "Plataforma", "Console", "Gênero", "Jogo", "Mídia", "Edição",
    "Condição", "Status", "Nota", "Tempo (h)", "Início", "Fim",
    "Observações coleção", "Comentários pessoais", "Data de lançamento"
]

if os.path.exists(ARQUIVO):
    try:
        df = pd.read_excel(ARQUIVO)
        for col in COLUNAS:
            if col not in df.columns:
                df[col] = ""
    except Exception as e:
        st.error(f"Erro ao carregar planilha: {e}")
        df = pd.DataFrame(columns=COLUNAS)
else:
    df = pd.DataFrame(columns=COLUNAS)

def data_segura(valor):
    if pd.isnull(valor) or valor in ["", "None", None]:
        return date.today()
    try:
        return pd.to_datetime(valor).date()
    except:
        return date.today()
CONSOLES = {
    "Playstation": ["PS1", "PS2", "PS3", "PS4", "PS5", "PSP", "PS Vita"],
    "Xbox": ["Xbox", "Xbox 360", "Xbox One", "Xbox Series S", "Xbox Series X"],
    "Nintendo": ["NES", "SNES", "Nintendo 64", "GameCube", "Wii", "Wii U", "Switch", "3DS", "DS"],
    "Sega": ["Master System", "Mega Drive", "Saturn", "Dreamcast"],
    "Outra": []
}

pagina = st.sidebar.radio("Ir para", [
    "📚 Ver Coleção",
    "➕ Adicionar Jogo",
    "✏️ Editar Jogo",
    "🗑️ Excluir Jogo",
    "📋 Lista Completa",
    "📁 Backup e Importação"
])

if pagina == "📚 Ver Coleção":
    st.subheader("📚 Ver Coleção")
    if df.empty:
        st.info("Nenhum jogo cadastrado ainda.")
    else:
        plataforma = st.selectbox("Plataforma", [""] + sorted(df["Plataforma"].dropna().unique()))
        if plataforma:
            df_plat = df[df["Plataforma"] == plataforma]
            st.markdown(f"**Total de jogos na plataforma _{plataforma}_: {df_plat.shape[0]}**")
            console = st.selectbox("Console", [""] + sorted(df_plat["Console"].dropna().unique()))
            if console:
                df_con = df_plat[df_plat["Console"] == console]
                st.markdown(f"**Total de jogos no console _{console}_: {df_con.shape[0]}**")
                jogo = st.selectbox("Jogo", [""] + sorted(df_con["Jogo"].dropna().unique()))
                if jogo:
                    st.dataframe(df_con[df_con["Jogo"] == jogo])

if pagina == "➕ Adicionar Jogo":
    st.subheader("➕ Adicionar novo jogo")
    plataforma = st.selectbox("Plataforma", [""] + list(CONSOLES.keys()))
    if plataforma:
        with st.form("form_adicionar"):
            console = st.selectbox("Console", [""] + CONSOLES[plataforma])
            genero = st.text_input("Gênero")
            jogo = st.text_input("Nome do Jogo")
            midia = st.selectbox("Mídia", ["", "Física", "Digital", "Outro"])
            edicao = st.text_input("Edição")
            condicao = st.text_area("Condição")
            data_lancamento = st.date_input("Data de lançamento", value=date.today())
            enviar = st.form_submit_button("Adicionar")
        if enviar:
            novo = {
                "Plataforma": plataforma, "Console": console, "Gênero": genero, "Jogo": jogo,
                "Mídia": midia, "Edição": edicao, "Condição": condicao,
                "Status": "", "Nota": "", "Tempo (h)": "", "Início": "", "Fim": "",
                "Observações coleção": "", "Comentários pessoais": "",
                "Data de lançamento": data_lancamento
            }
            df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
            df.to_excel(ARQUIVO, index=False)
            st.success("Jogo adicionado com sucesso!")


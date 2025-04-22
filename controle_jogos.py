
import streamlit as st
import pandas as pd
import os
from datetime import date, datetime
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
    try:
        if isinstance(valor, date):
            return valor
        return pd.to_datetime(valor, errors="coerce").date()
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

if pagina == "✏️ Editar Jogo":
    st.subheader("✏️ Editar jogo")
    if df.empty:
        st.info("Nenhum jogo para editar.")
    else:
        plataforma = st.selectbox("Plataforma", [""] + sorted(df["Plataforma"].dropna().unique()))
        if plataforma:
            console = st.selectbox("Console", sorted(df[df["Plataforma"] == plataforma]["Console"].dropna().unique()))
            jogo = st.selectbox("Jogo", sorted(df[(df["Plataforma"] == plataforma) & (df["Console"] == console)]["Jogo"].dropna().unique()))
            idx = df[(df["Plataforma"] == plataforma) & (df["Console"] == console) & (df["Jogo"] == jogo)].index[0]
            with st.form("editar"):
                genero = st.text_input("Gênero", value=str(df.at[idx, "Gênero"]))
                midia = st.selectbox("Mídia", ["", "Física", "Digital", "Outro"],
                                     index=["", "Física", "Digital", "Outro"].index(str(df.at[idx, "Mídia"])) if str(df.at[idx, "Mídia"]) in ["", "Física", "Digital", "Outro"] else 0)
                edicao = st.text_input("Edição", value=str(df.at[idx, "Edição"]))
                condicao = st.text_area("Condição", value=str(df.at[idx, "Condição"]))
                data_lancamento = st.date_input("Data de lançamento", value=data_segura(df.at[idx, "Data de lançamento"]))
                status = st.selectbox("Status", ["", "Jogando", "Zerado", "Parado", "Nunca Joguei"],
                                      index=["", "Jogando", "Zerado", "Parado", "Nunca Joguei"].index(str(df.at[idx, "Status"])) if str(df.at[idx, "Status"]) in ["", "Jogando", "Zerado", "Parado", "Nunca Joguei"] else 0)
                nota = st.slider("Nota", 0, 10, int(df.at[idx, "Nota"]) if pd.notnull(df.at[idx, "Nota"]) else 0)
                tempo = st.number_input("Tempo (h)", min_value=0, value=int(df.at[idx, "Tempo (h)"]) if pd.notnull(df.at[idx, "Tempo (h)"]) else 0)
                inicio = st.date_input("Início", value=data_segura(df.at[idx, "Início"]))
                fim = st.date_input("Fim", value=data_segura(df.at[idx, "Fim"]))
                obs = st.text_area("Observações coleção", value=str(df.at[idx, "Observações coleção"]))
                coment = st.text_area("Comentários pessoais", value=str(df.at[idx, "Comentários pessoais"]))
                editar = st.form_submit_button("Salvar alterações")
            if editar:
                df.at[idx, "Gênero"] = genero
                df.at[idx, "Mídia"] = midia
                df.at[idx, "Edição"] = edicao
                df.at[idx, "Condição"] = condicao
                df.at[idx, "Data de lançamento"] = data_lancamento
                df.at[idx, "Status"] = status
                df.at[idx, "Nota"] = nota
                df.at[idx, "Tempo (h)"] = tempo
                df.at[idx, "Início"] = inicio
                df.at[idx, "Fim"] = fim
                df.at[idx, "Observações coleção"] = obs
                df.at[idx, "Comentários pessoais"] = coment
                df.to_excel(ARQUIVO, index=False)
                st.success("Informações atualizadas!")

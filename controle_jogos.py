import streamlit as st
import pandas as pd
import os
from datetime import date, datetime
from io import BytesIO

ARQUIVO = "Lista de Jogos_ver1.xlsx"
colunas = [
    "Plataforma", "Console", "Gênero", "Jogo", "Mídia", "Edição",
    "Condição", "Status", "Nota", "Tempo (h)", "Início", "Fim",
    "Observações coleção", "Comentários pessoais", "Data de lançamento"
]

if os.path.exists(ARQUIVO):
    try:
        df = pd.read_excel(ARQUIVO)
        for col in colunas:
            if col not in df.columns:
                df[col] = ""
    except Exception as e:
        st.error(f"Erro ao carregar planilha: {e}")
        df = pd.DataFrame(columns=colunas)
else:
    df = pd.DataFrame(columns=colunas)

def parse_data(data):
    if pd.isnull(data) or data == "":
        return date.today()
    try:
        return pd.to_datetime(data, dayfirst=True).date()
    except:
        return date.today()

st.set_page_config(page_title="🎮 Coleção de Jogos", layout="centered")
st.title("🎮 Coleção de Jogos")
st.markdown("---")

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

if pagina == "📋 Lista Completa":
    st.subheader("📋 Lista completa de jogos")
    if df.empty:
        st.info("Nenhum jogo registrado ainda.")
    else:
        df["Data de lançamento"] = pd.to_datetime(df["Data de lançamento"], errors="coerce").dt.date
        df["Data de lançamento"] = df["Data de lançamento"].apply(lambda d: d.strftime("%d/%m/%Y") if pd.notnull(d) else "")
        st.dataframe(df)

if pagina == "📁 Backup e Importação":
    st.subheader("📁 Backup e Importação")
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    st.download_button("📥 Exportar para Excel", buffer.getvalue(), "jogos_backup.xlsx", mime="application/vnd.ms-excel")

    arquivo = st.file_uploader("📤 Importar nova planilha", type=["xlsx"])
    if arquivo:
        try:
            df = pd.read_excel(arquivo)
            for col in colunas:
                if col not in df.columns:
                    df[col] = ""
            df.to_excel(ARQUIVO, index=False)
            st.success("Planilha importada com sucesso!")
        except Exception as e:
            st.error(f"Erro ao importar: {e}")

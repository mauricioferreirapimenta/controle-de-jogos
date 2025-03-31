
import streamlit as st
import pandas as pd
import os

ARQUIVO = "Lista de Jogos_ver1.xlsx"
if os.path.exists(ARQUIVO):
    df = pd.read_excel(ARQUIVO)
else:
    df = pd.DataFrame()

st.set_page_config(page_title="🎮 Minha Coleção de Jogos", layout="wide")
st.title("🎮 Minha Coleção - Visual por Cards")

# Filtros básicos
st.sidebar.header("🔍 Filtros")
plataformas = ["Todas"] + sorted(df["Plataforma"].dropna().unique())
plataforma_sel = st.sidebar.selectbox("Plataforma", plataformas)

console_sel = ""
if plataforma_sel != "Todas":
    consoles = ["Todos"] + sorted(df[df["Plataforma"] == plataforma_sel]["Console"].dropna().unique())
    console_sel = st.sidebar.selectbox("Console", consoles)

# Aplicar filtro
df_filtrado = df.copy()
if plataforma_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Plataforma"] == plataforma_sel]
if console_sel and console_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Console"] == console_sel]

# Visualizar em cards
st.markdown("### 🎲 Jogos encontrados")
if df_filtrado.empty:
    st.info("Nenhum jogo encontrado com os filtros selecionados.")
else:
    for i, row in df_filtrado.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.image("https://via.placeholder.com/100x140?text=Jogo", width=80)
            with col2:
                st.markdown(f"**🎮 {row['Jogo']}**")
                st.markdown(f"- Plataforma: {row['Plataforma']} | Console: {row['Console']}")
                st.markdown(f"- Gênero: {row['Gênero']} | Mídia: {row['Mídia']} | Edição: {row['Edição']}")
                st.markdown(f"- Status: **{row.get('Status', '')}** | Nota: {row.get('Nota', '')}")
                st.markdown(f"📝 *{row.get('Comentários pessoais', '')}*")
            st.markdown("---")

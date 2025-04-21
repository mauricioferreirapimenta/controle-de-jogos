
import streamlit as st
import pandas as pd
import os

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

st.write("Página selecionada:", pagina)

if pagina == "📚 Ver Coleção":
    st.subheader("🎮 Explorar Coleção de Jogos")
    if df.empty:
        st.info("Nenhum jogo adicionado ainda.")
    else:
        plataformas = sorted(df["Plataforma"].dropna().unique())
        plataforma = st.selectbox("Escolha a Plataforma", [""] + plataformas)
        if plataforma:
            total_plataforma = df[df["Plataforma"] == plataforma].shape[0]
            st.markdown(f"**Total de jogos na plataforma _{plataforma}_: {total_plataforma}**")
            consoles = sorted(df[df["Plataforma"] == plataforma]["Console"].dropna().unique())
            console = st.selectbox("Escolha o Console", [""] + consoles)
            if console:
                total_console = df[(df["Plataforma"] == plataforma) & (df["Console"] == console)].shape[0]
                st.markdown(f"**Total de jogos no console _{console}_: {total_console}**")
                jogos = sorted(df[(df["Plataforma"] == plataforma) & (df["Console"] == console)]["Jogo"].dropna().unique())
                jogo = st.selectbox("Escolha o Jogo", [""] + jogos)
                if jogo:
                    info = df[
                        (df["Plataforma"] == plataforma) &
                        (df["Console"] == console) &
                        (df["Jogo"] == jogo)
                    ]
                    st.markdown("### Detalhes do Jogo Selecionado")
                    st.dataframe(info)

# As outras páginas permanecem vazias por enquanto

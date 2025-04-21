
import streamlit as st
import pandas as pd
import os
from datetime import date
from io import BytesIO

st.set_page_config(page_title="🎮 Controle de Jogos", layout="centered")
st.title("🎮 Controle de Coleção e Progresso de Jogos")
st.markdown("---")

# -------------------------------
# Inicialização
# -------------------------------
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

# -------------------------------
# Página: Adicionar Jogo
# -------------------------------
if pagina == "➕ Adicionar Jogo":
    st.subheader("➕ Adicionar novo jogo à coleção")
    with st.form("form_adicionar"):
        plataforma = st.selectbox("Plataforma", list(consoles_por_plataforma.keys()))
        console = st.selectbox("Console", consoles_por_plataforma.get(plataforma, []))
        genero = st.text_input("Gênero")
        jogo = st.text_input("Nome do Jogo")
        midia = st.selectbox("Mídia", ["Físico", "Digital", "Outro"])
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

# -------------------------------
# Página: Editar Jogo
# -------------------------------
elif pagina == "✏️ Editar Jogo":
    st.subheader("✏️ Editar jogo")
    plataforma = st.selectbox("Plataforma", df["Plataforma"].unique())
    consoles = df[df["Plataforma"] == plataforma]["Console"].unique()
    console = st.selectbox("Console", consoles)
    jogos = df[(df["Plataforma"] == plataforma) & (df["Console"] == console)]["Jogo"].unique()
    jogo = st.selectbox("Jogo", jogos)

    idx = df[(df["Plataforma"] == plataforma) & (df["Console"] == console) & (df["Jogo"] == jogo)].index[0]

    with st.form("form_edicao"):
        status = st.selectbox("Status", ["", "Jogando", "Zerado", "Parado", "Nunca Joguei"], index=0)
        nota = st.slider("Nota pessoal", 0, 10, int(df.at[idx, "Nota"] or 0))
        tempo = st.number_input("Tempo jogado (h)", min_value=0, value=int(df.at[idx, "Tempo (h)"] or 0))
        inicio = st.date_input("Data de início", value=date.today())
        fim = st.date_input("Data de fim", value=date.today())
        comentarios = st.text_area("Comentários pessoais")
        editar = st.form_submit_button("Salvar alterações")

    if editar:
        df.at[idx, "Status"] = status
        df.at[idx, "Nota"] = nota
        df.at[idx, "Tempo (h)"] = tempo
        df.at[idx, "Início"] = inicio
        df.at[idx, "Fim"] = fim
        df.at[idx, "Comentários pessoais"] = comentarios
        df.to_excel(ARQUIVO, index=False)
        st.success("Informações atualizadas com sucesso!")

# -------------------------------
# Página: Excluir Jogo
# -------------------------------
elif pagina == "🗑️ Excluir Jogo":
    st.subheader("🗑️ Excluir jogo")
    plataforma = st.selectbox("Plataforma", df["Plataforma"].unique())
    consoles = df[df["Plataforma"] == plataforma]["Console"].unique()
    console = st.selectbox("Console", consoles)
    jogos = df[(df["Plataforma"] == plataforma) & (df["Console"] == console)]["Jogo"].unique()
    jogo = st.selectbox("Jogo", jogos)

    if st.button("Excluir jogo selecionado"):
        df = df[~((df["Plataforma"] == plataforma) & (df["Console"] == console) & (df["Jogo"] == jogo))]
        df.to_excel(ARQUIVO, index=False)
        st.success(f"Jogo '{jogo}' excluído com sucesso!")

# -------------------------------
# Página: Navegar por Plataforma
# -------------------------------
elif pagina == "📁 Navegar por Plataforma":
    st.subheader("📁 Minha Coleção por Plataforma e Console")
    plataformas = df["Plataforma"].value_counts()
    for plat in plataformas.index:
        with st.expander(f"{plat} ({plataformas[plat]})"):
            subset = df[df["Plataforma"] == plat]
            consoles = subset["Console"].value_counts()
            for con in consoles.index:
                st.markdown(f"**🎮 {con}** ({consoles[con]})")
                st.dataframe(subset[subset["Console"] == con][["Jogo", "Gênero", "Status", "Nota"]])

# -------------------------------
# Página: Lista Completa
# -------------------------------
elif pagina == "📋 Lista Completa":
    st.subheader("📋 Lista completa de jogos")
    df_ordenado = df.sort_values(by=["Plataforma", "Console", "Jogo"])
    st.dataframe(df_ordenado)

# -------------------------------
# Página: Backup e Importação
# -------------------------------
elif pagina == "📁 Backup e Importação":
    st.subheader("📁 Backup e Importação")
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    st.download_button("📥 Exportar para Excel", buffer.getvalue(), "jogos_backup.xlsx", mime="application/vnd.ms-excel")

    arquivo = st.file_uploader("📤 Importar nova planilha", type=["xlsx"])
    if arquivo:
        df = pd.read_excel(arquivo)
        df.to_excel(ARQUIVO, index=False)
        st.success("Planilha importada com sucesso!")


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

# ---------------- ADICIONAR JOGO ----------------
if pagina == "➕ Adicionar Jogo":
    st.subheader("➕ Adicionar novo jogo")
    plataforma = st.selectbox("Plataforma", [""] + list(consoles_por_plataforma.keys()))
    if plataforma:
        with st.form("form_adicionar"):
            console = st.selectbox("Console", [""] + consoles_por_plataforma.get(plataforma, []))
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

# ---------------- VER COLEÇÃO ----------------
elif pagina == "📚 Ver Coleção":
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

# ---------------- EDITAR JOGO ----------------
elif pagina == "✏️ Editar Jogo":
    st.subheader("✏️ Editar jogo")
    if df.empty:
        st.warning("Nenhum jogo cadastrado para editar.")
    else:
        plataforma = st.selectbox("Plataforma", [""] + sorted(df["Plataforma"].dropna().unique()))
        if plataforma:
            consoles = df[df["Plataforma"] == plataforma]["Console"].dropna().unique()
            console = st.selectbox("Console", [""] + sorted(consoles))
            if console:
                jogos = df[(df["Plataforma"] == plataforma) & (df["Console"] == console)]["Jogo"].dropna().unique()
                jogo = st.selectbox("Jogo", [""] + sorted(jogos))
                if jogo:
                    idx = df[(df["Plataforma"] == plataforma) & (df["Console"] == console) & (df["Jogo"] == jogo)].index[0]
                    with st.form("form_edicao"):
                        midia = st.selectbox("Mídia", ["", "Físico", "Digital", "Outro"], index=["", "Físico", "Digital", "Outro"].index(df.at[idx, "Mídia"]) if pd.notnull(df.at[idx, "Mídia"]) and df.at[idx, "Mídia"] in ["Físico", "Digital", "Outro"] else 0)
                        edicao = st.text_input("Edição", value=df.at[idx, "Edição"] if pd.notnull(df.at[idx, "Edição"]) else "")
                        condicao = st.text_area("Condição", value=df.at[idx, "Condição"] if pd.notnull(df.at[idx, "Condição"]) else "")
                        obs_colecao = st.text_area("Observações coleção", value=df.at[idx, "Observações coleção"] if pd.notnull(df.at[idx, "Observações coleção"]) else "")
                        status = st.selectbox("Status", ["", "Jogando", "Zerado", "Parado", "Nunca Joguei"])
                        nota = st.slider("Nota pessoal", 0, 10, int(df.at[idx, "Nota"]) if pd.notnull(df.at[idx, "Nota"]) else 0)
                        tempo = st.number_input("Tempo jogado (h)", min_value=0, value=int(df.at[idx, "Tempo (h)"]) if pd.notnull(df.at[idx, "Tempo (h)"]) else 0)
                        inicio = st.date_input("Data de início", value=pd.to_datetime(df.at[idx, "Início"]) if pd.notnull(df.at[idx, "Início"]) else date.today())
                        fim = st.date_input("Data de fim", value=pd.to_datetime(df.at[idx, "Fim"]) if pd.notnull(df.at[idx, "Fim"]) else date.today())
                        comentarios = st.text_area("Comentários pessoais", value=df.at[idx, "Comentários pessoais"] if pd.notnull(df.at[idx, "Comentários pessoais"]) else "")
                        editar = st.form_submit_button("Salvar alterações")
                    if editar:
                        df.at[idx, "Mídia"] = midia
                        df.at[idx, "Edição"] = edicao
                        df.at[idx, "Condição"] = condicao
                        df.at[idx, "Observações coleção"] = obs_colecao
                        df.at[idx, "Status"] = status
                        df.at[idx, "Nota"] = nota
                        df.at[idx, "Tempo (h)"] = tempo
                        df.at[idx, "Início"] = inicio
                        df.at[idx, "Fim"] = fim
                        df.at[idx, "Comentários pessoais"] = comentarios
                        df.to_excel(ARQUIVO, index=False)
                        st.success("Informações atualizadas com sucesso!")

# ---------------- EXCLUIR JOGO ----------------
elif pagina == "🗑️ Excluir Jogo":
    st.subheader("🗑️ Excluir jogo")
    if df.empty:
        st.warning("Nenhum jogo cadastrado para excluir.")
    else:
        plataforma = st.selectbox("Plataforma", [""] + sorted(df["Plataforma"].dropna().unique()))
        if plataforma:
            consoles = df[df["Plataforma"] == plataforma]["Console"].dropna().unique()
            console = st.selectbox("Console", [""] + sorted(consoles))
            if console:
                jogos = df[(df["Plataforma"] == plataforma) & (df["Console"] == console)]["Jogo"].dropna().unique()
                jogo = st.selectbox("Jogo", [""] + sorted(jogos))
                if jogo and st.button("Excluir jogo selecionado"):
                    df = df[~((df["Plataforma"] == plataforma) & (df["Console"] == console) & (df["Jogo"] == jogo))]
                    df.to_excel(ARQUIVO, index=False)
                    st.success(f"Jogo '{jogo}' excluído com sucesso!")

# ---------------- BACKUP E IMPORTAÇÃO ----------------
elif pagina == "📁 Backup e Importação":
    st.subheader("📁 Backup e Importação")
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    st.download_button("📥 Exportar para Excel", buffer.getvalue(), "jogos_backup.xlsx", mime="application/vnd.ms-excel")

    arquivo = st.file_uploader("📤 Importar nova planilha", type=["xlsx"])
    if arquivo:
        try:
            df = pd.read_excel(arquivo)
            df.to_excel(ARQUIVO, index=False)
            st.success("Planilha importada com sucesso!")
        except Exception as e:
            st.error(f"Erro ao importar: {e}")

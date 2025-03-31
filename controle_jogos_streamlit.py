
import streamlit as st
import pandas as pd
import os
from datetime import date

# -------------------------------
# 🔐 Login opcional
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

# -------------------------------
# 📁 Carregar/Salvar dados
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

st.set_page_config(page_title="🎮 Controle de Jogos", layout="centered")
st.title("🎮 Controle de Coleção e Progresso de Jogos")
st.markdown("---")

# -------------------------------
# 🔓 Exibição pública (leitura)
# -------------------------------
if not st.session_state["autenticado"]:
    st.info("🔒 Acesso limitado - apenas visualização")
    df_exibicao = df[colunas].sort_values(by=["Plataforma", "Console", "Jogo"])
    st.dataframe(df_exibicao, use_container_width=True)
    autenticar()
    st.stop()

# -------------------------------
# 🗃️ Adicionar novo jogo
# -------------------------------
st.subheader("➕ Adicionar novo jogo à coleção")

plataforma = st.selectbox("Plataforma", [""] + list(consoles_por_plataforma.keys()))
if plataforma:
    console_opcoes = [""] + consoles_por_plataforma.get(plataforma, [])
    console = st.selectbox("Console", console_opcoes)
else:
    console = st.text_input("Console (digite manualmente)")

with st.form("adicionar_jogo"):
    col1, col2 = st.columns(2)
    generos_opcoes = [""] + ["Ação", "Aventura", "RPG", "Corrida", "Esporte", "Puzzle", "Terror", "Simulação", "Outro"]
    midia_opcoes = [""] + ["Físico", "Digital", "Cartucho", "CD/DVD", "Outro"]
    edicao_opcoes = [""] + ["Standard", "Deluxe", "Colecionador", "Outro"]

    with col1:
        genero = st.selectbox("Gênero", generos_opcoes)
        midia = st.selectbox("Mídia", midia_opcoes)
        condicao = st.text_input("Condição / Observações de coleção")

    with col2:
        edicao = st.selectbox("Edição", edicao_opcoes)
        jogo = st.text_input("Nome do Jogo")
        obs_colecao = st.text_area("Observações gerais da mídia")

    enviar = st.form_submit_button("Adicionar à coleção")
    if enviar and jogo:
        novo = pd.DataFrame([{
            "Plataforma": plataforma,
            "Console": console,
            "Gênero": genero,
            "Jogo": jogo,
            "Mídia": midia,
            "Edição": edicao,
            "Condição": condicao,
            "Status": "",
            "Nota": "",
            "Tempo (h)": "",
            "Início": "",
            "Fim": "",
            "Observações coleção": obs_colecao,
            "Comentários pessoais": ""
        }])
        df = pd.concat([df, novo], ignore_index=True)
        df.to_excel(ARQUIVO, index=False)
        st.success(f"✅ '{jogo}' adicionado à coleção!")

st.markdown("---")

# -------------------------------
# 🛠️ Editar informações de gameplay
# -------------------------------
st.subheader("✏️ Editar jogo")
if not df.empty:
    plataforma_edit = st.selectbox("Plataforma", [""] + sorted(df["Plataforma"].dropna().unique()), key="edit_plat")
    if plataforma_edit:
        console_edit = st.selectbox("Console", [""] + sorted(df[df["Plataforma"] == plataforma_edit]["Console"].dropna().unique()), key="edit_console")
    else:
        console_edit = None

    if console_edit:
        jogos_edit = df[(df["Plataforma"] == plataforma_edit) & (df["Console"] == console_edit)]["Jogo"].unique()
        jogo_sel = st.selectbox("Jogo", [""] + list(jogos_edit), key="edit_jogo")
        if jogo_sel:
            jogo_selecionado = df[(df["Plataforma"] == plataforma_edit) & (df["Console"] == console_edit) & (df["Jogo"] == jogo_sel)].index[0]

            with st.form("form_edicao_jogo"):
                status_opcoes = [""] + ["Jogando", "Zerado", "Parado", "Nunca Joguei"]
                status = st.selectbox("📍 Status", status_opcoes)
                nota = st.slider("⭐ Nota pessoal", 0, 10, 0)
                tempo = st.number_input("⏱️ Tempo jogado (horas)", min_value=0)
                inicio = st.date_input("📅 Data de início", value=date.today())
                fim = st.date_input("📅 Data de término", value=date.today())
                comentarios = st.text_area("📝 Comentários pessoais sobre o jogo")

                salvar_edicao = st.form_submit_button("Salvar edição")
                if salvar_edicao:
                    df.at[jogo_selecionado, "Status"] = status
                    df.at[jogo_selecionado, "Nota"] = nota
                    df.at[jogo_selecionado, "Tempo (h)"] = tempo
                    df.at[jogo_selecionado, "Início"] = inicio
                    df.at[jogo_selecionado, "Fim"] = fim
                    df.at[jogo_selecionado, "Comentários pessoais"] = comentarios
                    df.to_excel(ARQUIVO, index=False)
                    st.success("✅ Jogo atualizado com sucesso!")

    with st.form("form_edicao_jogo"):
        status_opcoes = [""] + ["Jogando", "Zerado", "Parado", "Nunca Joguei"]
        status = st.selectbox("📍 Status", status_opcoes)
        nota = st.slider("⭐ Nota pessoal", 0, 10, 0)
        tempo = st.number_input("⏱️ Tempo jogado (horas)", min_value=0)
        inicio = st.date_input("📅 Data de início", value=date.today())
        fim = st.date_input("📅 Data de término", value=date.today())
        comentarios = st.text_area("📝 Comentários pessoais sobre o jogo")

        salvar_edicao = st.form_submit_button("Salvar edição")
        if salvar_edicao:
            df.at[jogo_selecionado, "Status"] = status
            df.at[jogo_selecionado, "Nota"] = nota
            df.at[jogo_selecionado, "Tempo (h)"] = tempo
            df.at[jogo_selecionado, "Início"] = inicio
            df.at[jogo_selecionado, "Fim"] = fim
            df.at[jogo_selecionado, "Comentários pessoais"] = comentarios
            df.to_excel(ARQUIVO, index=False)
            st.success("✅ Jogo atualizado com sucesso!")

st.markdown("---")

# -------------------------------
# 🗑️ Excluir jogo com filtros
# -------------------------------
st.subheader("🗑️ Excluir jogo")

plataforma_del = st.selectbox("Plataforma", [""] + sorted(df["Plataforma"].dropna().unique()))
if plataforma_del:
    console_del = st.selectbox("Console", [""] + sorted(df[df["Plataforma"] == plataforma_del]["Console"].dropna().unique()))
else:
    console_del = None

if console_del:
    jogos_filtrados = df[(df["Plataforma"] == plataforma_del) & (df["Console"] == console_del)]
    jogo_del = st.selectbox("Jogo", [""] + list(jogos_filtrados["Jogo"].unique()))
    if st.button("Excluir jogo selecionado"):
        df = df.drop(jogos_filtrados[jogos_filtrados["Jogo"] == jogo_del].index).reset_index(drop=True)
        df.to_excel(ARQUIVO, index=False)
        st.success(f"🗑️ '{jogo_del}' excluído com sucesso!")

st.markdown("---")

# -------------------------------
# 📤 Exportar / 📥 Importar
# -------------------------------
st.subheader("📁 Backup e Importação")

col1, col2 = st.columns(2)

with col1:
    st.download_button("⬇️ Exportar para CSV", data=df.to_csv(index=False).encode(), file_name="jogos_backup.csv", mime="text/csv")

with col2:
    uploaded = st.file_uploader("📥 Importar planilha (.xlsx)", type=["xlsx"])
    if uploaded:
        df_import = pd.read_excel(uploaded)
        df = df_import
        df.to_excel(ARQUIVO, index=False)
        st.success("📂 Planilha importada com sucesso!")

# -------------------------------
# 📋 Lista final
# -------------------------------
st.markdown("---")
st.subheader("📋 Lista completa de jogos")
if not df.empty:
    df_exibicao = df[colunas].sort_values(by=["Plataforma", "Console", "Jogo"])
    st.dataframe(df_exibicao, use_container_width=True)

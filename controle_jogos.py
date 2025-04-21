
import streamlit as st
import pandas as pd
import os
from datetime import date
from io import BytesIO

st.set_page_config(page_title="🎮 Controle de Jogos", layout="centered")
st.title("🎮 Controle de Coleção e Progresso de Jogos")
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
    "➕ Adicionar Jogo",
    "✏️ Editar Jogo",
    "🗑️ Excluir Jogo",
    "📁 Navegar por Plataforma",
    "📋 Lista Completa",
    "📁 Backup e Importação"
]
pagina = st.sidebar.radio("Ir para", paginas)
st.sidebar.markdown("---")

st.write("Página selecionada:", pagina)

if pagina == "➕ Adicionar Jogo":
    st.subheader("➕ Adicionar novo jogo à coleção")
    with st.form("form_adicionar"):
        plataforma = st.selectbox("Plataforma", [""] + list(consoles_por_plataforma.keys()))
        console = st.selectbox("Console", [""] + consoles_por_plataforma.get(plataforma, []))
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

elif pagina == "✏️ Editar Jogo":
    st.subheader("✏️ Editar jogo")
    if df.empty:
        st.warning("Nenhum jogo cadastrado para editar.")
    else:
        try:
            plataforma = st.selectbox("Plataforma", [""] + sorted(df["Plataforma"].dropna().unique().tolist()))
            if plataforma:
                consoles = df[df["Plataforma"] == plataforma]["Console"].dropna().unique()
                console = st.selectbox("Console", [""] + sorted(consoles.tolist()))
                if console:
                    jogos = df[(df["Plataforma"] == plataforma) & (df["Console"] == console)]["Jogo"].dropna().unique()
                    jogo = st.selectbox("Jogo", [""] + sorted(jogos.tolist()))
                    if jogo:
                        idx = df[(df["Plataforma"] == plataforma) & (df["Console"] == console) & (df["Jogo"] == jogo)].index[0]

                        with st.form("form_edicao"):
                            status = st.selectbox("Status", ["", "Jogando", "Zerado", "Parado", "Nunca Joguei"])
                            nota_valor = df.at[idx, "Nota"]
                            nota = st.slider("Nota pessoal", 0, 10, int(nota_valor) if pd.notnull(nota_valor) else 0)
                            tempo_valor = df.at[idx, "Tempo (h)"]
                            tempo = st.number_input("Tempo jogado (h)", min_value=0, value=int(tempo_valor) if pd.notnull(tempo_valor) else 0)
                            inicio = st.date_input("Data de início", value=pd.to_datetime(df.at[idx, "Início"]) if pd.notnull(df.at[idx, "Início"]) else date.today())
                            fim = st.date_input("Data de fim", value=pd.to_datetime(df.at[idx, "Fim"]) if pd.notnull(df.at[idx, "Fim"]) else date.today())
                            comentarios = st.text_area("Comentários pessoais", value=df.at[idx, "Comentários pessoais"] if pd.notnull(df.at[idx, "Comentários pessoais"]) else "")
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
        except Exception as e:
            st.error(f"Erro ao editar jogo: {e}")

elif pagina == "🗑️ Excluir Jogo":
    st.subheader("🗑️ Excluir jogo")
    if df.empty:
        st.warning("Nenhum jogo cadastrado para excluir.")
    else:
        try:
            plataforma = st.selectbox("Plataforma", [""] + sorted(df["Plataforma"].dropna().unique().tolist()))
            if plataforma:
                consoles = df[df["Plataforma"] == plataforma]["Console"].dropna().unique()
                console = st.selectbox("Console", [""] + sorted(consoles.tolist()))
                if console:
                    jogos = df[(df["Plataforma"] == plataforma) & (df["Console"] == console)]["Jogo"].dropna().unique()
                    jogo = st.selectbox("Jogo", [""] + sorted(jogos.tolist()))
                    if jogo and st.button("Excluir jogo selecionado"):
                        df = df[~((df["Plataforma"] == plataforma) & (df["Console"] == console) & (df["Jogo"] == jogo))]
                        df.to_excel(ARQUIVO, index=False)
                        st.success(f"Jogo '{jogo}' excluído com sucesso!")
        except Exception as e:
            st.error(f"Erro ao excluir jogo: {e}")

elif pagina == "📁 Navegar por Plataforma":
    st.subheader("📁 Minha Coleção por Plataforma e Console")
    if df.empty:
        st.info("Nenhum jogo adicionado ainda.")
    else:
        plataformas = df["Plataforma"].value_counts()
        for plat in plataformas.index:
            with st.expander(f"{plat} ({plataformas[plat]})"):
                subset = df[df["Plataforma"] == plat]
                consoles = subset["Console"].value_counts()
                for con in consoles.index:
                    st.markdown(f"**🎮 {con}** ({consoles[con]})")
                    st.dataframe(subset[subset["Console"] == con][["Jogo", "Gênero", "Status", "Nota"]])

elif pagina == "📋 Lista Completa":
    st.subheader("📋 Lista completa de jogos")
    if df.empty:
        st.info("Nenhum jogo registrado ainda.")
    else:
        df_ordenado = df.sort_values(by=["Plataforma", "Console", "Jogo"])
        st.dataframe(df_ordenado)

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

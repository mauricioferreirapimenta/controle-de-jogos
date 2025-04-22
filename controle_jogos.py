# Recriação do código completo com todas as seções e correções aplicadas

full_code_path = Path("/mnt/data/controle_jogos_completo_corrigido_final.py")

with open(full_code_path, "w", encoding="utf-8") as f:
    f.write("""
import streamlit as st
import pandas as pd
import os
from datetime import date, datetime
from io import BytesIO

st.set_page_config(page_title="🎮 Coleção de Jogos", layout="centered")
st.title("🎮 Coleção de Jogos")
st.markdown("---")

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
    if isinstance(data, pd.Timestamp):
        return data.date()
    if isinstance(data, str):
        try:
            return pd.to_datetime(data).date()
        except:
            return date.today()
    return data

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

if pagina == "📚 Ver Coleção":
    st.subheader("🎮 Explorar Coleção de Jogos")
    if df.empty:
        st.info("Nenhum jogo adicionado ainda.")
    else:
        plataformas = sorted(df["Plataforma"].dropna().unique())
        plataforma = st.selectbox("Escolha a Plataforma", [""] + plataformas)
        if plataforma:
            total_plat = df[df["Plataforma"] == plataforma].shape[0]
            st.markdown(f"**Total de jogos na plataforma _{plataforma}_: {total_plat}**")
            subset = df[df["Plataforma"] == plataforma]
            consoles = sorted(subset["Console"].dropna().unique())
            console = st.selectbox("Escolha o Console", [""] + consoles)
            if console:
                total_console = subset[subset["Console"] == console].shape[0]
                st.markdown(f"**Total de jogos no console _{console}_: {total_console}**")
                jogos = sorted(subset[subset["Console"] == console]["Jogo"].dropna().unique())
                jogo = st.selectbox("Escolha o Jogo", [""] + jogos)
                if jogo:
                    st.markdown("### Detalhes do Jogo Selecionado")
                    st.dataframe(subset[(subset["Console"] == console) & (subset["Jogo"] == jogo)])

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
            data_lancamento = st.date_input("Data de lançamento", value=date.today())
            enviar = st.form_submit_button("Adicionar à coleção")
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
            st.success(f"Jogo '{jogo}' adicionado com sucesso!")

if pagina == "✏️ Editar Jogo":
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
                        genero = st.text_input("Gênero", value=str(df.at[idx, "Gênero"]) if pd.notnull(df.at[idx, "Gênero"]) else "")
                        midia = st.selectbox("Mídia", ["", "Físico", "Digital", "Outro"],
                            index=["", "Físico", "Digital", "Outro"].index(str(df.at[idx, "Mídia"])) if str(df.at[idx, "Mídia"]) in ["", "Físico", "Digital", "Outro"] else 0)
                        edicao = st.text_input("Edição", value=str(df.at[idx, "Edição"]) if pd.notnull(df.at[idx, "Edição"]) else "")
                        condicao = st.text_area("Condição", value=str(df.at[idx, "Condição"]) if pd.notnull(df.at[idx, "Condição"]) else "")
                        obs_colecao = st.text_area("Observações coleção", value=str(df.at[idx, "Observações coleção"]) if pd.notnull(df.at[idx, "Observações coleção"]) else "")
                        data_lancamento = st.date_input("Data de lançamento", value=parse_data(df.at[idx, "Data de lançamento"]))
                        status = st.selectbox("Status", ["", "Jogando", "Zerado", "Parado", "Nunca Joguei"],
                            index=["", "Jogando", "Zerado", "Parado", "Nunca Joguei"].index(str(df.at[idx, "Status"])) if str(df.at[idx, "Status"]) in ["", "Jogando", "Zerado", "Parado", "Nunca Joguei"] else 0)
                        nota = st.slider("Nota pessoal", 0, 10, int(df.at[idx, "Nota"]) if pd.notnull(df.at[idx, "Nota"]) else 0)
                        tempo = st.number_input("Tempo jogado (h)", min_value=0, value=int(df.at[idx, "Tempo (h)"]) if pd.notnull(df.at[idx, "Tempo (h)"]) else 0)
                        inicio = st.date_input("Data de início", value=parse_data(df.at[idx, "Início"]))
                        fim = st.date_input("Data de fim", value=parse_data(df.at[idx, "Fim"]))
                        comentarios = st.text_area("Comentários pessoais", value=str(df.at[idx, "Comentários pessoais"]) if pd.notnull(df.at[idx, "Comentários pessoais"]) else "")
                        editar = st.form_submit_button("Salvar alterações")
                    if editar:
                        df.at[idx, "Gênero"] = genero
                        df.at[idx, "Mídia"] = midia
                        df.at[idx, "Edição"] = edicao
                        df.at[idx, "Condição"] = condicao
                        df.at[idx, "Observações coleção"] = obs_colecao
                        df.at[idx, "Data de lançamento"] = data_lancamento
                        df.at[idx, "Status"] = status
                        df.at[idx, "Nota"] = nota
                        df.at[idx, "Tempo (h)"] = tempo
                        df.at[idx, "Início"] = inicio
                        df.at[idx, "Fim"] = fim
                        df.at[idx, "Comentários pessoais"] = comentarios
                        df.to_excel(ARQUIVO, index=False)
                        st.success("Informações atualizadas com sucesso!")

if pagina == "🗑️ Excluir Jogo":
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

if pagina == "📋 Lista Completa":
    st.subheader("📋 Lista completa de jogos")
    if df.empty:
        st.info("Nenhum jogo registrado ainda.")
    else:
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
""")

full_code_path.name

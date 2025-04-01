
import streamlit as st
import pandas as pd
import os
from datetime import date
from io import BytesIO

# O restante do código será preenchido (placeholder inicial apenas)
st.title("🎮 Controle de Jogos")
st.write("Este é um placeholder para o código completo.")

# Exemplo da correção no botão de exportação
df = pd.DataFrame({
    "Plataforma": ["Playstation"],
    "Console": ["PS5"],
    "Jogo": ["Spider-Man 2"]
})

buffer = BytesIO()
df.to_excel(buffer, index=False, engine='openpyxl')
buffer.seek(0)

st.download_button("⬇️ Exportar para Excel", buffer, file_name="backup_colecao_jogos.xlsx")

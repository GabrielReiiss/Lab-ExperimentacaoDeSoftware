import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from dashboard.pages import comparador, dados, exploratorio

st.set_page_config(page_title="Lab01: Repositórios Populares", layout="wide")

pagina = st.navigation([
    st.Page(exploratorio.render, title="Dashboard Exploratório", url_path="exploratorio"),
    st.Page(comparador.render, title="Comparador Individual", url_path="comparador"),
    st.Page(dados.render, title="Dados", url_path="dados"),
])
pagina.run()

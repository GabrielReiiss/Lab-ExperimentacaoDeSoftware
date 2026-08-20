import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from dashboard.data import CSV_PATH, PAGE_SIZE, TOTAL_REPOSITORIOS, load_repositories
from dashboard.pages import comparador, dados, exploratorio, snapshots
from scripts.fetch_repositories import fetch_top_repositories
from src.export.csv_writer import write_csv

st.set_page_config(page_title="Lab01: Repositórios Populares", layout="wide")

if not CSV_PATH.exists():
    st.title("Lab01: Repositórios Populares")
    st.warning(
        "Nenhum dataset encontrado em data/raw/repositories.csv. "
        "Colete os dados antes de acessar o dashboard."
    )
    if st.button("Coletar 1000 repositórios agora"):
        with st.spinner("Coletando dados do GitHub, isso pode levar alguns minutos..."):
            rows = fetch_top_repositories(TOTAL_REPOSITORIOS, PAGE_SIZE)
            write_csv(rows, CSV_PATH)
            load_repositories.clear()
        st.success("Dados coletados.")
        st.rerun()
    st.stop()

pagina = st.navigation([
    st.Page(exploratorio.render, title="Dashboard Exploratório", url_path="exploratorio"),
    st.Page(comparador.render, title="Comparador Individual", url_path="comparador"),
    st.Page(dados.render, title="Dados", url_path="dados"),
    st.Page(snapshots.render, title="Snapshots de Sprint", url_path="snapshots"),
])
pagina.run()

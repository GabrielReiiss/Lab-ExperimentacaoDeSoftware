from datetime import datetime

import streamlit as st

from dashboard.data import CSV_PATH, PAGE_SIZE, TOTAL_REPOSITORIOS, load_repositories
from scripts.fetch_repositories import fetch_top_repositories
from src.export.csv_writer import write_csv


def render():
    st.title("Dados")

    if CSV_PATH.exists():
        modificado = datetime.fromtimestamp(CSV_PATH.stat().st_mtime)
        df = load_repositories()
        st.write(f"Última coleta: {modificado:%d/%m/%Y %H:%M}")
        st.write(f"{len(df)} repositórios no dataset atual")
    else:
        st.warning("Nenhum dataset encontrado em data/raw/repositories.csv")

    if st.button("Reminerar dados (1000 repositórios)"):
        with st.spinner("Coletando dados do GitHub, isso pode levar alguns minutos..."):
            rows = fetch_top_repositories(TOTAL_REPOSITORIOS, PAGE_SIZE)
            write_csv(rows, CSV_PATH)
            load_repositories.clear()
        st.success("Dados atualizados.")
        st.rerun()

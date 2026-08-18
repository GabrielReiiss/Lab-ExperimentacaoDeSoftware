import streamlit as st

from dashboard.data import load_repositories


def render():
    st.title("Comparador Individual")
    df = load_repositories()
    nomes = df["owner"] + "/" + df["name"]

    col_a, col_b = st.columns(2)
    with col_a:
        repo_a = st.selectbox("Repositório A", nomes, key="comparador_repo_a")
    with col_b:
        repo_b = st.selectbox("Repositório B", nomes, key="comparador_repo_b")

    st.caption("Comparação detalhada em construção")

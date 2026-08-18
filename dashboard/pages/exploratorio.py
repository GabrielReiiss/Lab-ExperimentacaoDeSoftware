import streamlit as st

from dashboard.data import load_repositories
from dashboard.sections import (
    rq01_idade,
    rq02_contribuicao,
    rq03_releases,
    rq04_atualizacao,
    rq05_linguagem,
    rq06_issues,
    rq07_por_linguagem,
)


def render():
    st.title("Dashboard Exploratório")
    df = load_repositories()
    st.caption(f"{len(df)} repositórios carregados de data/raw/repositories.csv")

    rq01_idade.render(df)
    rq02_contribuicao.render(df)
    rq03_releases.render(df)
    rq04_atualizacao.render(df)
    rq05_linguagem.render(df)
    rq06_issues.render(df)
    rq07_por_linguagem.render(df)

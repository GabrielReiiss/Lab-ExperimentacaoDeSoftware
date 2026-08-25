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


def aplicar_filtros(df):
    st.sidebar.header("Filtros")

    linguagens = sorted(df["primary_language"].dropna().unique())
    selecionadas = st.sidebar.multiselect("Linguagem", linguagens)

    estrelas_min, estrelas_max = int(df["stars"].min()), int(df["stars"].max())
    faixa_estrelas = st.sidebar.slider(
        "Estrelas", estrelas_min, estrelas_max, (estrelas_min, estrelas_max)
    )

    idade_min, idade_max = int(df["age_days"].min()), int(df["age_days"].max())
    faixa_idade = st.sidebar.slider(
        "Idade (dias)", idade_min, idade_max, (idade_min, idade_max)
    )

    filtrado = df[
        df["stars"].between(*faixa_estrelas) & df["age_days"].between(*faixa_idade)
    ]
    if selecionadas:
        filtrado = filtrado[filtrado["primary_language"].isin(selecionadas)]

    return filtrado


def render():
    st.title("Dashboard Exploratório")
    df = load_repositories()

    filtrado = aplicar_filtros(df)
    st.caption(f"{len(filtrado)} de {len(df)} repositórios exibidos")

    rq01_idade.render(filtrado)
    rq02_contribuicao.render(filtrado)
    rq03_releases.render(filtrado)
    rq04_atualizacao.render(filtrado)
    rq05_linguagem.render(filtrado)
    rq06_issues.render(filtrado)
    rq07_por_linguagem.render(filtrado)

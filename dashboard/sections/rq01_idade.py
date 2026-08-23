import plotly.express as px
import streamlit as st

from src.analysis.repo_age import repo_age_summary

ACCENT = "#2a78d6"


def render(df):
    st.subheader("RQ01: Idade dos repositórios")

    if df.empty:
        st.info("Nenhum repositório para os filtros selecionados.")
        return

    resumo = repo_age_summary(df)
    col1, col2 = st.columns(2)
    col1.metric("Mediana de idade", f"{resumo['median']:.0f} dias")
    col2.metric("Repositórios sem data de criação", resumo["missing"])

    fig = px.histogram(df, x="age_days", nbins=30, color_discrete_sequence=[ACCENT])
    fig.update_layout(
        xaxis_title="Idade (dias)",
        yaxis_title="Repositórios",
        bargap=0.05,
    )
    st.plotly_chart(fig, width="stretch")

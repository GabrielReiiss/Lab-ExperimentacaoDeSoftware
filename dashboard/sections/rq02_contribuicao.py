import plotly.express as px
import streamlit as st

from src.analysis.external_contribution import external_contribution_summary

ACCENT = "#2a78d6"


def render(df):
    st.subheader("RQ02: Contribuição externa")

    if df.empty:
        st.info("Nenhum repositório para os filtros selecionados.")
        return

    resumo = external_contribution_summary(df)
    col1, col2 = st.columns(2)
    col1.metric("Mediana de PRs mescladas", f"{resumo['median']:.0f}")
    col2.metric("Repositórios sem esse dado", resumo["missing"])


    fig = px.box(
        df, y="merged_pull_requests", points="outliers", log_y=True,
        color_discrete_sequence=[ACCENT],
    )
    fig.update_layout(
        yaxis_title="Pull requests aceitas (escala log)",
        xaxis_title="",
    )
    st.plotly_chart(fig, width="stretch")

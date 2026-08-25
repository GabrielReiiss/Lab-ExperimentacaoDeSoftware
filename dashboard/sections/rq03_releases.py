import plotly.express as px
import streamlit as st

from src.analysis.release_frequency import release_frequency_summary

ACCENT = "#2a78d6"


def render(df):
    st.subheader("RQ03: Frequência de releases")

    if df.empty:
        st.info("Nenhum repositório para os filtros selecionados.")
        return

    resumo = release_frequency_summary(df)
    col1, col2, col3 = st.columns(3)
    col1.metric("Mediana (todos)", f"{resumo['median']:.0f} releases")
    if resumo["median_with_releases"] is not None:
        col2.metric("Mediana (quem lança release)", f"{resumo['median_with_releases']:.0f} releases")
    col3.metric("Sem nenhuma release", resumo["zero_count"])

    fig = px.histogram(df, x="releases", nbins=30, color_discrete_sequence=[ACCENT])
    fig.update_layout(
        xaxis_title="Total de releases",
        yaxis_title="Repositórios",
        bargap=0.05,
    )
    st.plotly_chart(fig, width="stretch")

import plotly.express as px
import streamlit as st

from src.analysis.update_frequency import update_frequency_summary

ACCENT = "#2a78d6"


def render(df):
    st.subheader("RQ04: Frequência de atualização")

    if df.empty:
        st.info("Nenhum repositório para os filtros selecionados.")
        return

    resumo = update_frequency_summary(df)
    col1, col2 = st.columns(2)
    col1.metric("Mediana", f"{resumo['median']:.0f} dias")
    col2.metric("Parados há mais de 1 ano", resumo["stale_count"])

    fig = px.histogram(df, x="update_frequency_days", nbins=30, color_discrete_sequence=[ACCENT])
    fig.update_layout(
        xaxis_title="Dias desde a última atualização",
        yaxis_title="Repositórios",
        bargap=0.05,
    )
    st.plotly_chart(fig, width="stretch")

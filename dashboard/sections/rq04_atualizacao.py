import plotly.express as px
import streamlit as st

ACCENT = "#2a78d6"


def render(df):
    st.subheader("RQ04: Frequência de atualização")

    if df.empty:
        st.info("Nenhum repositório para os filtros selecionados.")
        return

    fig = px.histogram(df, x="update_frequency_days", nbins=30, color_discrete_sequence=[ACCENT])
    fig.update_layout(
        xaxis_title="Dias desde a última atualização",
        yaxis_title="Repositórios",
        bargap=0.05,
    )
    st.plotly_chart(fig, width="stretch")

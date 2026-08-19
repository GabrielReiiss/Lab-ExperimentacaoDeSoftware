import plotly.express as px
import streamlit as st

ACCENT = "#2a78d6"


def render(df):
    st.subheader("RQ01: Idade dos repositórios")

    if df.empty:
        st.info("Nenhum repositório para os filtros selecionados.")
        return

    fig = px.histogram(df, x="age_days", nbins=30, color_discrete_sequence=[ACCENT])
    fig.update_layout(
        xaxis_title="Idade (dias)",
        yaxis_title="Repositórios",
        bargap=0.05,
    )
    st.plotly_chart(fig, width="stretch")

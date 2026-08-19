import plotly.express as px
import streamlit as st

ACCENT = "#2a78d6"


def render(df):
    st.subheader("RQ03: Frequência de releases")

    if df.empty:
        st.info("Nenhum repositório para os filtros selecionados.")
        return

    fig = px.histogram(df, x="releases", nbins=30, color_discrete_sequence=[ACCENT])
    fig.update_layout(
        xaxis_title="Total de releases",
        yaxis_title="Repositórios",
        bargap=0.05,
    )
    st.plotly_chart(fig, width="stretch")

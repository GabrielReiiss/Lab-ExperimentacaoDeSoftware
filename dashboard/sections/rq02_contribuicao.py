import plotly.express as px
import streamlit as st

ACCENT = "#2a78d6"


def render(df):
    st.subheader("RQ02: Contribuição externa")

    if df.empty:
        st.info("Nenhum repositório para os filtros selecionados.")
        return

    fig = px.box(df, y="merged_pull_requests", points="outliers", color_discrete_sequence=[ACCENT])
    fig.update_layout(
        yaxis_title="Pull requests aceitas",
        xaxis_title="",
    )
    st.plotly_chart(fig, width="stretch")

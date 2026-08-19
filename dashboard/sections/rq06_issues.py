import plotly.express as px
import streamlit as st

ACCENT = "#2a78d6"


def render(df):
    st.subheader("RQ06: Percentual de issues fechadas")

    valores = df["closed_issues_ratio"].dropna()

    if valores.empty:
        st.info("Nenhum repositório com issues para os filtros selecionados.")
        return

    fig = px.histogram(x=valores, nbins=20, color_discrete_sequence=[ACCENT])
    fig.update_layout(
        xaxis_title="Issues fechadas / total",
        yaxis_title="Repositórios",
        xaxis_tickformat=".0%",
        bargap=0.05,
    )
    st.plotly_chart(fig, width="stretch")

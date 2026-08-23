import plotly.express as px
import streamlit as st

from src.analysis.closed_issues_ratio import closed_issues_ratio_summary

ACCENT = "#2a78d6"


def render(df):
    st.subheader("RQ06: Percentual de issues fechadas")

    valores = df["closed_issues_ratio"].dropna()

    if valores.empty:
        st.info("Nenhum repositório com issues para os filtros selecionados.")
        return

    resumo = closed_issues_ratio_summary(df)
    col1, col2 = st.columns(2)
    col1.metric("Mediana de issues fechadas", f"{resumo['median']:.0%}")
    col2.metric("Repositórios sem issues", resumo["missing"])

    fig = px.histogram(x=valores, nbins=20, color_discrete_sequence=[ACCENT])
    fig.update_layout(
        xaxis_title="Issues fechadas / total",
        yaxis_title="Repositórios",
        xaxis_tickformat=".0%",
        bargap=0.05,
    )
    st.plotly_chart(fig, width="stretch")

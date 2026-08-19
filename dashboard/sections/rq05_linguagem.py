import pandas as pd
import plotly.express as px
import streamlit as st

ACCENT = "#2a78d6"
TOP_N = 15


def render(df):
    st.subheader("RQ05: Linguagem primária")

    if df.empty:
        st.info("Nenhum repositório para os filtros selecionados.")
        return

    contagem = df["primary_language"].fillna("Sem linguagem").value_counts()

    if len(contagem) > TOP_N:
        top = contagem.iloc[:TOP_N]
        outros = pd.Series({"Outros": contagem.iloc[TOP_N:].sum()})
        contagem = pd.concat([top, outros])

    dados = contagem.reset_index()
    dados.columns = ["linguagem", "repositorios"]

    fig = px.bar(dados, x="linguagem", y="repositorios", color_discrete_sequence=[ACCENT])
    fig.update_layout(
        xaxis_title="Linguagem",
        yaxis_title="Repositórios",
        xaxis={"categoryorder": "total descending"},
    )
    st.plotly_chart(fig, width="stretch")

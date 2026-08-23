import pandas as pd
import plotly.express as px
import streamlit as st

from src.analysis.language_distribution import compare_with_reference, language_distribution
from src.analysis.language_reference import OCTOVERSE_2025_TOP_LANGUAGES

ACCENT = "#2a78d6"
TOP_N = 15


def render(df):
    st.subheader("RQ05: Linguagem primária")

    if df.empty:
        st.info("Nenhum repositório para os filtros selecionados.")
        return

    distribuicao = language_distribution(df)
    top_linguagem = distribuicao[0]
    st.metric(
        f"Linguagem mais comum: {top_linguagem['language']}",
        f"{top_linguagem['share']:.0%} dos repositórios",
    )

    st.caption("Comparação com o ranking do GitHub Octoverse 2025 (ver README.md para a fonte)")
    comparacao = compare_with_reference(distribuicao, OCTOVERSE_2025_TOP_LANGUAGES)
    tabela_comparacao = pd.DataFrame(
        [
            {
                "Linguagem": item["language"],
                "Posição no Octoverse": item["reference_rank"],
                "Posição na amostra": item["collected_rank"] or "fora do top",
                "% da amostra": f"{item['collected_share']:.1%}",
            }
            for item in comparacao
        ]
    )
    st.dataframe(tabela_comparacao, width="stretch", hide_index=True)

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

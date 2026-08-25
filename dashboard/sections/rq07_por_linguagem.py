import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from src.analysis.language_breakdown import language_breakdown, popular_vs_other_comparison
from src.analysis.language_reference import OCTOVERSE_2025_TOP_LANGUAGES

ACCENT = "#2a78d6"


def render(df):
    st.subheader("RQ07: Contribuição, releases e atualização por linguagem")

    if df.empty:
        st.info("Nenhum repositório para os filtros selecionados.")
        return

    st.caption(f"Linguagens populares (Octoverse 2025): {', '.join(OCTOVERSE_2025_TOP_LANGUAGES)}")

    comparacao = popular_vs_other_comparison(df, OCTOVERSE_2025_TOP_LANGUAGES)
    popular, outras = comparacao["popular"], comparacao["outras"]

    if popular["count"] and outras["count"]:
        col1, col2, col3 = st.columns(3)
        col1.metric(
            "PRs mescladas (mediana)",
            f"{popular['merged_pull_requests_median']:.0f}",
            delta=f"{popular['merged_pull_requests_median'] - outras['merged_pull_requests_median']:.0f} vs. outras",
        )
        col2.metric(
            "Releases (mediana)",
            f"{popular['releases_median']:.0f}",
            delta=f"{popular['releases_median'] - outras['releases_median']:.0f} vs. outras",
        )
        col3.metric(
            "Dias desde att. (mediana)",
            f"{popular['update_frequency_days_median']:.0f}",
            delta=f"{outras['update_frequency_days_median'] - popular['update_frequency_days_median']:.0f} vs. outras",
        )

    breakdown = language_breakdown(df, top_n=10)
    tabela = pd.DataFrame([
        {
            "Linguagem": item["language"],
            "Repositórios": item["count"],
            "PRs mescladas (mediana)": item["merged_pull_requests_median"],
            "Releases (mediana)": item["releases_median"],
            "Dias desde att. (mediana)": item["update_frequency_days_median"],
        }
        for item in breakdown
    ])
    st.dataframe(tabela, width="stretch", hide_index=True)

    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=(
            "RQ02: PRs mescladas",
            "RQ03: Releases",
            "RQ04: Dias desde atualização",
        ),
    )
    fig.add_trace(
        go.Bar(x=tabela["Linguagem"], y=tabela["PRs mescladas (mediana)"], marker_color=ACCENT),
        row=1, col=1,
    )
    fig.add_trace(
        go.Bar(x=tabela["Linguagem"], y=tabela["Releases (mediana)"], marker_color=ACCENT),
        row=1, col=2,
    )
    fig.add_trace(
        go.Bar(x=tabela["Linguagem"], y=tabela["Dias desde att. (mediana)"], marker_color=ACCENT),
        row=1, col=3,
    )
    fig.update_layout(showlegend=False, height=400)
    fig.update_yaxes(title_text="Mediana", row=1, col=1)
    st.plotly_chart(fig, width="stretch")

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from dashboard.data import load_repositories
from src.analysis.correlation import (
    METRIC_LABELS,
    REQUIRED_PAIRS,
    build_normalized_metrics,
    correlation_matrices,
    interpret,
    pairs_above_threshold,
)

ACCENT = "#2a78d6"
TREND_COLOR = "#d62a2a"
THRESHOLD = 0.3

# O que significa "pender" para cada lado (positivo/negativo) em cada par de
# métricas. update_frequency_days entra invertida no cálculo (valor
# normalizado alto = atualização mais recente), então as frases já
# descrevem "recência", não "dias parado".
PAIR_MEANINGS = {
    frozenset({"age_days", "merged_pull_requests"}): (
        "repositórios mais antigos tendem a acumular mais PRs aceitas.",
        "repositórios mais antigos tendem a receber menos PRs aceitas que os mais novos.",
    ),
    frozenset({"age_days", "releases"}): (
        "repositórios mais antigos tendem a ter lançado mais releases.",
        "repositórios mais antigos tendem a ter lançado menos releases que os mais novos.",
    ),
    frozenset({"age_days", "update_frequency_days"}): (
        "repositórios mais antigos tendem a ser atualizados mais recentemente.",
        "repositórios mais antigos tendem a ficar mais tempo sem atualização.",
    ),
    frozenset({"age_days", "closed_issues_ratio"}): (
        "repositórios mais antigos tendem a fechar uma fração maior das issues.",
        "repositórios mais antigos tendem a fechar uma fração menor das issues.",
    ),
    frozenset({"age_days", "popular_language"}): (
        "repositórios mais antigos tendem a estar em linguagens hoje populares.",
        "repositórios mais antigos tendem a estar em linguagens que perderam popularidade.",
    ),
    frozenset({"merged_pull_requests", "releases"}): (
        "mais PRs aceitas acompanham mais releases lançadas.",
        "mais PRs aceitas acompanham menos releases lançadas.",
    ),
    frozenset({"merged_pull_requests", "update_frequency_days"}): (
        "mais PRs aceitas acompanham atualização mais recente.",
        "mais PRs aceitas acompanham atualização menos recente.",
    ),
    frozenset({"merged_pull_requests", "closed_issues_ratio"}): (
        "mais PRs aceitas acompanham uma fração maior de issues fechadas.",
        "mais PRs aceitas acompanham uma fração menor de issues fechadas.",
    ),
    frozenset({"merged_pull_requests", "popular_language"}): (
        "projetos em linguagens populares recebem mais PRs aceitas.",
        "projetos em linguagens populares recebem menos PRs aceitas.",
    ),
    frozenset({"releases", "update_frequency_days"}): (
        "mais releases acompanham atualização mais recente.",
        "mais releases acompanham atualização menos recente.",
    ),
    frozenset({"releases", "closed_issues_ratio"}): (
        "mais releases acompanham uma fração maior de issues fechadas.",
        "mais releases acompanham uma fração menor de issues fechadas.",
    ),
    frozenset({"releases", "popular_language"}): (
        "projetos em linguagens populares lançam mais releases.",
        "projetos em linguagens populares lançam menos releases.",
    ),
    frozenset({"update_frequency_days", "closed_issues_ratio"}): (
        "atualização mais recente acompanha uma fração maior de issues fechadas.",
        "atualização mais recente acompanha uma fração menor de issues fechadas "
        "(projetos mais parados fecham proporcionalmente mais issues).",
    ),
    frozenset({"update_frequency_days", "popular_language"}): (
        "projetos em linguagens populares tendem a ser atualizados mais recentemente.",
        "projetos em linguagens populares tendem a ser atualizados menos recentemente.",
    ),
    frozenset({"closed_issues_ratio", "popular_language"}): (
        "projetos em linguagens populares fecham uma fração maior de issues.",
        "projetos em linguagens populares fecham uma fração menor de issues.",
    ),
}

def _pair_meaning(metric_a: str, metric_b: str) -> tuple[str, str]:
    return PAIR_MEANINGS.get(
        frozenset({metric_a, metric_b}),
        (
            f"{METRIC_LABELS[metric_a]} alto acompanha {METRIC_LABELS[metric_b]} alto.",
            f"{METRIC_LABELS[metric_a]} alto acompanha {METRIC_LABELS[metric_b]} baixo.",
        ),
    )

def _heatmap(matriz, titulo):
    labels = [METRIC_LABELS[coluna] for coluna in matriz.columns]
    fig = px.imshow(
        matriz.to_numpy(),
        x=labels,
        y=labels,
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
        text_auto=".2f",
        aspect="auto",
    )
    fig.update_layout(title=titulo, height=450)
    return fig

def _scatter_com_tendencia(normalized, metric_a, metric_b):
    dados = normalized[[metric_a, metric_b]].dropna()
    x = dados[metric_a].to_numpy()
    y = dados[metric_b].to_numpy()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x, y=y, mode="markers",
            marker=dict(color=ACCENT, opacity=0.4, size=6),
            name="Repositórios",
        )
    )
    if len(x) > 1 and np.std(x) > 0:
        coeficientes = np.polyfit(x, y, 1)
        tendencia = np.poly1d(coeficientes)
        x_linha = np.linspace(x.min(), x.max(), 100)
        fig.add_trace(
            go.Scatter(
                x=x_linha, y=tendencia(x_linha), mode="lines",
                line=dict(color=TREND_COLOR, width=2),
                name="Linha de tendência",
            )
        )

    fig.update_layout(
        xaxis_title=METRIC_LABELS[metric_a],
        yaxis_title=METRIC_LABELS[metric_b],
        height=400,
        showlegend=False,
    )
    return fig

def render():
    st.title("Análise de Correlação entre Métricas")
    st.caption(
        "Correlação (Pearson e Spearman) entre as 6 métricas normalizadas por min-max, "
        "as mesmas usadas no índice de saúde/maturidade."
    )

    df = load_repositories()
    normalized = build_normalized_metrics(df)
    pearson, spearman = correlation_matrices(normalized)

    metodo = st.radio("Método", ["Pearson", "Spearman"], horizontal=True)
    if metodo == "Pearson":
        st.caption(
            "Mede relação **linear**: o quanto os pontos se aproximam de uma reta. "
            "Usa os valores normalizados diretamente, então é sensível a outliers."
        )
    else:
        st.caption(
            "Mede relação **monotônica**: se quando uma métrica sobe a outra tende a subir "
            "(ou descer) junto, mesmo sem ser proporcional/linear. Usa o ranking dos valores "
            "em vez dos valores em si, então é mais robusto a outliers e distribuições tortas."
        )
    matriz = pearson if metodo == "Pearson" else spearman
    st.plotly_chart(_heatmap(matriz, f"Matriz de correlação ({metodo})"), width="stretch")

    st.subheader("Pares")
    for metric_a, metric_b in REQUIRED_PAIRS:
        r = pearson.loc[metric_a, metric_b]
        rho = spearman.loc[metric_a, metric_b]
        positivo, negativo = _pair_meaning(metric_a, metric_b)
        st.write(f"- {interpret(metric_a, metric_b, r, rho)}")
        with st.expander("O que significa cada lado?"):
            st.write(f"↑ Pendendo para **positivo**: {positivo}")
            st.write(f"↓ Pendendo para **negativo**: {negativo}")

    st.subheader(f"Pares com |r| de Pearson > {THRESHOLD}")
    pares_relevantes = pairs_above_threshold(pearson, THRESHOLD)
    if not pares_relevantes:
        st.info("Nenhum par ultrapassou o limiar.")
        return

    for metric_a, metric_b, r in pares_relevantes:
        rho = spearman.loc[metric_a, metric_b]
        positivo, negativo = _pair_meaning(metric_a, metric_b)
        st.markdown(f"**{METRIC_LABELS[metric_a]} × {METRIC_LABELS[metric_b]}**")
        st.plotly_chart(_scatter_com_tendencia(normalized, metric_a, metric_b), width="stretch")
        st.caption(interpret(metric_a, metric_b, r, rho))
        with st.expander("O que significa cada lado?"):
            st.write(f"↑ Pendendo para **positivo**: {positivo}")
            st.write(f"↓ Pendendo para **negativo**: {negativo}")

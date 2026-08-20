import altair as alt
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from dashboard.data import load_repositories
from dashboard.metrics_percentile import repo_percentiles, with_percentiles

def _format_raw_value(metric: dict) -> str:
    if metric["raw_value"] is None:
        return "sem dado"
    if metric["rq"] == "RQ05":
        return f"{metric['raw_value']:.1%} da base"
    if metric["rq"] == "RQ06":
        return f"{metric['raw_value']:.1%}"
    if isinstance(metric["raw_value"], float) and metric["raw_value"].is_integer():
        return f"{int(metric['raw_value'])} {metric['unit']}"
    return f"{metric['raw_value']} {metric['unit']}"


def render():
    st.title("Comparador Individual")
    st.caption("Compare um repositório da base com os outros 999, métrica a métrica (RQ01-RQ06).")

    df = load_repositories()
    df_percentiles = with_percentiles(df)
    nomes = df["owner"] + "/" + df["name"]

    escolhido = st.selectbox("Repositório", sorted(nomes), key="comparador_repo")
    repo_index = df.index[nomes == escolhido][0]

    linguagem = df.loc[repo_index, "primary_language"]
    st.write(f"**{escolhido}** — linguagem primária: {linguagem if pd.notna(linguagem) else 'não detectada'}")

    metrics = repo_percentiles(df_percentiles, repo_index)

    chart_data = pd.DataFrame(
        [
            {
                "Métrica": f"{m['rq']} · {m['label']}",
                "Percentil": m["percentile"] if m["percentile"] is not None else 0,
                "Valor bruto": _format_raw_value(m),
                "Sem dado": m["percentile"] is None,
            }
            for m in metrics
        ]
    )

    bars = (
        alt.Chart(chart_data)
        .mark_bar()
        .encode(
            x=alt.X("Percentil:Q", scale=alt.Scale(domain=[0, 100]), title="Percentil (0-100)"),
            y=alt.Y("Métrica:N", sort=None, title=None),
            color=alt.condition(
                alt.datum["Sem dado"], alt.value("#d0d0d0"), alt.value("#4C78A8")
            ),
            tooltip=["Métrica", "Percentil", "Valor bruto"],
        )
    )
    labels = bars.mark_text(align="left", dx=4).encode(
        text=alt.condition(
            alt.datum["Sem dado"], alt.value("sem dado"), alt.Text("Percentil:Q", format=".0f")
        )
    )

    st.altair_chart(bars + labels, width="stretch")

    st.caption(
        "Percentil = posição do repositório entre os 1000 para aquela métrica (100 = maior/melhor "
        "posição, 0 = menor). RQ04 é invertida (menos dias desde a última atualização = percentil "
        "mais alto). RQ05 usa a fração da base escrita na mesma linguagem primária, já que a "
        "métrica original não é numérica."
    )

    st.subheader("Perfil do repositório nas 6 métricas")
    st.caption(
        "Mesmos percentis do gráfico de barras acima, num formato que destaca o formato geral "
        "do perfil: quanto mais próximo da borda externa em cada eixo, melhor a posição do "
        "repositório naquela métrica em relação aos outros 999."
    )

    BAR_BLUE = "rgba(76, 120, 168, 0.85)"  # mesmo azul das barras do gráfico acima
    REPO_FILL = "rgba(183, 201, 220, 0.5)"  # tom claro do mesmo azul, translúcido

    radar_categories = chart_data["Métrica"].tolist()
    radar_values = chart_data["Percentil"].tolist()
    # fecha o polígono repetindo o primeiro ponto no fim
    radar_fig = go.Figure(
        data=go.Scatterpolar(
            r=radar_values + radar_values[:1],
            theta=radar_categories + radar_categories[:1],
            fill="toself",
            fillcolor=REPO_FILL,
            line=dict(color="white", width=2),
            marker=dict(color="white", size=5),
            name=escolhido,
            hovertemplate="%{theta}: %{r:.0f}<extra></extra>",
        )
    )
    radar_fig.update_layout(
        polar=dict(
            bgcolor=BAR_BLUE,
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color="white", size=12),
                gridcolor="rgba(255, 255, 255, 0.35)",
                linecolor="rgba(255, 255, 255, 0.6)",
            ),
            angularaxis=dict(gridcolor="rgba(255, 255, 255, 0.35)"),
        ),
        showlegend=False,
        margin=dict(t=20, b=20),
    )
    st.plotly_chart(radar_fig, width="stretch")

    for m in metrics:
        percentil_texto = f"percentil {m['percentile']:.0f}" if m["percentile"] is not None else "sem dado suficiente"
        st.write(f"- **{m['rq']} · {m['label']}**: {_format_raw_value(m)} — {percentil_texto}")

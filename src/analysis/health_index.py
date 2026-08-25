"""
Índice composto de saúde/maturidade do repositório (RQ01-RQ06), combinadas
num score de 0 a 1 por média ponderada de métricas normalizadas por
min-max.

Pesos: idade 20%, PRs aceitas 25% (maior peso, sinal mais direto de
colaboração externa), releases 15%, atualização recente 15%, linguagem
popular 15%, issues fechadas 10% (menor peso, varia muito entre
processos de projeto e é o sinal mais ruidoso).

Métrica ausente no repositório (ex. sem issues ou sem linguagem
detectada) é ignorada e os pesos das demais são renormalizados, em vez
de penalizar como pior valor possível.
"""
import pandas as pd

from src.analysis.language_reference import OCTOVERSE_2025_TOP_LANGUAGES

WEIGHTS = {
    "age_days": 0.20,
    "merged_pull_requests": 0.25,
    "releases": 0.15,
    "update_frequency_days": 0.15,
    "popular_language": 0.15,
    "closed_issues_ratio": 0.10,
}

# RQ04 é dias desde a última atualização: quanto menor, mais saudável,
# por isso é invertida antes do min-max.
INVERTED_METRICS = {"update_frequency_days"}


def _min_max(series: pd.Series) -> pd.Series:
    minimo = series.min()
    maximo = series.max()
    if pd.isna(minimo) or maximo == minimo:
        return pd.Series(float("nan"), index=series.index)
    return (series - minimo) / (maximo - minimo)


def add_health_index(df: pd.DataFrame) -> pd.DataFrame:
    """Devolve uma cópia de `df` com a coluna "health_index" (0 a 1)."""
    df = df.copy()
    popular_language = df["primary_language"].apply(
        lambda lang: None if pd.isna(lang) else float(lang in OCTOVERSE_2025_TOP_LANGUAGES)
    )

    normalizado = pd.DataFrame(index=df.index)
    for coluna in WEIGHTS:
        if coluna == "popular_language":
            normalizado[coluna] = popular_language
            continue
        valores = df[coluna]
        if coluna in INVERTED_METRICS:
            valores = -valores
        normalizado[coluna] = _min_max(valores)

    pesos = pd.Series(WEIGHTS)
    disponiveis = normalizado.notna()
    soma_ponderada = normalizado.fillna(0).mul(pesos, axis=1).sum(axis=1)
    peso_total = disponiveis.mul(pesos, axis=1).sum(axis=1)

    df["health_index"] = soma_ponderada / peso_total
    return df

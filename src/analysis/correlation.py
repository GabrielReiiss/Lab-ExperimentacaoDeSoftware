"""
Análise de correlação (Pearson e Spearman) entre as 6 métricas
normalizadas.
"""
import pandas as pd

from src.analysis.language_reference import OCTOVERSE_2025_TOP_LANGUAGES
from src.analysis.normalization import min_max

METRIC_LABELS = {
    "age_days": "Idade",
    "merged_pull_requests": "PRs aceitas",
    "releases": "Releases",
    "update_frequency_days": "Tempo desde update",
    "closed_issues_ratio": "Razão de issues fechadas",
    "popular_language": "Linguagem popular",
}

# Dias desde a última atualização: quanto menor, mais ativo,
INVERTED_METRICS = {"update_frequency_days"}

REQUIRED_PAIRS = [
    ("age_days", "releases"),
    ("age_days", "closed_issues_ratio"),
    ("merged_pull_requests", "releases"),
    ("update_frequency_days", "closed_issues_ratio"),
]

def build_normalized_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Devolve um DataFrame só com as 6 métricas normalizadas (0-1)."""
    popular_language = df["primary_language"].apply(
        lambda lang: None if pd.isna(lang) else float(lang in OCTOVERSE_2025_TOP_LANGUAGES)
    )

    normalizado = pd.DataFrame(index=df.index)
    for coluna in METRIC_LABELS:
        if coluna == "popular_language":
            normalizado[coluna] = popular_language
            continue
        valores = df[coluna]
        if coluna in INVERTED_METRICS:
            valores = -valores
        normalizado[coluna] = min_max(valores)

    return normalizado


def correlation_matrices(normalized: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Retorna (matriz de Pearson, matriz de Spearman) das métricas normalizadas."""
    pearson = normalized.corr(method="pearson")
    spearman = normalized.corr(method="spearman")
    return pearson, spearman


def pairs_above_threshold(pearson: pd.DataFrame, threshold: float = 0.3) -> list[tuple[str, str, float]]:
    """Lista (métrica_a, métrica_b, r) para pares com |r| > threshold.

    Considera só o triângulo superior da matriz (sem duplicar pares nem
    incluir a diagonal), ordenado por |r| decrescente.
    """
    colunas = list(pearson.columns)
    pares = []
    for i, coluna_a in enumerate(colunas):
        for coluna_b in colunas[i + 1:]:
            r = pearson.loc[coluna_a, coluna_b]
            if pd.notna(r) and abs(r) > threshold:
                pares.append((coluna_a, coluna_b, r))

    pares.sort(key=lambda par: abs(par[2]), reverse=True)
    return pares


def interpret(metric_a: str, metric_b: str, pearson_r: float, spearman_r: float) -> str:
    """Gera a frase de interpretação de um par de métricas."""
    forca = _forca(pearson_r)
    direcao = "positiva" if pearson_r >= 0 else "negativa"
    label_a = METRIC_LABELS.get(metric_a, metric_a)
    label_b = METRIC_LABELS.get(metric_b, metric_b)
    return (
        f"{label_a} e {label_b} apresentam correlação {direcao} {forca} "
        f"(Pearson r={pearson_r:.2f}, Spearman rho={spearman_r:.2f})."
    )


def _forca(r: float) -> str:
    r = abs(r)
    if r > 0.7:
        return "forte"
    if r > 0.5:
        return "moderada"
    return "fraca"

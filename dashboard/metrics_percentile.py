"""
Cálculo de percentis por métrica (RQ01-RQ06), usado pelo comparador
individual (dashboard/pages/comparador.py) para posicionar um
repositório em relação aos outros 999 da base.
"""
import pandas as pd

METRICS = [
    {
        "rq": "RQ01",
        "label": "Idade",
        "column": "age_days",
        "ascending": True,
        "unit": "dias",
    },
    {
        "rq": "RQ02",
        "label": "Contribuição externa",
        "column": "merged_pull_requests",
        "ascending": True,
        "unit": "PRs mescladas",
    },
    {
        "rq": "RQ03",
        "label": "Releases",
        "column": "releases",
        "ascending": True,
        "unit": "releases",
    },
    {
        "rq": "RQ04",
        "label": "Frequência de atualização",
        "column": "update_frequency_days",
        "ascending": False,
        "unit": "dias desde a última atualização",
    },
    {
        "rq": "RQ05",
        "label": "Popularidade da linguagem",
        "column": "_language_share",
        "ascending": True,
        "unit": "fração da base na mesma linguagem",
    },
    {
        "rq": "RQ06",
        "label": "Issues fechadas",
        "column": "closed_issues_ratio",
        "ascending": True,
        "unit": "proporção de issues fechadas",
    },
]


def with_percentiles(df: pd.DataFrame) -> pd.DataFrame:
    """
    Devolve uma cópia de `df` com uma coluna "<coluna>_percentile" por
    métrica de METRICS (0-100), calculada em relação a todo o DataFrame
    recebido.
    """
    df = df.copy()
    df["_language_share"] = df["primary_language"].map(
        df["primary_language"].value_counts(normalize=True)
    )

    for metric in METRICS:
        column = metric["column"]
        df[f"{column}_percentile"] = (
            df[column].rank(pct=True, ascending=metric["ascending"]) * 100
        )

    return df


def repo_percentiles(df_with_percentiles: pd.DataFrame, repo_index) -> list[dict]:
    """
    Extrai, para uma linha (repositório) já processada por
    with_percentiles(), a lista de métricas prontas para exibição: rq,
    label, unidade, valor bruto e percentil (None quando não houver
    dado suficiente para calcular).
    """
    row = df_with_percentiles.loc[repo_index]
    result = []
    for metric in METRICS:
        raw_value = row[metric["column"]]
        percentile = row[f"{metric['column']}_percentile"]
        result.append(
            {
                "rq": metric["rq"],
                "label": metric["label"],
                "unit": metric["unit"],
                "raw_value": None if pd.isna(raw_value) else raw_value,
                "percentile": None if pd.isna(percentile) else round(percentile, 1),
            }
        )
    return result

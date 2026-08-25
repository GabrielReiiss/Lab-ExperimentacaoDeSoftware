"""
Normalização min-max compartilhada entre o índice de saúde/maturidade
(`health_index.py`) e a análise de correlação (`correlation.py`).
"""
import pandas as pd


def min_max(series: pd.Series) -> pd.Series:
    """Normaliza `series` para o intervalo 0-1.

    Colunas constantes (ou totalmente ausentes) não têm como ser
    normalizadas de forma significativa, então viram NaN em vez de 0.
    """
    minimo = series.min()
    maximo = series.max()
    if pd.isna(minimo) or maximo == minimo:
        return pd.Series(float("nan"), index=series.index)
    return (series - minimo) / (maximo - minimo)

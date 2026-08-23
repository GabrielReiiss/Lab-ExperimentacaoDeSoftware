"""
Estatísticas formais da RQ04: mediana de dias desde a última
atualização e contagem de repositórios parados há mais de um ano.
"""

STALE_THRESHOLD_DAYS = 365


def update_frequency_summary(df) -> dict:
    dias = df["update_frequency_days"].dropna()

    return {
        "median": float(dias.median()),
        "mean": float(dias.mean()),
        "count": int(dias.count()),
        "missing": int(df["update_frequency_days"].isna().sum()),
        "same_day_count": int((dias == 0).sum()),
        "stale_count": int((dias > STALE_THRESHOLD_DAYS).sum()),
    }

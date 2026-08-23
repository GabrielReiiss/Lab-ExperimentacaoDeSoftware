def repo_age_summary(df) -> dict:
    valores = df["age_days"].dropna()

    return {
        "median": float(valores.median()),
        "mean": float(valores.mean()),
        "count": int(valores.count()),
        "missing": int(df["age_days"].isna().sum()),
    }

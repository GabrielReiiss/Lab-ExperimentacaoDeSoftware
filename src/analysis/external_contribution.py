def external_contribution_summary(df) -> dict:
    valores = df["merged_pull_requests"].dropna()

    return {
        "median": float(valores.median()),
        "mean": float(valores.mean()),
        "count": int(valores.count()),
        "missing": int(df["merged_pull_requests"].isna().sum()),
    }

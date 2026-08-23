def closed_issues_ratio_summary(df) -> dict:
    valores = df["closed_issues_ratio"].dropna()

    return {
        "median": float(valores.median()),
        "mean": float(valores.mean()),
        "count": int(valores.count()),
        "missing": int(df["closed_issues_ratio"].isna().sum()),
    }

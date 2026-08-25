import pandas as pd


def language_breakdown(df: pd.DataFrame, top_n: int = 10) -> list[dict]:
    linguagens_frequentes = df["primary_language"].value_counts().head(top_n).index

    grupo = df["primary_language"].where(df["primary_language"].isin(linguagens_frequentes), "Outras")
    grupo = grupo.fillna("Sem linguagem")

    linhas = []
    for nome, subset in df.groupby(grupo, observed=True):
        linhas.append({
            "language": nome,
            "count": len(subset),
            "merged_pull_requests_median": float(subset["merged_pull_requests"].median()),
            "releases_median": float(subset["releases"].median()),
            "update_frequency_days_median": float(subset["update_frequency_days"].median()),
        })

    return sorted(linhas, key=lambda linha: linha["count"], reverse=True)


def popular_vs_other_comparison(df: pd.DataFrame, popular_languages: list[str]) -> dict:
    populares = df[df["primary_language"].isin(popular_languages)]
    outras = df[~df["primary_language"].isin(popular_languages)]

    def resumo(subset):
        return {
            "count": len(subset),
            "merged_pull_requests_median": float(subset["merged_pull_requests"].median()) if len(subset) else None,
            "releases_median": float(subset["releases"].median()) if len(subset) else None,
            "update_frequency_days_median": float(subset["update_frequency_days"].median()) if len(subset) else None,
        }

    return {"popular": resumo(populares), "outras": resumo(outras)}

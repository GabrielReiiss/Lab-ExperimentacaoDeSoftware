"""
Estatísticas formais da RQ03: mediana geral e mediana condicionada a
quem tem pelo menos 1 release, documentando o teto de 1000 no campo
`releases` já identificado na validação da Sprint 2.
"""

RELEASES_API_CAP = 1000


def release_frequency_summary(df) -> dict:
    releases = df["releases"].dropna()
    com_releases = releases[releases > 0]

    return {
        "median": float(releases.median()),
        "median_with_releases": float(com_releases.median()) if not com_releases.empty else None,
        "mean": float(releases.mean()),
        "count": int(releases.count()),
        "missing": int(df["releases"].isna().sum()),
        "zero_count": int((releases == 0).sum()),
        "capped_count": int((releases == RELEASES_API_CAP).sum()),
    }

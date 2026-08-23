import pandas as pd

from src.analysis.repo_age import repo_age_summary


def test_repo_age_summary_computes_median_and_mean():
    df = pd.DataFrame({"age_days": [1000, 2000, 3000]})

    resultado = repo_age_summary(df)

    assert resultado["median"] == 2000
    assert resultado["mean"] == 2000
    assert resultado["count"] == 3
    assert resultado["missing"] == 0


def test_repo_age_summary_counts_missing_values():
    df = pd.DataFrame({"age_days": [1000, None, None]})

    resultado = repo_age_summary(df)

    assert resultado["count"] == 1
    assert resultado["missing"] == 2

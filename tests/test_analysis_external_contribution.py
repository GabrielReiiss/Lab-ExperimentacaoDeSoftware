import pandas as pd

from src.analysis.external_contribution import external_contribution_summary


def test_external_contribution_summary_computes_median_and_mean():
    df = pd.DataFrame({"merged_pull_requests": [10, 20, 30]})

    resultado = external_contribution_summary(df)

    assert resultado["median"] == 20
    assert resultado["mean"] == 20
    assert resultado["count"] == 3
    assert resultado["missing"] == 0


def test_external_contribution_summary_counts_missing_values():
    df = pd.DataFrame({"merged_pull_requests": [10, None, None]})

    resultado = external_contribution_summary(df)

    assert resultado["count"] == 1
    assert resultado["missing"] == 2

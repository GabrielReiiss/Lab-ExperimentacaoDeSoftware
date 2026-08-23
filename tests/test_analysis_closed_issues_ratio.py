import pandas as pd

from src.analysis.closed_issues_ratio import closed_issues_ratio_summary


def test_closed_issues_ratio_summary_computes_median_and_mean():
    df = pd.DataFrame({"closed_issues_ratio": [0.5, 0.75, 1.0]})

    resultado = closed_issues_ratio_summary(df)

    assert resultado["median"] == 0.75
    assert resultado["mean"] == 0.75
    assert resultado["count"] == 3
    assert resultado["missing"] == 0


def test_closed_issues_ratio_summary_counts_missing_values():
    df = pd.DataFrame({"closed_issues_ratio": [0.5, None, None]})

    resultado = closed_issues_ratio_summary(df)

    assert resultado["count"] == 1
    assert resultado["missing"] == 2

import pandas as pd

from src.analysis.language_breakdown import language_breakdown, popular_vs_other_comparison


def _df():
    return pd.DataFrame({
        "primary_language": ["Python", "Python", "Go", "Go", "Rust"],
        "merged_pull_requests": [10, 30, 5, 15, 2],
        "releases": [1, 3, 0, 2, 0],
        "update_frequency_days": [1, 3, 10, 20, 100],
    })


def test_language_breakdown_computes_median_per_language():
    resultado = language_breakdown(_df(), top_n=10)

    python = next(item for item in resultado if item["language"] == "Python")
    assert python["count"] == 2
    assert python["merged_pull_requests_median"] == 20.0
    assert python["releases_median"] == 2.0
    assert python["update_frequency_days_median"] == 2.0


def test_language_breakdown_groups_rare_languages_as_outras():
    resultado = language_breakdown(_df(), top_n=2)

    outras = next(item for item in resultado if item["language"] == "Outras")
    assert outras["count"] == 1


def test_popular_vs_other_comparison_splits_correctly():
    resultado = popular_vs_other_comparison(_df(), popular_languages=["Python"])

    assert resultado["popular"]["count"] == 2
    assert resultado["popular"]["merged_pull_requests_median"] == 20.0
    assert resultado["outras"]["count"] == 3


def test_popular_vs_other_comparison_handles_empty_group():
    resultado = popular_vs_other_comparison(_df(), popular_languages=["Elixir"])

    assert resultado["popular"]["count"] == 0
    assert resultado["popular"]["merged_pull_requests_median"] is None

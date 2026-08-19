"""Testes de with_percentiles/repo_percentiles, sem depender do Streamlit."""
import pandas as pd

from dashboard.metrics_percentile import repo_percentiles, with_percentiles

def _sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": ["a", "b", "c", "d"],
            "owner": ["o1", "o2", "o3", "o4"],
            "age_days": [10, 20, 30, 40],
            "merged_pull_requests": [0, 5, 10, 15],
            "releases": [1, 1, 1, 1],
            "update_frequency_days": [100, 50, 10, 0],
            "primary_language": ["Python", "Python", "Go", None],
            "closed_issues_ratio": [0.5, 1.0, None, 0.0],
        }
    )

def test_ascending_metric_gives_highest_percentile_to_max_value():
    df = with_percentiles(_sample_df())
    percentiles = repo_percentiles(df, 3)  # age_days=40, o maior da amostra

    age = next(m for m in percentiles if m["rq"] == "RQ01")
    assert age["percentile"] == 100.0

def test_update_frequency_is_inverted_fewer_days_is_higher_percentile():
    df = with_percentiles(_sample_df())
    # linha 3 tem update_frequency_days=0 (atualizado hoje), deveria ser o melhor percentil
    percentiles = repo_percentiles(df, 3)
    update = next(m for m in percentiles if m["rq"] == "RQ04")
    assert update["percentile"] == 100.0

    # linha 0 tem update_frequency_days=100 (mais tempo parado), deveria ser o pior
    percentiles_0 = repo_percentiles(df, 0)
    update_0 = next(m for m in percentiles_0 if m["rq"] == "RQ04")
    assert update_0["percentile"] == 25.0

def test_missing_language_gives_none_percentile_without_breaking_others():
    df = with_percentiles(_sample_df())
    percentiles = repo_percentiles(df, 3)  # linha sem primary_language

    language = next(m for m in percentiles if m["rq"] == "RQ05")
    assert language["percentile"] is None
    assert language["raw_value"] is None

    # as outras métricas da mesma linha continuam calculadas normalmente
    age = next(m for m in percentiles if m["rq"] == "RQ01")
    assert age["percentile"] is not None

def test_missing_closed_issues_ratio_gives_none_percentile():
    df = with_percentiles(_sample_df())
    percentiles = repo_percentiles(df, 2)  # linha com closed_issues_ratio=None

    issues = next(m for m in percentiles if m["rq"] == "RQ06")
    assert issues["percentile"] is None

def test_language_popularity_ranks_shared_language_higher():
    df = with_percentiles(_sample_df())
    # "Python" aparece em 2 de 4 linhas, "Go" em 1 de 4: Python deve ter percentil maior
    python_repo = repo_percentiles(df, 0)
    go_repo = repo_percentiles(df, 2)

    python_lang = next(m for m in python_repo if m["rq"] == "RQ05")
    go_lang = next(m for m in go_repo if m["rq"] == "RQ05")

    assert python_lang["percentile"] > go_lang["percentile"]

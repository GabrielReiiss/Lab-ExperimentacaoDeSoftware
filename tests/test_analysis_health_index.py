import pandas as pd

from src.analysis.health_index import add_health_index, health_index_summary


def _sample_df():
    return pd.DataFrame(
        {
            "age_days": [100, 100, 100, 100],
            "merged_pull_requests": [0, 100, 0, 0],
            "releases": [5, 5, 5, 5],
            "update_frequency_days": [0, 0, 0, 400],
            "primary_language": ["Python", "Python", "COBOL", "Python"],
            "closed_issues_ratio": [0.5, 0.5, 0.5, 0.5],
        }
    )


def test_add_health_index_creates_column_between_0_and_1():
    resultado = add_health_index(_sample_df())

    assert "health_index" in resultado.columns
    assert resultado["health_index"].between(0, 1).all()


def test_more_merged_pull_requests_increases_score():
    resultado = add_health_index(_sample_df())

    assert resultado.loc[1, "health_index"] > resultado.loc[0, "health_index"]


def test_unpopular_language_lowers_score():
    resultado = add_health_index(_sample_df())

    assert resultado.loc[2, "health_index"] < resultado.loc[0, "health_index"]


def test_stale_update_lowers_score():
    resultado = add_health_index(_sample_df())

    assert resultado.loc[3, "health_index"] < resultado.loc[0, "health_index"]


def test_missing_closed_issues_ratio_does_not_zero_score():
    df = _sample_df()
    df.loc[0, "closed_issues_ratio"] = None

    resultado = add_health_index(df)

    assert resultado.loc[0, "health_index"] > 0


def test_constant_column_does_not_break_normalization():
    resultado = add_health_index(_sample_df())  # releases é constante em todas as linhas

    assert resultado["health_index"].notna().all()


def test_health_index_summary_computes_median_and_mean():
    df = add_health_index(_sample_df())

    resumo = health_index_summary(df)

    assert resumo["count"] == 4
    assert resumo["missing"] == 0
    assert 0 <= resumo["median"] <= 1
    assert 0 <= resumo["mean"] <= 1


def test_health_index_summary_counts_missing_values():
    df = add_health_index(_sample_df())
    df.loc[0, "health_index"] = None

    resumo = health_index_summary(df)

    assert resumo["count"] == 3
    assert resumo["missing"] == 1

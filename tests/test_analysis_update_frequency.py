import pandas as pd

from src.analysis.update_frequency import update_frequency_summary


def test_update_frequency_summary_computes_median_and_mean():
    df = pd.DataFrame({"update_frequency_days": [0, 2, 4, 10]})

    resultado = update_frequency_summary(df)

    assert resultado["median"] == 3
    assert resultado["mean"] == 4
    assert resultado["count"] == 4
    assert resultado["missing"] == 0


def test_update_frequency_summary_counts_missing_values():
    df = pd.DataFrame({"update_frequency_days": [5, None, None]})

    resultado = update_frequency_summary(df)

    assert resultado["count"] == 1
    assert resultado["missing"] == 2


def test_update_frequency_summary_counts_same_day_updates():
    df = pd.DataFrame({"update_frequency_days": [0, 0, 5]})

    resultado = update_frequency_summary(df)

    assert resultado["same_day_count"] == 2


def test_update_frequency_summary_counts_stale_repos():
    df = pd.DataFrame({"update_frequency_days": [1, 400, 1000]})

    resultado = update_frequency_summary(df)

    assert resultado["stale_count"] == 2

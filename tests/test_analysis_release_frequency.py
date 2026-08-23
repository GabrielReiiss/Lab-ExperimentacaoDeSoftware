import pandas as pd

from src.analysis.release_frequency import release_frequency_summary


def test_release_frequency_summary_computes_median_and_mean():
    df = pd.DataFrame({"releases": [0, 10, 20, 30]})

    resultado = release_frequency_summary(df)

    assert resultado["median"] == 15
    assert resultado["mean"] == 15
    assert resultado["count"] == 4
    assert resultado["missing"] == 0


def test_release_frequency_summary_counts_missing_values():
    df = pd.DataFrame({"releases": [10, None, None]})

    resultado = release_frequency_summary(df)

    assert resultado["count"] == 1
    assert resultado["missing"] == 2


def test_release_frequency_summary_computes_median_only_with_releases():
    df = pd.DataFrame({"releases": [0, 0, 10, 30]})

    resultado = release_frequency_summary(df)

    assert resultado["median"] == 5
    assert resultado["median_with_releases"] == 20
    assert resultado["zero_count"] == 2


def test_release_frequency_summary_handles_no_releases_at_all():
    df = pd.DataFrame({"releases": [0, 0]})

    resultado = release_frequency_summary(df)

    assert resultado["median_with_releases"] is None


def test_release_frequency_summary_counts_api_cap():
    df = pd.DataFrame({"releases": [1000, 1000, 5]})

    resultado = release_frequency_summary(df)

    assert resultado["capped_count"] == 2

"""Testes de extract_release_frequency, sem chamar a API."""
from src.metrics.release_frequency import extract_release_frequency


def test_extract_release_frequency_returns_release_count():
    repo = {"releases": {"totalCount": 58}}

    assert extract_release_frequency(repo) == 58


def test_extract_release_frequency_zero_releases():
    repo = {"releases": {"totalCount": 0}}

    assert extract_release_frequency(repo) == 0

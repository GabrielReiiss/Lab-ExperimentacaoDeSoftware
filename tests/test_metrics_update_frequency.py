"""
Testa extract_update_frequency() com datas fixas, sem bater na API de verdade.
"""
from datetime import datetime, timezone

from src.metrics.update_frequency import extract_update_frequency


def test_extract_update_frequency_computes_days_since_last_push():
    repo = {"pushedAt": "2026-08-01T12:00:00Z"}
    now = datetime(2026, 8, 11, 12, 0, 0, tzinfo=timezone.utc)

    assert extract_update_frequency(repo, now=now) == 10


def test_extract_update_frequency_same_day_is_zero():
    repo = {"pushedAt": "2026-08-11T08:00:00Z"}
    now = datetime(2026, 8, 11, 12, 0, 0, tzinfo=timezone.utc)

    assert extract_update_frequency(repo, now=now) == 0

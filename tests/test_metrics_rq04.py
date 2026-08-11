"""
Testa extract_rq04() com datas fixas, sem bater na API de verdade.
"""
from datetime import datetime, timezone

from src.metrics.rq04 import extract_rq04


def test_extract_rq04_computes_days_since_last_push():
    repo = {"pushedAt": "2026-08-01T12:00:00Z"}
    now = datetime(2026, 8, 11, 12, 0, 0, tzinfo=timezone.utc)

    assert extract_rq04(repo, now=now) == 10


def test_extract_rq04_same_day_is_zero():
    repo = {"pushedAt": "2026-08-11T08:00:00Z"}
    now = datetime(2026, 8, 11, 12, 0, 0, tzinfo=timezone.utc)

    assert extract_rq04(repo, now=now) == 0

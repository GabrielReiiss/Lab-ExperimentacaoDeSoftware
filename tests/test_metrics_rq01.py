"""
Testa extract_rq01() com datas fixas, sem bater na API de verdade.
"""
from datetime import datetime, timezone

from src.metrics.rq01 import extract_rq01


def test_extract_rq01_computes_days_since_creation():
    repo = {"createdAt": "2020-08-01T12:00:00Z"}
    now = datetime(2026, 8, 11, 12, 0, 0, tzinfo=timezone.utc)

    assert extract_rq01(repo, now=now) == 2201


def test_extract_rq01_same_day_is_zero():
    repo = {"createdAt": "2026-08-11T08:00:00Z"}
    now = datetime(2026, 8, 11, 12, 0, 0, tzinfo=timezone.utc)

    assert extract_rq01(repo, now=now) == 0

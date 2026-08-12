"""Testes de extract_repo_age, sem chamar a API."""
from datetime import datetime, timezone

from src.metrics.repo_age import extract_repo_age


def test_extract_repo_age_computes_days_since_creation():
    repo = {"createdAt": "2020-08-01T12:00:00Z"}
    now = datetime(2026, 8, 11, 12, 0, 0, tzinfo=timezone.utc)

    assert extract_repo_age(repo, now=now) == 2201


def test_extract_repo_age_same_day_is_zero():
    repo = {"createdAt": "2026-08-11T08:00:00Z"}
    now = datetime(2026, 8, 11, 12, 0, 0, tzinfo=timezone.utc)

    assert extract_repo_age(repo, now=now) == 0

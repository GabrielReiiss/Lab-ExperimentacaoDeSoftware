"""Testes de extract_rq02, sem chamar a API."""
from src.metrics.rq02 import extract_rq02


def test_extract_rq02_returns_merged_pr_count():
    repo = {"pullRequests": {"totalCount": 342}}

    assert extract_rq02(repo) == 342


def test_extract_rq02_zero_merged_prs():
    repo = {"pullRequests": {"totalCount": 0}}

    assert extract_rq02(repo) == 0

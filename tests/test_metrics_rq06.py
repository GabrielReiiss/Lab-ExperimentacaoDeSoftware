"""
Testa extract_rq06() com dados fixos, sem bater na API de verdade.
"""
from src.metrics.rq06 import extract_rq06


def test_extract_rq06_computes_closed_ratio():
    repo = {"closedIssues": {"totalCount": 75}, "totalIssues": {"totalCount": 100}}

    assert extract_rq06(repo) == 0.75


def test_extract_rq06_all_closed_is_one():
    repo = {"closedIssues": {"totalCount": 40}, "totalIssues": {"totalCount": 40}}

    assert extract_rq06(repo) == 1.0


def test_extract_rq06_no_issues_returns_none():
    repo = {"closedIssues": {"totalCount": 0}, "totalIssues": {"totalCount": 0}}

    assert extract_rq06(repo) is None

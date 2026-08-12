"""Testes de extract_closed_issues_ratio, sem chamar a API."""
from src.metrics.closed_issues_ratio import extract_closed_issues_ratio


def test_extract_closed_issues_ratio_computes_closed_ratio():
    repo = {"closedIssues": {"totalCount": 75}, "totalIssues": {"totalCount": 100}}

    assert extract_closed_issues_ratio(repo) == 0.75


def test_extract_closed_issues_ratio_all_closed_is_one():
    repo = {"closedIssues": {"totalCount": 40}, "totalIssues": {"totalCount": 40}}

    assert extract_closed_issues_ratio(repo) == 1.0


def test_extract_closed_issues_ratio_no_issues_returns_none():
    repo = {"closedIssues": {"totalCount": 0}, "totalIssues": {"totalCount": 0}}

    assert extract_closed_issues_ratio(repo) is None

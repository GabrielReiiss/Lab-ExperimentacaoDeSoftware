"""Testes de extract_external_contribution, sem chamar a API."""
from src.metrics.external_contribution import extract_external_contribution


def test_extract_external_contribution_returns_merged_pr_count():
    repo = {"pullRequests": {"totalCount": 342}}

    assert extract_external_contribution(repo) == 342


def test_extract_external_contribution_zero_merged_prs():
    repo = {"pullRequests": {"totalCount": 0}}

    assert extract_external_contribution(repo) == 0

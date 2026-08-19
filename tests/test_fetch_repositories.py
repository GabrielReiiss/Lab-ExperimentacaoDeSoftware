"""
Testa build_row() do script de integração, sem bater na API real,
usando um node de repositório de exemplo com o formato que a query
unificada retorna.
"""
import pytest

from scripts.fetch_repositories import MAX_PAGE_SIZE, build_row, fetch_top_repositories

FAKE_REPO = {
    "name": "example-repo",
    "owner": {"login": "example-owner"},
    "createdAt": "2015-01-01T00:00:00Z",
    "pushedAt": "2024-01-01T00:00:00Z",
    "stargazerCount": 1500,
    "primaryLanguage": {"name": "Python"},
    "pullRequests": {"totalCount": 42},
    "releases": {"totalCount": 7},
    "closedIssues": {"totalCount": 8},
    "totalIssues": {"totalCount": 10},
}

def test_build_row_combines_all_metrics():
    row = build_row(FAKE_REPO)

    assert row["name"] == "example-repo"
    assert row["owner"] == "example-owner"
    assert row["stars"] == 1500
    assert row["age_days"] > 0
    assert row["merged_pull_requests"] == 42
    assert row["releases"] == 7
    assert row["update_frequency_days"] >= 0
    assert row["primary_language"] == "Python"
    assert row["closed_issues_ratio"] == 0.8

def test_build_row_handles_repo_without_issues():
    repo_without_issues = {
        **FAKE_REPO,
        "closedIssues": {"totalCount": 0},
        "totalIssues": {"totalCount": 0},
    }

    row = build_row(repo_without_issues)

    assert row["closed_issues_ratio"] is None

def test_fetch_top_repositories_rejects_page_size_above_api_limit():
    with pytest.raises(ValueError):
        fetch_top_repositories(total=10, page_size=MAX_PAGE_SIZE + 1)

"""
Testa paginate() sem bater na API de verdade, usando mocks.
"""
from src.github_client import pagination


def fake_pages():
    return [
        {
            "search": {
                "pageInfo": {"hasNextPage": True, "endCursor": "cursor-1"},
                "nodes": [{"name": "repo-a"}, {"name": "repo-b"}],
            }
        },
        {
            "search": {
                "pageInfo": {"hasNextPage": False, "endCursor": "cursor-2"},
                "nodes": [{"name": "repo-c"}],
            }
        },
    ]


def test_paginate_stops_when_has_next_page_is_false(monkeypatch):
    pages = iter(fake_pages())
    monkeypatch.setattr(pagination, "run_query", lambda query, variables: next(pages))

    result = list(
        pagination.paginate(
            query="query fake",
            base_variables={},
            get_connection=lambda data: data["search"],
            page_size=2,
        )
    )

    assert result == [
        [{"name": "repo-a"}, {"name": "repo-b"}],
        [{"name": "repo-c"}],
    ]

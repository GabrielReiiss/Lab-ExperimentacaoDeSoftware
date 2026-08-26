"""
Testa paginate() sem bater na API de verdade, usando mocks.
"""
import requests

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

def test_paginate_recovers_from_read_timeout_instead_of_crashing(monkeypatch):
    """
    Reproduz o crash relatado: run_query esgota o retry interno e propaga um
    ReadTimeout (subclasse de Timeout) puro, sem ser um HTTPError. paginate()
    precisa tratar isso como falha transitória, não deixar a exceção escapar.
    """
    monkeypatch.setattr(pagination.time, "sleep", lambda seconds: None)

    calls = {"n": 0}

    def flaky_run_query(query, variables):
        calls["n"] += 1
        if calls["n"] <= 2:
            raise requests.exceptions.ReadTimeout("Read timed out. (read timeout=15)")
        return {
            "search": {
                "pageInfo": {"hasNextPage": False, "endCursor": "cursor-1"},
                "nodes": [{"name": "repo-a"}],
            }
        }

    monkeypatch.setattr(pagination, "run_query", flaky_run_query)

    result = list(
        pagination.paginate(
            query="query fake",
            base_variables={},
            get_connection=lambda data: data["search"],
            page_size=2,
        )
    )

    assert result == [[{"name": "repo-a"}]]
    assert calls["n"] == 3

def test_paginate_shrinks_page_size_on_first_failure_not_third(monkeypatch):
    """
    FAILURE_STREAK_TO_SHRINK=1: encolhe já na 1ª falha, sem esperar
    confirmar 3x no mesmo page_size (ver docs/benchmark_pagination.md
    — confirmar 3x custava ~26% do tempo total sem ganho medido).
    """
    monkeypatch.setattr(pagination.time, "sleep", lambda seconds: None)

    page_sizes_tentados = []

    def flaky_run_query(query, variables):
        page_sizes_tentados.append(variables["first"])
        if len(page_sizes_tentados) == 1:
            error = requests.exceptions.HTTPError("502 Bad Gateway")
            error.response = type("Resp", (), {"status_code": 502})()
            raise error
        return {
            "search": {
                "pageInfo": {"hasNextPage": False, "endCursor": "cursor-1"},
                "nodes": [{"name": "repo-a"}],
            }
        }

    monkeypatch.setattr(pagination, "run_query", flaky_run_query)

    list(
        pagination.paginate(
            query="query fake",
            base_variables={},
            get_connection=lambda data: data["search"],
            page_size=50,
        )
    )

    assert page_sizes_tentados == [50, 45]  # encolheu logo após a única falha, não 3

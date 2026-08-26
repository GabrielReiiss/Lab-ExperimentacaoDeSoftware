"""
Testa o retry de run_query() em erro 502/503/504, sem bater na API real.
Substitui client._session.post (a Session reaproveitada por run_query)
por uma função mocada.
"""
import requests

from src.github_client import client

class FakeResponse:
    def __init__(self, status_code: int, json_data: dict = None, reason: str = "", invalid_json: bool = False):
        self.status_code = status_code
        self.reason = reason
        self._json_data = json_data or {}
        self._invalid_json = invalid_json

    def json(self):
        if self._invalid_json:
            raise requests.exceptions.JSONDecodeError("Expecting value", "", 0)
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"{self.status_code} {self.reason}")

def test_run_query_raises_immediately_on_502_without_retrying(monkeypatch):
    """
    502/503/504 são determinísticos por custo de consulta (ver
    docs/benchmark_pagination.md),run_query NÃO retenta esse caso de
    propósito, porque o diagnóstico mostrou que os dois retries
    empilhados (aqui + em paginate()) multiplicavam o tempo perdido em
    page_sizes ruins sem nenhum ganho. Quem sabe *o que* mudar diante
    desse erro (paginate(), reduzindo o page_size) é quem deve tratar
    o HTTPError e decidir como tentar de novo.
    """
    call_count = {"n": 0}

    def fake_post(*args, **kwargs):
        call_count["n"] += 1
        return FakeResponse(502, reason="Bad Gateway")

    monkeypatch.setattr(client._session, "post", fake_post)

    try:
        client.run_query("{ viewer { login } }")
        assert False, "deveria ter levantado HTTPError"
    except requests.exceptions.HTTPError:
        pass

    assert call_count["n"] == 1 

def test_run_query_does_not_retry_on_graphql_error(monkeypatch):
    call_count = {"n": 0}

    def fake_post(*args, **kwargs):
        call_count["n"] += 1
        return FakeResponse(200, {"errors": [{"message": "Field 'x' doesn't exist"}]})

    monkeypatch.setattr(client._session, "post", fake_post)

    try:
        client.run_query("{ x }")
        assert False, "deveria ter levantado GraphQLError"
    except Exception as e:
        assert type(e).__name__ == "GraphQLError"

    assert call_count["n"] == 1

def test_run_query_retries_on_invalid_json_body_and_succeeds(monkeypatch):
    responses = iter(
        [
            FakeResponse(200, invalid_json=True),
            FakeResponse(200, {"data": {"viewer": {"login": "felipeaps46"}}}),
        ]
    )
    monkeypatch.setattr(client._session, "post", lambda *a, **k: next(responses))
    monkeypatch.setattr(client.time, "sleep", lambda seconds: None)

    data = client.run_query("{ viewer { login } }")

    assert data == {"viewer": {"login": "felipeaps46"}}

def test_run_query_retries_on_chunked_encoding_error_and_succeeds(monkeypatch):
    """
    Reproduz o crash real visto na coleta de N=1000: a conexão é cortada
    no meio do corpo da resposta (ChunkedEncodingError), não coberto
    pelo tuple original de erros de rede retentáveis.
    """
    responses = iter(
        [
            requests.exceptions.ChunkedEncodingError("Connection broken"),
            FakeResponse(200, {"data": {"viewer": {"login": "felipeaps46"}}}),
        ]
    )

    def fake_post(*args, **kwargs):
        next_response = next(responses)
        if isinstance(next_response, Exception):
            raise next_response
        return next_response

    monkeypatch.setattr(client._session, "post", fake_post)
    monkeypatch.setattr(client.time, "sleep", lambda seconds: None)

    data = client.run_query("{ viewer { login } }")

    assert data == {"viewer": {"login": "felipeaps46"}}

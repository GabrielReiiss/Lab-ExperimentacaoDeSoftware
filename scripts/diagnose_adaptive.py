"""
Diagnóstico único (não faz parte do pipeline): mede pra onde vai o tempo
dentro de paginate() em modo adaptativo, quanto é requisição bem-sucedida,
quanto é requisição que falhou, e quanto é sleep de backoff (das DUAS
camadas de retry: run_query e paginate()).

Não altera src/github_client/*.py, instrumenta via monkeypatch dos
próprios time.sleep e requests.Session.post pra cronometrar sem mudar
comportamento.

Uso:
    python -m scripts.diagnose_adaptive --total 100
"""
import argparse
import time

from src.github_client import client, pagination
from src.queries.top_repositories import (
    TOP_REPOSITORIES_QUERY,
    TOP_REPOSITORIES_SEARCH_QUERY,
)

BASE_VARIABLES = {"searchQuery": TOP_REPOSITORIES_SEARCH_QUERY}
GET_CONNECTION = lambda data: data["search"]

stats = {
    "tempo_requisicoes_ok": 0.0,
    "tempo_requisicoes_falhas": 0.0,
    "tempo_sleep_client": 0.0,
    "tempo_sleep_paginate": 0.0,
    "n_requisicoes_ok": 0,
    "n_requisicoes_falhas": 0,
}

_real_post = client._session.post
_real_client_sleep = time.sleep


def timed_post(*args, **kwargs):
    start = time.perf_counter()
    try:
        response = _real_post(*args, **kwargs)
    except Exception:
        stats["tempo_requisicoes_falhas"] += time.perf_counter() - start
        stats["n_requisicoes_falhas"] += 1
        raise
    elapsed = time.perf_counter() - start
    if response.status_code in client.RETRYABLE_STATUS_CODES:
        stats["tempo_requisicoes_falhas"] += elapsed
        stats["n_requisicoes_falhas"] += 1
    else:
        stats["tempo_requisicoes_ok"] += elapsed
        stats["n_requisicoes_ok"] += 1
    return response


def client_sleep(seconds):
    stats["tempo_sleep_client"] += seconds
    _real_client_sleep(0) 


def paginate_sleep(seconds):
    stats["tempo_sleep_paginate"] += seconds
    _real_client_sleep(0)


def main(total: int) -> None:
    client._session.post = timed_post
    client.time.sleep = client_sleep
    pagination.time.sleep = paginate_sleep

    repos = 0
    pages = 0
    wall_start = time.perf_counter()

    for page in pagination.paginate(
        TOP_REPOSITORIES_QUERY, BASE_VARIABLES, GET_CONNECTION, page_size=10
    ):
        pages += 1
        repos += len(page)
        if repos >= total:
            break

    wall_elapsed = time.perf_counter() - wall_start

    print(f"\nColetados: {repos} em {pages} páginas, {wall_elapsed:.1f}s de parede (real).")
    print(f"  tempo em requisições OK:     {stats['tempo_requisicoes_ok']:.1f}s ({stats['n_requisicoes_ok']} reqs)")
    print(f"  tempo em requisições falhas: {stats['tempo_requisicoes_falhas']:.1f}s ({stats['n_requisicoes_falhas']} reqs)")
    print(f"  sleep de backoff (client.py, silencioso):   {stats['tempo_sleep_client']:.1f}s (não esperado de verdade, só contabilizado)")
    print(f"  sleep de backoff (pagination.py, impresso): {stats['tempo_sleep_paginate']:.1f}s (idem)")
    tempo_util = stats["tempo_requisicoes_ok"]
    tempo_overhead = wall_elapsed - tempo_util
    print(f"\n  tempo 'útil' (requisições OK): {tempo_util:.1f}s ({tempo_util/wall_elapsed:.0%} do total)")
    print(f"  tempo 'overhead' (falhas + sleep real, não simulado): {tempo_overhead:.1f}s ({tempo_overhead/wall_elapsed:.0%} do total)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--total", type=int, default=100)
    args = parser.parse_args()

    main(args.total)

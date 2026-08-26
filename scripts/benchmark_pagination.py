"""
Benchmark único (não faz parte do pipeline de coleta): compara a
paginação adaptativa (src/github_client/pagination.paginate) contra uma
paginação de page_size fixo, coletando o mesmo número de repositórios
pela mesma query unificada.

Mede: tempo total, número de páginas/requisições, quantas vezes o
page_size adaptativo cresceu/encolheu, e quantas páginas falharam em
cada estratégia. O resultado impresso aqui foi copiado, com data, para
docs/benchmark_pagination.md, este script pode ser rodado de novo a
qualquer momento pra atualizar aquele registro.

Uso:
    python -m scripts.benchmark_pagination --total 200
"""
import argparse
import io
import time
from contextlib import redirect_stdout

import requests

from src.github_client.client import run_query
from src.github_client.errors import GraphQLError
from src.github_client.pagination import paginate
from src.queries.top_repositories import (
    TOP_REPOSITORIES_QUERY,
    TOP_REPOSITORIES_SEARCH_QUERY,
)

BASE_VARIABLES = {"searchQuery": TOP_REPOSITORIES_SEARCH_QUERY}
GET_CONNECTION = lambda data: data["search"]

RETRYABLE_STATUS_CODES = {502, 503, 504}


def run_adaptive(total: int, start_page_size: int) -> dict:
    """Coleta `total` repositórios com o page_size adaptativo atual."""
    captured = io.StringIO()
    repos = 0
    pages = 0
    start = time.perf_counter()

    with redirect_stdout(captured):
        for page in paginate(
            TOP_REPOSITORIES_QUERY, BASE_VARIABLES, GET_CONNECTION, page_size=start_page_size
        ):
            pages += 1
            repos += len(page)
            if repos >= total:
                break

    elapsed = time.perf_counter() - start
    log = captured.getvalue()

    return {
        "estrategia": f"adaptativo (início={start_page_size})",
        "repos_coletados": repos,
        "paginas": pages,
        "segundos": round(elapsed, 1),
        "crescimentos": log.count("Aumentando page_size"),
        "reducoes": log.count("Reduzindo page_size"),
        "falhas_transitorias": log.count("falha "),
        "abortou": repos < total,
    }


def run_fixed(total: int, page_size: int, max_page_failures: int) -> dict:
    """
    Coleta `total` repositórios com page_size CONSTANTE, sem adaptar.
    Aborta cedo (max_page_failures) se a mesma página falhar
    repetidamente, isso é o comportamento que queremos evidenciar
    para page_size grande, não deixar rodar até estourar o rate limit.
    """
    repos = 0
    pages = 0
    page_failures = 0
    cursor = None
    start = time.perf_counter()
    aborted_reason = None

    while repos < total:
        variables = {**BASE_VARIABLES, "first": page_size, "cursor": cursor}
        try:
            data = run_query(TOP_REPOSITORIES_QUERY, variables)
        except requests.exceptions.HTTPError as error:
            status = error.response.status_code if error.response is not None else None
            if status not in RETRYABLE_STATUS_CODES:
                raise
            page_failures += 1
            if page_failures >= max_page_failures:
                aborted_reason = f"{page_failures}x HTTPError {status} na mesma página, abortando"
                break
            continue
        except GraphQLError:
            raise

        connection = GET_CONNECTION(data)
        pages += 1
        repos += len(connection["nodes"])
        page_info = connection["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        cursor = page_info["endCursor"]

    elapsed = time.perf_counter() - start

    return {
        "estrategia": f"fixo (page_size={page_size})",
        "repos_coletados": repos,
        "paginas": pages,
        "segundos": round(elapsed, 1),
        "falhas_transitorias": page_failures,
        "abortou": aborted_reason,
    }


def print_result(result: dict) -> None:
    print(f"\n== {result['estrategia']} ==")
    for key, value in result.items():
        if key == "estrategia":
            continue
        print(f"  {key}: {value}")


def main(total: int) -> None:
    print(f"Benchmark: coletando {total} repositórios com cada estratégia.\n")

    print_result(run_adaptive(total, start_page_size=10))
    print_result(run_fixed(total, page_size=10, max_page_failures=3))
    print_result(run_fixed(total, page_size=50, max_page_failures=3))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--total", type=int, default=200)
    args = parser.parse_args()

    main(args.total)

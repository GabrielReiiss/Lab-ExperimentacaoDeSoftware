"""
Paginação genérica por cursor, reaproveitável por qualquer query que siga
o padrão de conexão do GitHub GraphQL (pageInfo { hasNextPage endCursor }
+ nodes).

Além de percorrer as páginas, ajusta adaptativamente o page_size: cresce
depois de uma sequência de páginas bem-sucedidas, encolhe depois de uma
sequência de falhas transitórias (timeout/erro de conexão/conexão
cortada no meio do corpo/erro 5xx/corpo de resposta inválido, que já
esgotaram o retry interno de run_query).
Para evitar flapping (crescer, falhar,
encolher, crescer de novo pro mesmo valor que já tinha falhado), o
page_size que causou a última sequência de falhas vira um teto.
"""
import time
from typing import Callable, Iterator

import requests

from src.github_client.client import run_query
from src.github_client.errors import GraphQLError

RETRYABLE_STATUS_CODES = {502, 503, 504}

SUCCESS_STREAK_TO_GROW = 3
FAILURE_STREAK_TO_SHRINK = 1
PAGE_SIZE_STEP = 5
MIN_PAGE_SIZE = 5
MAX_PAGE_SIZE = 100
MAX_CONSECUTIVE_FAILURES = 10
CEILING_FORGIVENESS_ROUNDS = 5
RETRY_BACKOFF_SECONDS = 2


def paginate(
    query: str,
    base_variables: dict,
    get_connection: Callable[[dict], dict],
    page_size: int = 50,
) -> Iterator[list[dict]]:
    """
    Generator que percorre todas as páginas de uma query paginada.

    Args:
        query: query GraphQL que declara $cursor e $first.
        base_variables: variáveis fixas da query.
        get_connection: recebe o `data` retornado por run_query() e
            devolve o objeto de conexão que contém "pageInfo" e "nodes".
        page_size: quantos itens pedir por página (ponto de partida;
            pode crescer ou encolher automaticamente durante a execução).

    Yields:
        A lista de nodes de cada página, uma por vez, até
        `hasNextPage` ser False.
    """
    cursor = None
    successful_pages = 0
    failed_pages = 0
    failure_ceiling = None
    capped_growth_rounds = 0

    while True:
        if successful_pages >= SUCCESS_STREAK_TO_GROW:
            successful_pages = 0
            candidate = min(page_size + PAGE_SIZE_STEP, MAX_PAGE_SIZE)

            if failure_ceiling is not None and candidate >= failure_ceiling:
                capped_growth_rounds += 1
                if capped_growth_rounds >= CEILING_FORGIVENESS_ROUNDS:
                    print(f"\nTeto de {failure_ceiling} parece superado, tentando ultrapassar de novo.")
                    page_size = candidate
                    failure_ceiling = None
                    capped_growth_rounds = 0
                else:
                    page_size = max(failure_ceiling - PAGE_SIZE_STEP, MIN_PAGE_SIZE)
            else:
                page_size = candidate
                capped_growth_rounds = 0
                print(
                    f"\nAumentando page_size para {page_size} após "
                    f"{SUCCESS_STREAK_TO_GROW} páginas bem-sucedidas seguidas."
                )
        elif failed_pages >= FAILURE_STREAK_TO_SHRINK:
            failed_pages = 0
            failure_ceiling = page_size
            capped_growth_rounds = 0
            page_size = max(page_size - PAGE_SIZE_STEP, MIN_PAGE_SIZE)
            print(
                f"\nReduzindo page_size para {page_size} após "
                f"{FAILURE_STREAK_TO_SHRINK} falhas seguidas (teto registrado em {failure_ceiling})."
            )

        variables = {**base_variables, "first": page_size, "cursor": cursor}

        try:
            data = run_query(query, variables)
        except requests.exceptions.HTTPError as error:
            status_code = error.response.status_code if error.response is not None else None
            if status_code not in RETRYABLE_STATUS_CODES:
                raise

            successful_pages = 0
            failed_pages += 1
            print(
                f"\nErro {status_code} na API do GitHub "
                f"(falha {failed_pages}/{FAILURE_STREAK_TO_SHRINK})."
            )
            if failed_pages >= MAX_CONSECUTIVE_FAILURES:
                raise
            time.sleep(RETRY_BACKOFF_SECONDS * failed_pages)
            continue
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.JSONDecodeError,
            requests.exceptions.ChunkedEncodingError,
        ) as error:
            successful_pages = 0
            failed_pages += 1
            print(
                f"\n{type(error).__name__} na requisição à API do GitHub "
                f"(falha {failed_pages}/{FAILURE_STREAK_TO_SHRINK})."
            )
            if failed_pages >= MAX_CONSECUTIVE_FAILURES:
                raise
            time.sleep(RETRY_BACKOFF_SECONDS * failed_pages)
            continue
        except GraphQLError:
            raise

        connection = get_connection(data)

        successful_pages += 1
        failed_pages = 0

        yield connection["nodes"]

        page_info = connection["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        cursor = page_info["endCursor"]

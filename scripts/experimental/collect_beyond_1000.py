"""
EXPERIMENTAL: não faz parte do pipeline de produção (scripts/fetch_repositories.py
continua sendo o script oficial, sem nenhuma dependência disto aqui).

A API de busca do GitHub limita cada consulta a ~1.000 resultados
acessíveis via paginação, não importa a estratégia (ver
docs/benchmark_pagination.md, testamos e confirmamos que o teto é real,
não artefato de código). Pra coletar mais que isso, este script quebra a
busca em várias faixas de `stars:` que não se sobrepõem, cada uma abaixo
do teto, e depois compara a mesma pergunta de sempre (adaptativa vs.
page_size fixo) num volume maior.

Uso:
    python -m scripts.experimental.collect_beyond_1000 --total 2000
    python -m scripts.experimental.collect_beyond_1000 --total 2000 --page-size 10 --safe-max-per-range 900

    # Teste direcionado: começa as faixas a partir de um teto de estrelas
    # em vez do topo do ranking, útil pra testar repositórios "menos
    # complexos" (menos populares) sem gastar tempo cobrindo os mais
    # populares no caminho:
    python -m scripts.experimental.collect_beyond_1000 --total 2000 --max-stars 500
"""
import argparse
import time

import requests

from scripts.fetch_repositories import build_row
from src.github_client import pagination as _pagination_tuning
from src.github_client.client import run_query
from src.github_client.errors import GraphQLError
from src.queries.repository_count import count_repositories
from src.queries.top_repositories import TOP_REPOSITORIES_QUERY

DEFAULT_PAGE_SIZE = 10
SAFE_MAX_PER_RANGE = 900  # folga abaixo do teto real de ~1.000 da API de busca
MAX_STAR_GUESS = 1_000_000  # teto superior pra busca binária (acima do repo mais popular)
MIN_STARS = 2  # mesmo piso usado na coleta oficial (stars:>1)


def range_query(low: int, high: int | None) -> str:
    """Monta o filtro de busca pra uma faixa de estrelas [low, high] (high=None = sem teto)."""
    if high is None:
        return f"stars:>={low}"
    return f"stars:{low}..{high}"


def find_lower_bound(upper: int | None, safe_max: int) -> int:
    """
    Busca binária: menor `low` tal que a faixa [low, upper] tenha no
    máximo `safe_max` repositórios. `count_repositories` é não-crescente
    conforme `low` aumenta (faixa mais estreita = menos repositórios).
    """
    lo, hi = MIN_STARS, upper if upper is not None else MAX_STAR_GUESS

    while lo < hi:
        mid = (lo + hi) // 2
        count = count_repositories(range_query(mid, upper))
        if count <= safe_max:
            hi = mid  
        else:
            lo = mid + 1  

    return lo


def find_star_ranges(
    total_desired: int,
    safe_max_per_range: int = SAFE_MAX_PER_RANGE,
    max_stars: int | None = None,
) -> list[tuple[int, int | None]]:
    """
    Descobre faixas de `stars:` que, somadas, cobrem pelo menos
    `total_desired` repositórios, cada faixa abaixo de `safe_max_per_range`.
    Não faz nenhuma coleta, só conta.
    """
    ranges: list[tuple[int, int | None]] = []
    covered = 0
    upper: int | None = max_stars

    while covered < total_desired:
        low = find_lower_bound(upper, safe_max_per_range)
        count = count_repositories(range_query(low, upper))

        if count > safe_max_per_range:
            raise RuntimeError(
                f"Faixa {range_query(low, upper)} tem {count} repositórios, "
                f"acima do safe_max_per_range={safe_max_per_range}, mesmo no "
                f"piso de estrelas (MIN_STARS={MIN_STARS}). Aumente "
                f"MIN_STARS, reduza --safe-max-per-range, ou aceite parar "
                f"aqui (cobertos até agora: {covered} repositórios)."
            )

        ranges.append((low, upper))
        covered += count
        print(f"  faixa {range_query(low, upper)}: {count} repositórios (acumulado: {covered})")

        if low <= MIN_STARS:
            break  # esgotou o universo de repositórios (stars >= MIN_STARS)
        upper = low - 1

    return ranges


def collect_range_adaptive(low: int, upper: int | None, start_page_size: int) -> tuple[list[dict], int]:
    """
    Versão adaptativa que devolve também o `page_size` final usado nessa
    faixa, pra permitir carregar esse valor pra faixa seguinte em vez de
    reiniciar em `start_page_size` toda vez (ver docs/benchmark_pagination.md
    reiniciar por faixa paga o custo de exploração repetidas vezes).
    """
    P = _pagination_tuning
    search_query = range_query(low, upper)
    page_size = start_page_size
    cursor = None
    successful_pages = 0
    failed_pages = 0
    failure_ceiling = None
    capped_growth_rounds = 0
    rows: list[dict] = []

    while True:
        if successful_pages >= P.SUCCESS_STREAK_TO_GROW:
            successful_pages = 0
            candidate = min(page_size + P.PAGE_SIZE_STEP, P.MAX_PAGE_SIZE)
            if failure_ceiling is not None and candidate >= failure_ceiling:
                capped_growth_rounds += 1
                if capped_growth_rounds >= P.CEILING_FORGIVENESS_ROUNDS:
                    print(f"\nTeto de {failure_ceiling} parece superado, tentando ultrapassar de novo.")
                    page_size = candidate
                    failure_ceiling = None
                    capped_growth_rounds = 0
                else:
                    page_size = max(failure_ceiling - P.PAGE_SIZE_STEP, P.MIN_PAGE_SIZE)
            else:
                page_size = candidate
                capped_growth_rounds = 0
                print(
                    f"\nAumentando page_size para {page_size} após "
                    f"{P.SUCCESS_STREAK_TO_GROW} páginas bem-sucedidas seguidas."
                )
        elif failed_pages >= P.FAILURE_STREAK_TO_SHRINK:
            failed_pages = 0
            failure_ceiling = page_size
            capped_growth_rounds = 0
            page_size = max(page_size - P.PAGE_SIZE_STEP, P.MIN_PAGE_SIZE)
            print(
                f"\nReduzindo page_size para {page_size} após "
                f"{P.FAILURE_STREAK_TO_SHRINK} falhas seguidas (teto registrado em {failure_ceiling})."
            )

        variables = {"searchQuery": search_query, "first": page_size, "cursor": cursor}

        try:
            data = run_query(TOP_REPOSITORIES_QUERY, variables)
        except requests.exceptions.HTTPError as error:
            status_code = error.response.status_code if error.response is not None else None
            if status_code not in P.RETRYABLE_STATUS_CODES:
                raise
            successful_pages = 0
            failed_pages += 1
            print(f"\nErro {status_code} na API do GitHub (falha {failed_pages}/{P.FAILURE_STREAK_TO_SHRINK}).")
            if failed_pages >= P.MAX_CONSECUTIVE_FAILURES:
                raise
            time.sleep(P.RETRY_BACKOFF_SECONDS * failed_pages)
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
                f"(falha {failed_pages}/{P.FAILURE_STREAK_TO_SHRINK})."
            )
            if failed_pages >= P.MAX_CONSECUTIVE_FAILURES:
                raise
            time.sleep(P.RETRY_BACKOFF_SECONDS * failed_pages)
            continue
        except GraphQLError:
            raise

        connection = data["search"]
        successful_pages += 1
        failed_pages = 0
        rows.extend(build_row(repo) for repo in connection["nodes"])

        page_info = connection["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        cursor = page_info["endCursor"]

    return rows, page_size


def collect_range_fixed(low: int, upper: int | None, page_size: int) -> list[dict]:
    search_query = range_query(low, upper)
    rows = []
    cursor = None

    while True:
        variables = {"searchQuery": search_query, "first": page_size, "cursor": cursor}
        data = run_query(TOP_REPOSITORIES_QUERY, variables)
        connection = data["search"]
        rows.extend(build_row(repo) for repo in connection["nodes"])

        page_info = connection["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        cursor = page_info["endCursor"]

    return rows


def collect_across_ranges(ranges: list[tuple[int, int | None]], page_size: int, strategy: str) -> dict:
    start = time.perf_counter()
    rows = []

    if strategy == "adaptive":
        current_page_size = page_size
        for low, upper in ranges:
            partition_rows, current_page_size = collect_range_adaptive(low, upper, current_page_size)
            rows.extend(partition_rows)
    else:
        for low, upper in ranges:
            rows.extend(collect_range_fixed(low, upper, page_size))

    elapsed = time.perf_counter() - start

    return {"estrategia": strategy, "repos_coletados": len(rows), "segundos": round(elapsed, 1)}


def main(total: int, page_size: int, safe_max_per_range: int, max_stars: int | None) -> None:
    teto_msg = f"a partir de stars<={max_stars}" if max_stars is not None else "do topo do ranking"
    print(f"Descobrindo faixas de stars: pra cobrir {total} repositórios, {teto_msg}...")
    discovery_start = time.perf_counter()
    ranges = find_star_ranges(total, safe_max_per_range, max_stars)
    discovery_elapsed = time.perf_counter() - discovery_start
    print(f"Descoberta de faixas: {discovery_elapsed:.1f}s, {len(ranges)} faixa(s) (tempo NÃO contado nas estratégias abaixo).\n")

    print("Coletando com estratégia adaptativa...")
    resultado_adaptativo = collect_across_ranges(ranges, page_size, "adaptive")
    print(f"  {resultado_adaptativo}\n")

    print("Coletando com estratégia fixa...")
    resultado_fixo = collect_across_ranges(ranges, page_size, "fixed")
    print(f"  {resultado_fixo}\n")

    razao = resultado_adaptativo["segundos"] / resultado_fixo["segundos"]
    print(f"Adaptativa/Fixa: {razao:.2f}x")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--total", type=int, default=2000)
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE)
    parser.add_argument("--safe-max-per-range", type=int, default=SAFE_MAX_PER_RANGE)
    parser.add_argument(
        "--max-stars", type=int, default=None,
        help="teto de estrelas por onde começar as faixas (default: sem teto, começa do topo)",
    )
    args = parser.parse_args()

    main(args.total, args.page_size, args.safe_max_per_range, args.max_stars)

"""
Script único de consulta do grupo.

Roda a query unificada (src/queries/top_repositories.py) para os N
repositórios mais populares e aplica as 6 métricas já validadas,
montando uma linha combinada por repositório.

Uso:
    python -m scripts.fetch_repositories
    python -m scripts.fetch_repositories --total 50 --page-size 10
"""
import argparse

from src.github_client.pagination import paginate
from src.metrics.closed_issues_ratio import extract_closed_issues_ratio
from src.metrics.external_contribution import extract_external_contribution
from src.metrics.primary_language import extract_primary_language
from src.metrics.release_frequency import extract_release_frequency
from src.metrics.repo_age import extract_repo_age
from src.metrics.update_frequency import extract_update_frequency
from src.queries.top_repositories import (
    TOP_REPOSITORIES_QUERY,
    TOP_REPOSITORIES_SEARCH_QUERY,
)

DEFAULT_PAGE_SIZE = 10  # repositórios por requisição
MAX_PAGE_SIZE = 100  # limite de "first" imposto pela API do GitHub

def build_row(repo: dict) -> dict:
    """Junta o resultado das 6 métricas num único dict por repositório."""
    return {
        "name": repo["name"],
        "owner": repo["owner"]["login"],
        "age_days": extract_repo_age(repo),
        "merged_pull_requests": extract_external_contribution(repo),
        "releases": extract_release_frequency(repo),
        "update_frequency_days": extract_update_frequency(repo),
        "primary_language": extract_primary_language(repo),
        "closed_issues_ratio": extract_closed_issues_ratio(repo),
    }

def fetch_top_repositories(total: int, page_size: int = DEFAULT_PAGE_SIZE) -> list[dict]:
    if page_size > MAX_PAGE_SIZE:
        raise ValueError(
            f"page_size={page_size} excede o máximo de {MAX_PAGE_SIZE} imposto pela API do GitHub."
        )
    if page_size > DEFAULT_PAGE_SIZE:
        print(
            f"Aviso: page_size={page_size} é maior que o padrão testado "
            f"({DEFAULT_PAGE_SIZE}). Requisições maiores tendem a devolver "
            "502 por custo de consulta, se acontecer reduza o page_size."
        )

    print(f"Buscando {total} repositórios (lotes de {page_size})...")

    rows = []

    for page in paginate(
        TOP_REPOSITORIES_QUERY,
        base_variables={"searchQuery": TOP_REPOSITORIES_SEARCH_QUERY},
        get_connection=lambda data: data["search"],
        page_size=page_size,
    ):
        for repo in page:
            rows.append(build_row(repo))
        print(f"  {len(rows)}/{total} coletados...")
        if len(rows) >= total:
            break

    return rows[:total]

def main(total: int, page_size: int) -> None:
    rows = fetch_top_repositories(total, page_size)

    print()

    header = (
        f"{'Repositório':<45} {'Idade(d)':>9} {'PRs':>6} {'Releases':>9} "
        f"{'Últ. att(d)':>12} {'Linguagem':<12} {'Issues fech.':>13}"
    )
    print(header)
    for row in rows:
        ratio = "—" if row["closed_issues_ratio"] is None else f"{row['closed_issues_ratio']:.0%}"
        nome = f"{row['owner']}/{row['name']}"
        print(
            f"{nome:<45} {row['age_days']:>9} {row['merged_pull_requests']:>6} "
            f"{row['releases']:>9} {row['update_frequency_days']:>12} "
            f"{str(row['primary_language']):<12} {ratio:>13}"
        )

    print(f"\n{len(rows)} repositórios coletados.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--total", type=int, default=100)
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE)
    args = parser.parse_args()

    main(args.total, args.page_size)

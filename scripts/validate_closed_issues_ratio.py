"""
Validação manual da RQ06 (Lab01S01).

Roda a query em uma amostra pequena de repositórios populares, extrai a
métrica e imprime o resultado para conferência visual antes de integrar
ao script único de consulta do grupo.

Uso: python -m scripts.validate_closed_issues_ratio
"""
from src.github_client.client import run_query
from src.metrics.closed_issues_ratio import extract_closed_issues_ratio
from src.queries.closed_issues_ratio import CLOSED_ISSUES_RATIO_QUERY, CLOSED_ISSUES_RATIO_SEARCH_QUERY

SAMPLE_SIZE = 10


def main():
    data = run_query(
        CLOSED_ISSUES_RATIO_QUERY,
        {"searchQuery": CLOSED_ISSUES_RATIO_SEARCH_QUERY, "first": SAMPLE_SIZE, "cursor": None},
    )
    repos = data["search"]["nodes"]

    print(f"{'Repositório':<40} {'Fechadas/Total':<16} {'% Fechadas':>10}")
    for repo in repos:
        razao = extract_closed_issues_ratio(repo)
        nome = f"{repo['owner']['login']}/{repo['name']}"
        fechadas = repo["closedIssues"]["totalCount"]
        total = repo["totalIssues"]["totalCount"]
        pct = f"{razao:.1%}" if razao is not None else "N/A"
        print(f"{nome:<40} {f'{fechadas}/{total}':<16} {pct:>10}")


if __name__ == "__main__":
    main()

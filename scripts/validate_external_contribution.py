"""
Validação manual da RQ02 (Lab01S01).

Roda a query em uma amostra pequena de repositórios populares, extrai a
métrica e imprime o resultado para conferência visual antes de integrar
ao script único de consulta do grupo.

Uso: python -m scripts.validate_external_contribution
"""
from src.github_client.client import run_query
from src.metrics.external_contribution import extract_external_contribution
from src.queries.external_contribution import (
    EXTERNAL_CONTRIBUTION_QUERY,
    EXTERNAL_CONTRIBUTION_SEARCH_QUERY,
)

SAMPLE_SIZE = 10


def main():
    data = run_query(
        EXTERNAL_CONTRIBUTION_QUERY,
        {"searchQuery": EXTERNAL_CONTRIBUTION_SEARCH_QUERY, "first": SAMPLE_SIZE, "cursor": None},
    )
    repos = data["search"]["nodes"]

    print(f"{'Repositório':<40} {'PRs aceitas':>12}")
    for repo in repos:
        prs = extract_external_contribution(repo)
        nome = f"{repo['owner']['login']}/{repo['name']}"
        print(f"{nome:<40} {prs:>12}")


if __name__ == "__main__":
    main()

"""
Validação manual da RQ02 (Lab01S01).

Roda a query em uma amostra pequena de repositórios populares, extrai a
métrica e imprime o resultado para conferência visual antes de integrar
ao script único de consulta do grupo.

Uso: python -m scripts.validate_rq02
"""
from src.github_client.client import run_query
from src.metrics.rq02 import extract_rq02
from src.queries.rq02 import RQ02_QUERY, RQ02_SEARCH_QUERY

SAMPLE_SIZE = 10


def main():
    data = run_query(
        RQ02_QUERY,
        {"searchQuery": RQ02_SEARCH_QUERY, "first": SAMPLE_SIZE, "cursor": None},
    )
    repos = data["search"]["nodes"]

    print(f"{'Repositório':<40} {'PRs aceitas':>12}")
    for repo in repos:
        prs = extract_rq02(repo)
        nome = f"{repo['owner']['login']}/{repo['name']}"
        print(f"{nome:<40} {prs:>12}")


if __name__ == "__main__":
    main()

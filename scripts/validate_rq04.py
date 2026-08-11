"""
Validação manual da RQ04 (Lab01S01).

Roda a query em uma amostra pequena de repositórios populares, extrai a
métrica e imprime o resultado para conferência visual antes de integrar
ao script único de consulta do grupo.

Uso: python -m scripts.validate_rq04
"""
from src.github_client.client import run_query
from src.metrics.rq04 import extract_rq04
from src.queries.rq04 import RQ04_QUERY, RQ04_SEARCH_QUERY

SAMPLE_SIZE = 10


def main():
    data = run_query(
        RQ04_QUERY,
        {"searchQuery": RQ04_SEARCH_QUERY, "first": SAMPLE_SIZE, "cursor": None},
    )
    repos = data["search"]["nodes"]

    print(f"{'Repositório':<40} {'Última atualização':<22} {'Dias desde então':>16}")
    for repo in repos:
        dias = extract_rq04(repo)
        nome = f"{repo['owner']['login']}/{repo['name']}"
        print(f"{nome:<40} {repo['pushedAt']:<22} {dias:>16}")


if __name__ == "__main__":
    main()

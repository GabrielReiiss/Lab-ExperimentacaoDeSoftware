"""
Validação manual da RQ03, Lab01S01.

Roda a query em uma amostra pequena de repositórios populares, extrai a
métrica e imprime o resultado para conferência visual antes de integrar
ao script único de consulta do grupo.

Uso: python -m scripts.validate_release_frequency
"""
from src.github_client.client import run_query
from src.metrics.release_frequency import extract_release_frequency
from src.queries.release_frequency import RELEASE_FREQUENCY_QUERY, RELEASE_FREQUENCY_SEARCH_QUERY

SAMPLE_SIZE = 10


def main():
    data = run_query(
        RELEASE_FREQUENCY_QUERY,
        {"searchQuery": RELEASE_FREQUENCY_SEARCH_QUERY, "first": SAMPLE_SIZE, "cursor": None},
    )
    repos = data["search"]["nodes"]

    print(f"{'Repositório':<40} {'Releases':>10}")
    for repo in repos:
        releases = extract_release_frequency(repo)
        nome = f"{repo['owner']['login']}/{repo['name']}"
        print(f"{nome:<40} {releases:>10}")


if __name__ == "__main__":
    main()

"""
Validação manual da RQ04 (Lab01S01).

Roda a query em uma amostra pequena de repositórios populares, extrai a
métrica e imprime o resultado para conferência visual antes de integrar
ao script único de consulta do grupo.

Uso: python -m scripts.validate_update_frequency
"""
from src.github_client.client import run_query
from src.metrics.update_frequency import extract_update_frequency
from src.queries.update_frequency import UPDATE_FREQUENCY_QUERY, UPDATE_FREQUENCY_SEARCH_QUERY

SAMPLE_SIZE = 10


def main():
    data = run_query(
        UPDATE_FREQUENCY_QUERY,
        {"searchQuery": UPDATE_FREQUENCY_SEARCH_QUERY, "first": SAMPLE_SIZE, "cursor": None},
    )
    repos = data["search"]["nodes"]

    print(f"{'Repositório':<40} {'Última atualização':<22} {'Dias desde então':>16}")
    for repo in repos:
        dias = extract_update_frequency(repo)
        nome = f"{repo['owner']['login']}/{repo['name']}"
        print(f"{nome:<40} {repo['pushedAt']:<22} {dias:>16}")


if __name__ == "__main__":
    main()

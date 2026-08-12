"""
Validação manual da RQ01 (Lab01S01).

Roda a query em uma amostra pequena de repositórios populares, extrai a
métrica e imprime o resultado para conferência visual antes de integrar
ao script único de consulta do grupo.

Uso: python -m scripts.validate_repo_age
"""
from src.github_client.client import run_query
from src.metrics.repo_age import extract_repo_age
from src.queries.repo_age import REPO_AGE_QUERY, REPO_AGE_SEARCH_QUERY

SAMPLE_SIZE = 10


def main():
    data = run_query(
        REPO_AGE_QUERY,
        {"searchQuery": REPO_AGE_SEARCH_QUERY, "first": SAMPLE_SIZE, "cursor": None},
    )
    repos = data["search"]["nodes"]

    print(f"{'Repositório':<40} {'Criado em':<22} {'Idade (dias)':>14}")
    for repo in repos:
        dias = extract_repo_age(repo)
        nome = f"{repo['owner']['login']}/{repo['name']}"
        print(f"{nome:<40} {repo['createdAt']:<22} {dias:>14}")


if __name__ == "__main__":
    main()

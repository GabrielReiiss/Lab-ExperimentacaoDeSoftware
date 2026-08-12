"""
Validação manual da RQ05 (Lab01S01).

Roda a query em uma amostra pequena de repositórios populares, extrai a
métrica e imprime o resultado para conferência visual antes de integrar
ao script único de consulta do grupo.

Uso: python -m scripts.validate_primary_language
"""
from src.github_client.client import run_query
from src.metrics.primary_language import extract_primary_language
from src.queries.primary_language import PRIMARY_LANGUAGE_QUERY, PRIMARY_LANGUAGE_SEARCH_QUERY

SAMPLE_SIZE = 10


def main():
    data = run_query(
        PRIMARY_LANGUAGE_QUERY,
        {"searchQuery": PRIMARY_LANGUAGE_SEARCH_QUERY, "first": SAMPLE_SIZE, "cursor": None},
    )
    repos = data["search"]["nodes"]

    print(f"{'Repositório':<40} {'Linguagem primária':<22}")
    for repo in repos:
        linguagem = extract_primary_language(repo) or "N/A"
        nome = f"{repo['owner']['login']}/{repo['name']}"
        print(f"{nome:<40} {linguagem:<22}")

if __name__ == "__main__":
    main()
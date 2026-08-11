"""
Validação manual da RQ05 (Lab01S01).

Roda a query em uma amostra pequena de repositórios populares, extrai a
métrica e imprime o resultado para conferência visual antes de integrar
ao script único de consulta do grupo.

Uso: python -m scripts.validate_rq05
"""
from src.github_client import run_query
from src.metrics.rq05 import extract_rq05
from src.queries.rq05 import RQ05_QUERY, RQ05_SEARCH_QUERY

SAMPLE_SIZE = 10

def main():
    data = run_query(
        RQ05_QUERY,
        {"searchQuery": RQ05_SEARCH_QUERY, "first": SAMPLE_SIZE, "cursor": None},
    )
    repos = data["search"]["nodes"]

    print(f"{'Repositório':<40} {'Linguagem primária':<22}")
    for repo in repos:
        linguagem = extract_rq05(repo) or "N/A"
        nome = f"{repo['owner']['login']}/{repo['name']}"
        print(f"{nome:<40} {linguagem:<22}")
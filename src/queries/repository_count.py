"""
Query leve, sem paginação.
"""
from src.github_client.client import run_query

REPOSITORY_COUNT_QUERY = """
query($searchQuery: String!) {
  search(query: $searchQuery, type: REPOSITORY) {
    repositoryCount
  }
}
"""


def count_repositories(search_query: str) -> int:
    """Quantos repositórios existem pra esse filtro de busca (sem paginar)."""
    data = run_query(REPOSITORY_COUNT_QUERY, {"searchQuery": search_query})
    return data["search"]["repositoryCount"]

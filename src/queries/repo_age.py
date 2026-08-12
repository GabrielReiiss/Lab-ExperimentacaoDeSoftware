"""
Query da RQ01. Traz o campo createdAt de cada repositório, usado para
calcular a idade.
"""

REPO_AGE_QUERY = """
query($searchQuery: String!, $first: Int!, $cursor: String) {
  search(query: $searchQuery, type: REPOSITORY, first: $first, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes {
      ... on Repository {
        name
        owner { login }
        createdAt
      }
    }
  }
}
"""

REPO_AGE_SEARCH_QUERY = "stars:>1 sort:stars-desc"

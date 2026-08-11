"""
Query GraphQL da RQ05 (linguagem primária do repositório).

Busca repositórios ordenados por estrelas e traz, para cada um, o campo `primaryLanguage`.
"""

RQ05_QUERY = """
query($searchQuery: String!, $first: Int!, $cursor: String) {
  search(query: $searchQuery, type: REPOSITORY, first: $first, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes {
      ... on Repository {
        name
        owner { login }
        primaryLanguage { name }
      }
    }
  }
}
"""

RQ05_SEARCH_QUERY = "stars:>1 sort:stars-desc"
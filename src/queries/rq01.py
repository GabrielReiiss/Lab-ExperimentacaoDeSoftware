"""
Query GraphQL da RQ01 (idade do repositório).

Busca repositórios ordenados por estrelas e traz, para cada um, o campo
`createdAt`: data de criação do repositório — é essa data que a métrica
usa para calcular a idade/maturidade.
"""

RQ01_QUERY = """
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

RQ01_SEARCH_QUERY = "stars:>1 sort:stars-desc"

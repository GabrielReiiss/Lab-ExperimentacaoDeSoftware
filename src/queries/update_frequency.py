"""
Query GraphQL da RQ04 (tempo até a última atualização).

Busca repositórios ordenados por estrelas e traz, para cada um, o campo
`pushedAt`: data do último push (commit) no repositório, é essa data que
a métrica usa como "última atualização".
"""

UPDATE_FREQUENCY_QUERY = """
query($searchQuery: String!, $first: Int!, $cursor: String) {
  search(query: $searchQuery, type: REPOSITORY, first: $first, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes {
      ... on Repository {
        name
        owner { login }
        pushedAt
      }
    }
  }
}
"""

UPDATE_FREQUENCY_SEARCH_QUERY = "stars:>1 sort:stars-desc"

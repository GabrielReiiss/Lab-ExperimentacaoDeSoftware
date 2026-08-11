"""
Query GraphQL da RQ02 (contribuição externa).

Busca repositórios ordenados por estrelas e traz, para cada um, o total
de pull requests com estado MERGED — é esse número que a métrica usa como
proxy de contribuição externa aceita pelo projeto.
"""

RQ02_QUERY = """
query($searchQuery: String!, $first: Int!, $cursor: String) {
  search(query: $searchQuery, type: REPOSITORY, first: $first, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes {
      ... on Repository {
        name
        owner { login }
        pullRequests(states: MERGED) {
          totalCount
        }
      }
    }
  }
}
"""

RQ02_SEARCH_QUERY = "stars:>1 sort:stars-desc"

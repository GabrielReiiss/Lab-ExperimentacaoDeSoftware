"""
Query GraphQL da RQ06 (percentual de issues fechadas).

Busca repositórios ordenados por estrelas e traz, para cada um, o total
de issues fechadas (`closedIssues`) e o total geral de issues
(`totalIssues`, sem filtro de estado) — usados para calcular a razão
issues fechadas / total de issues.
"""

RQ06_QUERY = """
query($searchQuery: String!, $first: Int!, $cursor: String) {
  search(query: $searchQuery, type: REPOSITORY, first: $first, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes {
      ... on Repository {
        name
        owner { login }
        closedIssues: issues(states: CLOSED) {
          totalCount
        }
        totalIssues: issues {
          totalCount
        }
      }
    }
  }
}
"""

RQ06_SEARCH_QUERY = "stars:>1 sort:stars-desc"

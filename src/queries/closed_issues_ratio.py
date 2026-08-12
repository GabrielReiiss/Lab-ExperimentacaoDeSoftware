"""
Query da RQ06. Traz o total de issues fechadas e o total geral de
issues de cada repositório (dois alias sobre o campo issues).
"""

CLOSED_ISSUES_RATIO_QUERY = """
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

CLOSED_ISSUES_RATIO_SEARCH_QUERY = "stars:>1 sort:stars-desc"

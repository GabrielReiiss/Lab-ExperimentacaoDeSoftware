"""
Query da RQ02. Traz o total de pull requests com status MERGED de cada
repositório.
"""

EXTERNAL_CONTRIBUTION_QUERY = """
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

EXTERNAL_CONTRIBUTION_SEARCH_QUERY = "stars:>1 sort:stars-desc"

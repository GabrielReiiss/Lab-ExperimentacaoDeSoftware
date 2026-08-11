"""
Query da RQ02. Traz o total de pull requests com status MERGED de cada
repositório.
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

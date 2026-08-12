"""
Query da RQ03, traz o total de releases de cada repositório, campo
releases.totalCount.
"""

RELEASE_FREQUENCY_QUERY = """
query($searchQuery: String!, $first: Int!, $cursor: String) {
  search(query: $searchQuery, type: REPOSITORY, first: $first, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes {
      ... on Repository {
        name
        owner { login }
        releases {
          totalCount
        }
      }
    }
  }
}
"""

RELEASE_FREQUENCY_SEARCH_QUERY = "stars:>1 sort:stars-desc"

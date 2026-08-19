"""
Query unificada da Sprint 01: traz, numa única consulta, todos os
campos necessários para as 6 métricas já validadas individualmente
(repo_age, external_contribution, release_frequency, update_frequency,
primary_language, closed_issues_ratio), além de stargazerCount, usado
pelo filtro de faixa de estrelas do dashboard.
"""

TOP_REPOSITORIES_QUERY = """
query($searchQuery: String!, $first: Int!, $cursor: String) {
  search(query: $searchQuery, type: REPOSITORY, first: $first, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes {
      ... on Repository {
        name
        owner { login }
        createdAt
        pushedAt
        stargazerCount
        primaryLanguage { name }
        pullRequests(states: MERGED) {
          totalCount
        }
        releases {
          totalCount
        }
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

TOP_REPOSITORIES_SEARCH_QUERY = "stars:>1 sort:stars-desc"

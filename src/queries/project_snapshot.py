PROJECT_SNAPSHOT_QUERY = """
query($login: String!, $number: Int!, $first: Int!, $cursor: String) {
  user(login: $login) {
    projectV2(number: $number) {
      items(first: $first, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          fieldValueByName(name: "Status") {
            ... on ProjectV2ItemFieldSingleSelectValue {
              name
            }
          }
          content {
            ... on Issue {
              number
              title
              url
              assignees(first: 10) {
                nodes { login }
              }
            }
          }
        }
      }
    }
  }
}
"""

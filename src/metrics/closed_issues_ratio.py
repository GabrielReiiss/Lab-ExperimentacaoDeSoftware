"""
Métrica da RQ06: razão entre issues fechadas e total de issues do
repositório.
"""


def extract_closed_issues_ratio(repo: dict) -> float | None:
    """Retorna None quando o repositório não tem nenhuma issue."""
    total = repo["totalIssues"]["totalCount"]
    closed = repo["closedIssues"]["totalCount"]

    if total == 0:
        return None

    return closed / total

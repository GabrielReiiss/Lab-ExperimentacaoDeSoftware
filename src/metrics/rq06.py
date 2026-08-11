"""
Métrica da RQ06: sistemas populares possuem um alto percentual de issues
fechadas?

Métrica: razão entre issues fechadas e total de issues do repositório.
"""


def extract_rq06(repo: dict) -> float | None:
    """
    Recebe um node de repositório (precisa ter os campos `closedIssues {
    totalCount }` e `totalIssues { totalCount }`) e devolve a razão
    issues fechadas / total de issues, entre 0 e 1.

    Devolve `None` quando o repositório não tem nenhuma issue (divisão
    por zero não faz sentido nesse caso).
    """
    total = repo["totalIssues"]["totalCount"]
    closed = repo["closedIssues"]["totalCount"]

    if total == 0:
        return None

    return closed / total

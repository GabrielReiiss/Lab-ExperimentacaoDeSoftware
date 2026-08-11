"""
Métrica da RQ02: sistemas populares recebem muita contribuição externa?

Métrica: total de pull requests aceitas (mescladas) no repositório. Não
distingue autor interno/externo — é uma aproximação: assume-se que boa
parte das PRs mescladas em projetos populares vem de fora do time
principal do projeto.
"""


def extract_rq02(repo: dict) -> int:
    """
    Recebe um node de repositório (precisa ter o campo
    `pullRequests { totalCount }`, filtrado por `states: MERGED` na
    query) e devolve o total de pull requests aceitas.
    """
    return repo["pullRequests"]["totalCount"]

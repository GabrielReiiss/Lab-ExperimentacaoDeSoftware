"""
Métrica da RQ02: total de pull requests aceitas (mescladas), usado como
aproximação de contribuição externa.
"""


def extract_rq02(repo: dict) -> int:
    return repo["pullRequests"]["totalCount"]

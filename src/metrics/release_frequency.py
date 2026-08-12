"""
Métrica da RQ03, total de releases de cada repositório.
"""


def extract_release_frequency(repo: dict) -> int:
    return repo["releases"]["totalCount"]

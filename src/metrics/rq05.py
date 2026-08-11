"""
Métrica da RQ05: sistemas populares são escritos nas linguagens mais populares?

Métrica: linguagem primária de cada repositório (campo `primaryLanguage`
retornado pela API GraphQL do GitHub).
"""

def extract_rq05(repo: dict) -> str | None:
    """
    Recebe um node de repositório e devolve o
    nome da linguagem primária, ou None se não houver.
    """
    primary_language = repo.get("primaryLanguage")
    return primary_language["name"] if primary_language else None

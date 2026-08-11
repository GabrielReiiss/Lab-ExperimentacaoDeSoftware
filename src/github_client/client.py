"""
Client HTTP genérico para a API GraphQL do GitHub.

Esta é a única peça do projeto que sabe falar HTTP com a API. Qualquer
consulta nova reaproveita esta mesma função, só passando query/variables diferentes.
"""
import requests

from config import GITHUB_GRAPHQL_URL, GITHUB_TOKEN
from src.github_client.errors import GraphQLError


def run_query(query: str, variables: dict = None) -> dict:
    """
    Envia uma query/mutation GraphQL para a API do GitHub.

    Retorna o conteúdo de `data` já "desembrulhado". E levanta GraphQLError
    se a resposta trouxer a chave "errors".
    """
    body = {"query": query}
    if variables is not None:
        body["variables"] = variables

    response = requests.post(
        GITHUB_GRAPHQL_URL,
        json=body,
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}"},
    )
    response.raise_for_status()
    payload = response.json()

    if payload.get("errors") is not None:
        raise GraphQLError(payload["errors"][0]["message"], payload["errors"])

    return payload["data"]

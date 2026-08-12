"""
Client HTTP genérico para a API GraphQL do GitHub.

Esta é a única peça do projeto que sabe falar HTTP com a API. Qualquer
consulta nova reaproveita esta mesma função, só passando query/variables diferentes.
"""
import time
import requests

from config import GITHUB_GRAPHQL_URL, GITHUB_TOKEN
from src.github_client.errors import GraphQLError

MAX_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 2  # espera entre tentativas, dobra a cada retry (backoff)

# Erros do lado do servidor do GitHub.
RETRYABLE_STATUS_CODES = {502, 503, 504}

# Sessão HTTP reaproveitada entre todas as chamadas.
_session = requests.Session()
_session.headers.update({"Authorization": f"Bearer {GITHUB_TOKEN}"})

def run_query(query: str, variables: dict = None) -> dict:
    """
    Envia uma query/mutation GraphQL para a API do GitHub.

    Retorna o conteúdo de `data` já "desembrulhado". Levanta GraphQLError
    se a resposta trouxer a chave "errors".

    Tenta de novo até MAX_ATTEMPTS vezes se a API responder com um erro
    5xx transiente (502/503/504).
    """
    body = {"query": query}
    if variables is not None:
        body["variables"] = variables

    last_error = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        response = _session.post(GITHUB_GRAPHQL_URL, json=body)

        if response.status_code in RETRYABLE_STATUS_CODES:
            last_error = requests.exceptions.HTTPError(
                f"{response.status_code} {response.reason} (tentativa {attempt}/{MAX_ATTEMPTS})",
                response=response,
            )
            if attempt < MAX_ATTEMPTS:
                time.sleep(RETRY_DELAY_SECONDS * attempt)
                continue
            raise last_error

        response.raise_for_status()
        payload = response.json()

        if payload.get("errors") is not None:
            raise GraphQLError(payload["errors"][0]["message"], payload["errors"])

        return payload["data"]

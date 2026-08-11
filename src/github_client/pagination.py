"""
Paginação genérica por cursor, reaproveitável por qualquer query que siga
o padrão de conexão do GitHub GraphQL (pageInfo { hasNextPage endCursor }
+ nodes).
"""
from typing import Callable, Iterator

from src.github_client.client import run_query


def paginate(
    query: str,
    base_variables: dict,
    get_connection: Callable[[dict], dict],
    page_size: int = 50,
) -> Iterator[list[dict]]:
    """
    Generator que percorre todas as páginas de uma query paginada.

    Args:
        query: query GraphQL que declara $cursor e $first, e os usa como
            `first: $first, after: $cursor` em algum campo de conexão.
        base_variables: variáveis fixas da query.
        get_connection: recebe o `data` retornado por run_query() e
            devolve o objeto de conexão que contém "pageInfo" e "nodes".
        page_size: quantos itens pedir por página.

    Yields:
        A lista de nodes de cada página, uma por vez, até
        `hasNextPage` ser False.
    """
    cursor = None

    while True:
        variables = {**base_variables, "first": page_size, "cursor": cursor}
        data = run_query(query, variables)
        connection = get_connection(data)

        yield connection["nodes"]

        page_info = connection["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        cursor = page_info["endCursor"]

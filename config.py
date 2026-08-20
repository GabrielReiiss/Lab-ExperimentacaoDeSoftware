"""
Configuração centralizada do projeto: variáveis de ambiente e constantes
compartilhadas entre client, scripts e testes.
"""
import os

from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

if not GITHUB_TOKEN:
    raise RuntimeError(
        "GITHUB_TOKEN não encontrado. Crie um arquivo .env na raiz do "
        "projeto com a linha: GITHUB_TOKEN=seu_token_aqui"
    )


def load_project_config() -> tuple[str, int]:
    owner = os.getenv("GITHUB_PROJECT_OWNER")
    number = os.getenv("GITHUB_PROJECT_NUMBER")

    if not owner or not number:
        raise RuntimeError(
            "GITHUB_PROJECT_OWNER/GITHUB_PROJECT_NUMBER não encontrados. Adicione "
            "ao .env: GITHUB_PROJECT_OWNER=seu_usuario e GITHUB_PROJECT_NUMBER=numero_do_project "
            "(o número aparece na URL do Project, ex.: github.com/users/x/projects/1)"
        )

    return owner, int(number)

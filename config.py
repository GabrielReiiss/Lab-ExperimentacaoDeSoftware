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

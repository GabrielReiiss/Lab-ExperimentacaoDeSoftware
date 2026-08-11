# Laboratório 01

Trabalho da disciplina Laboratório de Experimentação de Software, cujo
objetivo é caracterizar repositórios populares open-source do GitHub a
partir de dados coletados via API GraphQL, respondendo a 7 questões de
pesquisa (idade, contribuição externa, releases, frequência de
atualização, linguagem, percentual de issues fechadas) sobre os 1.000
repositórios com mais estrelas.

## Setup

1. `pip install -r requirements.txt`
2. Crie um arquivo `.env` na raiz com um [token pessoal do GitHub](https://github.com/settings/tokens):
   ```
   GITHUB_TOKEN=seu_token_aqui
   ```

## Estrutura

```
├── 📁 data                    # (pendente) CSVs gerados pela coleta
│   ├── 📁 raw                   # (pendente) CSV dos repositórios coletados
│   └── 📁 snapshots             # (pendente) CSVs de fechamento de sprint do GitHub Projects
├── 📁 reports                 # (pendente) saída do relatório final
│   └── 📁 figures               # (pendente) gráficos gerados para o relatório (Lab01S03)
├── 📁 scripts                 # (pendente) runners que orquestram client + queries + metrics
├── 📁 src
│   ├── 📁 analysis              # (pendente) estatísticas e gráficos (Lab01S03)
│   ├── 📁 export                # (pendente) escrita de CSV
│   ├── 📁 github_client         # client GraphQL genérico
│   ├── 📁 metrics               # (pendente) um extract_rqXX por RQ: o "o que fazer com a resposta"
│   ├── 📁 queries               # (pendente) strings de query GraphQL: o "o quê perguntar" de cada RQ
│   └── __init__.py
├── 📁 tests
│   └── test_pagination.py     # testa paginate() com run_query (mocks)
├── .gitignore
├── README.md
├── config.py                  # carrega token/URL da API a partir do .env
└── requirements.txt
```

## Como usar (para quem for criar um endpoint de consulta)

```python
from src.github_client.client import run_query
from src.github_client.pagination import paginate

# 1. escreva sua query GraphQL, com $cursor e $first declarados
QUERY = """
query($searchQuery: String!, $first: Int!, $cursor: String) {
  search(query: $searchQuery, type: REPOSITORY, first: $first, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes { ... on Repository { name } }
  }
}
"""

# 2. consulta simples, sem paginação
data = run_query(QUERY, {"searchQuery": "stars:>1", "first": 5, "cursor": None})

# 3. ou percorra todas as páginas automaticamente
for page in paginate(
    QUERY,
    base_variables={"searchQuery": "stars:>1"},
    get_connection=lambda data: data["search"],
    page_size=50,
):
    for node in page:
        ...  # sua lógica de extração aqui
```

`get_connection` existe porque o objeto com `pageInfo`/`nodes` fica em
caminhos diferentes conforme a query (`data["search"]`,
`data["repository"]["issues"]`, etc.), quem cria a query informa onde
achar isso.

## Rodando os testes

```
python -m pytest
```

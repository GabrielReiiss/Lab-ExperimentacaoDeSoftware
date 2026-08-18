# Laboratório 01

Trabalho da disciplina Laboratório de Experimentação de Software, cujo
objetivo é caracterizar repositórios populares open-source do GitHub a
partir de dados coletados via API GraphQL, respondendo a 7 questões de
pesquisa (idade, contribuição externa, releases, frequência de
atualização, linguagem, percentual de issues fechadas) sobre os 1.000
repositórios com mais estrelas.

## Fonte de referência: linguagens mais populares (RQ05)

A RQ05 pergunta se repositórios populares são escritos nas linguagens mais
populares, comparando a distribuição de `primary_language` coletada nos
1.000 repositórios com um ranking externo de mercado. A fonte adotada para
esse ranking é o **GitHub Octoverse**, edição mais recente disponível no
momento da análise formal (Lab01S03):

> Octoverse 2025: ["Octoverse: A new developer joins GitHub every second as AI leads TypeScript to #1"](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/), GitHub Blog, outubro/2025.

Essa é a mesma referência a ser usada em qualquer comparação com "linguagens
mais populares" ao longo de todo o laboratório (RQ05 e o recorte por
linguagem da RQ07), para manter consistência entre as sprints. A
comparação quantitativa em si (distribuição coletada x ranking do
Octoverse) fica para a análise formal da Lab01S03, conforme o cronograma
do enunciado.

## Setup

1. `pip install -r requirements.txt`
2. Crie um arquivo `.env` na raiz com um [token pessoal do GitHub](https://github.com/settings/tokens):
   ```
   GITHUB_TOKEN=seu_token_aqui
   ```

## Estrutura

```
├── 📁 data                    # (pendente, Lab01S02) CSVs gerados pela coleta
│   ├── 📁 raw
│   └── 📁 snapshots            # (pendente) CSVs de fechamento de sprint do GitHub Projects
├── 📁 reports                 # (pendente, Lab01S03) saída do relatório final
│   └── 📁 figures
├── 📁 scripts
│   ├── fetch_repositories.py    # script único de consulta do grupo: 100 repos, todas as métricas
│   └── validate_*.py            # validação individual de cada RQ em amostra pequena (Lab01S01)
├── 📁 src
│   ├── 📁 analysis              # (pendente, Lab01S03) estatísticas e gráficos
│   ├── 📁 export                # (pendente, Lab01S02) escrita de CSV
│   ├── 📁 github_client         # client GraphQL genérico
│   │   ├── client.py              # run_query(query, variables) -> data
│   │   ├── pagination.py          # paginate(): generator por cursor (Lab01S02)
│   │   └── errors.py              # GraphQLError
│   ├── 📁 metrics                # extract_* de cada RQ (repo_age, external_contribution,
│   │                              #   release_frequency, update_frequency, primary_language,
│   │                              #   closed_issues_ratio)
│   ├── 📁 queries                # query de cada RQ + top_repositories.py (query unificada)
│   └── __init__.py
├── 📁 tests                   # um teste por métrica + client/paginação/integração
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

# Laboratório 01

Trabalho da disciplina Laboratório de Experimentação de Software, cujo
objetivo é caracterizar repositórios populares open-source do GitHub a
partir de dados coletados via API GraphQL, respondendo a 7 questões de
pesquisa (idade, contribuição externa, releases, frequência de
atualização, linguagem, percentual de issues fechadas) sobre os 1.000
repositórios com mais estrelas. O relatório final está em [`Relatorio.md`](Relatorio.md).

## Fonte de referência: linguagens mais populares (RQ05)

A RQ05 pergunta se repositórios populares são escritos nas linguagens mais
populares, comparando a distribuição de `primary_language` coletada nos
1.000 repositórios com um ranking externo de mercado. A fonte adotada para
esse ranking é o **GitHub Octoverse**:

> Octoverse 2025: ["Octoverse: A new developer joins GitHub every second as AI leads TypeScript to #1"](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/), GitHub Blog, outubro/2025.

Essa é a mesma referência usada em qualquer comparação com "linguagens
mais populares" ao longo de todo o laboratório (RQ05 e o recorte por
linguagem da RQ07).

## Setup

1. `pip install -r requirements.txt`
2. Crie um arquivo `.env` na raiz com um [token pessoal do GitHub](https://github.com/settings/tokens):
   ```
   GITHUB_TOKEN=seu_token_aqui
   ```

## Estrutura

```
├── 📁 dashboard                # dashboard Streamlit (multi-página)
│   ├── app.py                    # entrypoint
│   ├── data.py                   # carregamento/cache dos dados coletados
│   ├── metrics_percentile.py     # comparador individual vs. população
│   ├── 📁 pages                  # dados, exploratório, correlação, comparador, snapshots
│   └── 📁 sections                # um módulo de gráficos por RQ (rq01..rq07)
├── 📁 data
│   ├── 📁 raw                    # repositories.csv da coleta oficial (980 repos)
│   ├── 📁 snapshots               # CSVs de fechamento de sprint do GitHub Projects
│   └── 📁 Prints                  # imagens dos gráficos usadas no relatório
├── 📁 docs
│   └── benchmark_pagination.md   # metodologia e números completos do benchmark (seção 4.6)
├── 📁 reports                  # saída do relatório final
│   ├── 📁 figures                 # scatterplots de correlação, distribuição do índice de saúde
│   └── *.pdf                      # entregas parciais (introdução/hipóteses, validações por RQ)
├── 📁 scripts
│   ├── fetch_repositories.py     # script principal: coleta e monta o CSV com as 6 métricas
│   ├── snapshot_project.py       # snapshot do board do GitHub Projects
│   ├── compute_correlations.py   # matriz de correlação Pearson/Spearman (inovação, 4.4)
│   ├── compute_health_index.py   # índice composto de saúde/maturidade (inovação, 4.5)
│   ├── benchmark_pagination.py   # benchmark adaptativa vs. fixa (inovação, 4.6)
│   ├── diagnose_adaptive.py      # diagnóstico de retry duplicado usado em 3.1
│   ├── validate_*.py             # validação individual de cada RQ em amostra pequena
│   └── 📁 experimental
│       └── collect_beyond_1000.py  # coleta além do teto de 1.000 via particionamento por stars
├── 📁 src
│   ├── 📁 analysis              # estatísticas: correlação, índice de saúde, normalização,
│   │                              #   distribuição/quebra por linguagem, uma função por RQ01-06
│   ├── 📁 export                # escrita de CSV
│   ├── 📁 github_client         # client GraphQL genérico
│   │   ├── client.py              # run_query(query, variables) -> data
│   │   ├── pagination.py          # paginate(): generator por cursor, page_size adaptativo
│   │   └── errors.py              # GraphQLError
│   ├── 📁 metrics                # extract_* de cada RQ (repo_age, external_contribution,
│   │                              #   release_frequency, update_frequency, primary_language,
│   │                              #   closed_issues_ratio, project_snapshot)
│   ├── 📁 queries                # query de cada RQ + top_repositories.py (query unificada)
│   ├── 📁 cli                    # spinner de progresso da coleta
│   └── __init__.py
├── 📁 tests                   # um teste por métrica/análise + client/paginação/integração
├── .gitignore
├── README.md
├── Relatorio.md                # relatório final do laboratório
├── config.py                  # carrega token/URL da API a partir do .env
└── requirements.txt
```

## Como rodar a coleta

```
python -m scripts.fetch_repositories            # 1.000 repositórios, todas as métricas -> data/raw/repositories.csv
python -m scripts.fetch_repositories --total 50 --page-size 10   # amostra pequena, pra testar
```

## Como rodar o dashboard

```
streamlit run dashboard/app.py
```

Se `data/raw/repositories.csv` ainda não existir, o dashboard dispara a
coleta automaticamente na primeira execução.

## Scripts das inovações (seção 3.6 do relatório)

```
python -m scripts.compute_correlations     # matriz de correlação Pearson/Spearman entre as 6 métricas
python -m scripts.compute_health_index     # índice composto de saúde/maturidade por repositório
python -m scripts.benchmark_pagination     # benchmark paginação adaptativa vs. fixa

# coleta além do teto de 1.000 (fora do pipeline oficial): particiona a busca
# em faixas de stars: que não se sobrepõem e soma os resultados
python -m scripts.experimental.collect_beyond_1000 --total 2000
python -m scripts.experimental.collect_beyond_1000 --total 2000 --page-size 10 --safe-max-per-range 900

# teste direcionado: começa as faixas a partir de um teto de estrelas em vez
# do topo do ranking (usado em 4.6 pra medir repositórios "menos populares")
python -m scripts.experimental.collect_beyond_1000 --total 2000 --max-stars 500
```

## Rodando os testes

```
python -m pytest
```

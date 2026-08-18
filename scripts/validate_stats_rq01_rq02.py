"""
Estatísticas de validação de dados para RQ01 e RQ02 (Lab01 Sprint 02).

Lê o dataset completo (data/raw/repositories.csv) e calcula, para as
colunas age_days (RQ01) e merged_pull_requests (RQ02): valores ausentes,
mínimo, mediana, P75, máximo e média, além de destacar outliers/achados
para dar suporte ao relatório de validação (reports/validacao_rq01_rq02.pdf).

Uso: python -m scripts.validate_stats_rq01_rq02
"""
import pandas as pd

DATASET_PATH = "data/raw/repositories.csv"


def describe_column(df: pd.DataFrame, column: str) -> dict:
    series = df[column]
    missing = series.isna().sum()
    return {
        "missing": missing,
        "missing_pct": missing / len(series) * 100,
        "min": series.min(),
        "median": series.median(),
        "p75": series.quantile(0.75),
        "max": series.max(),
        "mean": series.mean(),
    }


def print_stats(title: str, stats: dict) -> None:
    print(f"\n{title}")
    print(f"  Valores ausentes: {stats['missing']} ({stats['missing_pct']:.1f}%)")
    print(f"  Minimo:  {stats['min']:.1f}")
    print(f"  Mediana: {stats['median']:.1f}")
    print(f"  P75:     {stats['p75']:.1f}")
    print(f"  Maximo:  {stats['max']:.1f}")
    print(f"  Media:   {stats['mean']:.1f}")


def main():
    df = pd.read_csv(DATASET_PATH)
    print(f"Dataset: {DATASET_PATH}, {len(df)} repositorios.\n")

    age_stats = describe_column(df, "age_days")
    print_stats("RQ01: age_days (idade em dias)", age_stats)

    pr_stats = describe_column(df, "merged_pull_requests")
    print_stats("RQ02: merged_pull_requests (PRs mescladas)", pr_stats)

    # Achados: repositórios com zero PRs mescladas
    zero_pr = df[df["merged_pull_requests"] == 0]
    print(f"\nRepositorios com 0 PRs mescladas: {len(zero_pr)} ({len(zero_pr)/len(df)*100:.1f}%)")
    if len(zero_pr):
        print(zero_pr[["owner", "name", "merged_pull_requests"]].head(10).to_string(index=False))

    # Achados: repositórios mais antigos e mais novos
    print("\n5 repositorios mais antigos:")
    print(df.nlargest(5, "age_days")[["owner", "name", "age_days"]].to_string(index=False))
    print("\n5 repositorios mais novos:")
    print(df.nsmallest(5, "age_days")[["owner", "name", "age_days"]].to_string(index=False))

    # Achados: repositórios com mais PRs mescladas (outliers no topo)
    print("\n5 repositorios com mais PRs mescladas:")
    print(df.nlargest(5, "merged_pull_requests")[["owner", "name", "merged_pull_requests"]].to_string(index=False))


if __name__ == "__main__":
    main()

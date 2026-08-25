"""
Calcula a matriz de correlação (Pearson e Spearman) entre as 6 métricas
normalizadas (idade, PRs aceitas, releases, tempo desde update, razão de
issues fechadas, linguagem popular).

Uso:
    python -m scripts.compute_correlations
    python -m scripts.compute_correlations --input data/raw/repositories.csv --figures-dir reports/figures
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.analysis.correlation import (
    METRIC_LABELS,
    REQUIRED_PAIRS,
    build_normalized_metrics,
    correlation_matrices,
    interpret,
    pairs_above_threshold,
)

DEFAULT_INPUT = "data/raw/repositories.csv"
DEFAULT_FIGURES_DIR = "reports/figures"
THRESHOLD = 0.3


def _print_matrix(titulo: str, matriz: pd.DataFrame) -> None:
    print(f"\n{titulo}")
    print(matriz.round(2).to_string())


def _plot_pair(normalized: pd.DataFrame, metric_a: str, metric_b: str, figures_dir: str) -> str:
    dados = normalized[[metric_a, metric_b]].dropna()
    x = dados[metric_a].to_numpy()
    y = dados[metric_b].to_numpy()

    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.scatter(x, y, alpha=0.4, s=15, color="#2a78d6")

    if len(x) > 1 and np.std(x) > 0:
        coeficientes = np.polyfit(x, y, 1)
        tendencia = np.poly1d(coeficientes)
        x_linha = np.linspace(x.min(), x.max(), 100)
        ax.plot(x_linha, tendencia(x_linha), color="#d62a2a", linewidth=2)

    ax.set_xlabel(METRIC_LABELS.get(metric_a, metric_a))
    ax.set_ylabel(METRIC_LABELS.get(metric_b, metric_b))
    ax.set_title(f"{METRIC_LABELS.get(metric_a, metric_a)} x {METRIC_LABELS.get(metric_b, metric_b)}")
    fig.tight_layout()

    caminho = f"{figures_dir}/corr_{metric_a}_x_{metric_b}.png"
    fig.savefig(caminho, dpi=150)
    plt.close(fig)
    return caminho


def main(input_path: str, figures_dir: str) -> None:
    df = pd.read_csv(input_path)
    normalized = build_normalized_metrics(df)
    pearson, spearman = correlation_matrices(normalized)

    _print_matrix("Matriz de correlação (Pearson):", pearson)
    _print_matrix("Matriz de correlação (Spearman):", spearman)

    print("\nPares obrigatórios (issue #33):")
    for metric_a, metric_b in REQUIRED_PAIRS:
        r = pearson.loc[metric_a, metric_b]
        rho = spearman.loc[metric_a, metric_b]
        print(f"  {interpret(metric_a, metric_b, r, rho)}")

    pares_relevantes = pairs_above_threshold(pearson, THRESHOLD)
    print(f"\nPares com |r| > {THRESHOLD} (gerando scatterplot em {figures_dir}/):")
    if not pares_relevantes:
        print("  Nenhum par ultrapassou o limiar.")
    for metric_a, metric_b, r in pares_relevantes:
        rho = spearman.loc[metric_a, metric_b]
        caminho = _plot_pair(normalized, metric_a, metric_b, figures_dir)
        print(f"  {interpret(metric_a, metric_b, r, rho)}")
        print(f"    -> {caminho}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default=DEFAULT_INPUT)
    parser.add_argument("--figures-dir", type=str, default=DEFAULT_FIGURES_DIR)
    args = parser.parse_args()

    main(args.input, args.figures_dir)

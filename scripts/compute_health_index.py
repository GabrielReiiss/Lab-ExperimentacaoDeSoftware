"""
Calcula o índice composto de saúde/maturidade (RQ01-RQ06 combinadas),
grava a coluna "health_index" no dataset e gera o histograma da
distribuição em reports/figures/.

Uso:
    python -m scripts.compute_health_index
    python -m scripts.compute_health_index --input data/raw/repositories.csv --figures-dir reports/figures
"""
import argparse

import matplotlib.pyplot as plt
import pandas as pd

from src.analysis.health_index import add_health_index, health_index_summary

DEFAULT_PATH = "data/raw/repositories.csv"
DEFAULT_FIGURES_DIR = "reports/figures"
ACCENT = "#2a78d6"


def _plot_distribution(df: pd.DataFrame, figures_dir: str) -> str:
    valores = df["health_index"].dropna()

    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.hist(valores, bins=30, color=ACCENT)
    ax.set_xlabel("Índice de saúde/maturidade")
    ax.set_ylabel("Repositórios")
    ax.set_title("Distribuição do índice de saúde/maturidade")
    fig.tight_layout()

    caminho = f"{figures_dir}/health_index_distribuicao.png"
    fig.savefig(caminho, dpi=150)
    plt.close(fig)
    return caminho


def main(input_path: str, output_path: str, figures_dir: str) -> None:
    df = pd.read_csv(input_path)
    df = add_health_index(df)
    resumo = health_index_summary(df)

    print(f"Mediana do health_index: {resumo['median']:.3f}")
    print(f"Média do health_index: {resumo['mean']:.3f}")
    print(f"Repositórios sem score (dados insuficientes): {resumo['missing']}")

    print("\nTop 5 (maior health_index):")
    top5 = df.nlargest(5, "health_index")
    for _, row in top5.iterrows():
        print(f"  {row['owner']}/{row['name']}: {row['health_index']:.3f}")

    print("\nBottom 5 (menor health_index):")
    bottom5 = df.nsmallest(5, "health_index")
    for _, row in bottom5.iterrows():
        print(f"  {row['owner']}/{row['name']}: {row['health_index']:.3f}")

    caminho_figura = _plot_distribution(df, figures_dir)
    print(f"\nHistograma salvo em {caminho_figura}")

    df.to_csv(output_path, index=False)
    print(f"Dataset atualizado em {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default=DEFAULT_PATH)
    parser.add_argument("--output", type=str, default=DEFAULT_PATH)
    parser.add_argument("--figures-dir", type=str, default=DEFAULT_FIGURES_DIR)
    args = parser.parse_args()

    main(args.input, args.output, args.figures_dir)

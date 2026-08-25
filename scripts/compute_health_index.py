"""
Calcula o índice composto de saúde/maturidade (RQ01-RQ06 combinadas) e
grava a coluna "health_index" no dataset.

Uso:
    python -m scripts.compute_health_index
    python -m scripts.compute_health_index --input data/raw/repositories.csv
"""
import argparse

import pandas as pd

from src.analysis.health_index import add_health_index

DEFAULT_PATH = "data/raw/repositories.csv"


def main(input_path: str, output_path: str) -> None:
    df = pd.read_csv(input_path)
    df = add_health_index(df)

    print(f"Mediana do health_index: {df['health_index'].median():.3f}")
    print(f"Repositórios sem score (dados insuficientes): {df['health_index'].isna().sum()}")

    print("\nTop 5 (maior health_index):")
    top5 = df.nlargest(5, "health_index")
    for _, row in top5.iterrows():
        print(f"  {row['owner']}/{row['name']}: {row['health_index']:.3f}")

    print("\nBottom 5 (menor health_index):")
    bottom5 = df.nsmallest(5, "health_index")
    for _, row in bottom5.iterrows():
        print(f"  {row['owner']}/{row['name']}: {row['health_index']:.3f}")

    df.to_csv(output_path, index=False)
    print(f"\nDataset atualizado em {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default=DEFAULT_PATH)
    parser.add_argument("--output", type=str, default=DEFAULT_PATH)
    args = parser.parse_args()

    main(args.input, args.output)

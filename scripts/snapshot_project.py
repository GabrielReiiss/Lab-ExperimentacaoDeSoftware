"""
Snapshot de fechamento de sprint do GitHub Projects para CSV.

Uso: python -m scripts.snapshot_project --sprint S02
"""
import argparse
from datetime import date
from pathlib import Path

from config import load_project_config
from src.export.csv_writer import write_csv
from src.github_client.pagination import paginate
from src.metrics.project_snapshot import extract_snapshot_row
from src.queries.project_snapshot import PROJECT_SNAPSHOT_QUERY

PAGE_SIZE = 50
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "snapshots"


def main(sprint: str) -> None:
    owner, number = load_project_config()
    data_snapshot = date.today().isoformat()

    print(f"Buscando itens do Project #{number} de '{owner}'...")

    pages = paginate(
        PROJECT_SNAPSHOT_QUERY,
        base_variables={"login": owner, "number": number},
        get_connection=lambda data: data["user"]["projectV2"]["items"],
        page_size=PAGE_SIZE,
    )

    linhas = []
    ignorados = 0
    try:
        for page in pages:
            for node in page:
                linha = extract_snapshot_row(node, sprint, data_snapshot)
                if linha is None:
                    ignorados += 1
                    continue
                linhas.append(linha)
    except TypeError:
        raise SystemExit(
            f"Project #{number} não encontrado para o usuário '{owner}'. "
            "Confira GITHUB_PROJECT_OWNER/GITHUB_PROJECT_NUMBER no .env."
        )

    print(f"\n{len(linhas)} item(ns) exportado(s) ({ignorados} draft/sem Issue ignorado(s))\n")
    for linha in linhas:
        print(f"  #{linha['issue_number']:<5} {str(linha['status']):12} {linha['assignees']:20} {linha['titulo']}")

    output_path = OUTPUT_DIR / f"snapshot_{sprint}.csv"
    write_csv(linhas, output_path)
    print(f"\nSnapshot salvo em: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sprint", required=True, help="Identificador da sprint (ex.: S01, S02, S03).")
    args = parser.parse_args()

    main(args.sprint)

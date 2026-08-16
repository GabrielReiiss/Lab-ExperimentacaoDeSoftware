"""
Escrita dos dados coletados em CSV.
"""
import csv
from pathlib import Path


def write_csv(rows: list[dict], path: str | Path) -> None:
    """Escreve `rows` (lista de dicts com as mesmas chaves) num CSV em `path`."""
    if not rows:
        raise ValueError("Nenhum repositório para exportar.")

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

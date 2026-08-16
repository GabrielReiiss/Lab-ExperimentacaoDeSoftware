"""Testes de write_csv, sem tocar a API."""
import csv

import pytest

from src.export.csv_writer import write_csv

ROWS = [
    {"name": "repo-a", "owner": "owner-a", "age_days": 100},
    {"name": "repo-b", "owner": "owner-b", "age_days": 200},
]


def test_write_csv_writes_header_and_rows(tmp_path):
    output = tmp_path / "repositories.csv"

    write_csv(ROWS, output)

    with output.open(newline="", encoding="utf-8") as csv_file:
        reader = list(csv.DictReader(csv_file))

    assert reader == [
        {"name": "repo-a", "owner": "owner-a", "age_days": "100"},
        {"name": "repo-b", "owner": "owner-b", "age_days": "200"},
    ]


def test_write_csv_creates_parent_directories(tmp_path):
    output = tmp_path / "nested" / "dir" / "repositories.csv"

    write_csv(ROWS, output)

    assert output.exists()


def test_write_csv_raises_on_empty_rows(tmp_path):
    with pytest.raises(ValueError):
        write_csv([], tmp_path / "repositories.csv")

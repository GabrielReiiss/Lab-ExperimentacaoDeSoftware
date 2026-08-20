from pathlib import Path

import pandas as pd
import streamlit as st

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "repositories.csv"
SNAPSHOTS_DIR = Path(__file__).resolve().parent.parent / "data" / "snapshots"

TOTAL_REPOSITORIOS = 1000
PAGE_SIZE = 10

@st.cache_data
def load_repositories() -> pd.DataFrame:
    return pd.read_csv(CSV_PATH)


def list_snapshots() -> list[Path]:
    return sorted(SNAPSHOTS_DIR.glob("snapshot_*.csv"))


def load_snapshot(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)

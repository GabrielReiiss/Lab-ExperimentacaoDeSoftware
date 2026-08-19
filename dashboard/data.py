from pathlib import Path

import pandas as pd
import streamlit as st

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "repositories.csv"

TOTAL_REPOSITORIOS = 1000
PAGE_SIZE = 10

@st.cache_data
def load_repositories() -> pd.DataFrame:
    return pd.read_csv(CSV_PATH)

"""
Testa extract_rq05() com dados fixos, sem bater na API de verdade.
"""

from src.metrics.rq05 import extract_rq05

def test_extract_rq05_returns_language_name():
    repo = {"primaryLanguage": {"name": "Python"}}
    assert extract_rq05(repo) == "Python"

def test_extract_rq05_returns_none_when_missing():
    repo = {"primaryLanguage": None}
    assert extract_rq05(repo) is None

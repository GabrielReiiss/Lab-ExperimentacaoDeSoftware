"""
Testa extract_primary_language() com dados fixos, sem bater na API de verdade.
"""

from src.metrics.primary_language import extract_primary_language

def test_extract_primary_language_returns_language_name():
    repo = {"primaryLanguage": {"name": "Python"}}
    assert extract_primary_language(repo) == "Python"

def test_extract_primary_language_returns_none_when_missing():
    repo = {"primaryLanguage": None}
    assert extract_primary_language(repo) is None

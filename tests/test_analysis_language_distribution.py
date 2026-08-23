import pandas as pd

from src.analysis.language_distribution import compare_with_reference, language_distribution


def test_language_distribution_counts_and_shares():
    df = pd.DataFrame({
        "primary_language": ["Python", "Python", "JavaScript", None],
    })

    resultado = language_distribution(df)

    assert resultado[0] == {"language": "Python", "count": 2, "share": 0.5}
    assert {"language": "Sem linguagem", "count": 1, "share": 0.25} in resultado
    assert {"language": "JavaScript", "count": 1, "share": 0.25} in resultado


def test_language_distribution_sorted_by_count_descending():
    df = pd.DataFrame({
        "primary_language": ["Go", "Python", "Python", "Python"],
    })

    resultado = language_distribution(df)

    assert resultado[0]["language"] == "Python"
    assert resultado[0]["count"] == 3


def test_compare_with_reference_matches_collected_rank_and_share():
    distribution = [
        {"language": "Python", "count": 3, "share": 0.75},
        {"language": "Go", "count": 1, "share": 0.25},
    ]

    resultado = compare_with_reference(distribution, reference=["Python", "Go"])

    assert resultado == [
        {"language": "Python", "reference_rank": 1, "collected_rank": 1, "collected_share": 0.75},
        {"language": "Go", "reference_rank": 2, "collected_rank": 2, "collected_share": 0.25},
    ]


def test_compare_with_reference_handles_language_absent_from_collected_data():
    distribution = [{"language": "Python", "count": 1, "share": 1.0}]

    resultado = compare_with_reference(distribution, reference=["Python", "Rust"])

    assert resultado[1] == {
        "language": "Rust",
        "reference_rank": 2,
        "collected_rank": None,
        "collected_share": 0.0,
    }

import numpy as np
import pandas as pd

from src.analysis.correlation import (
    build_normalized_metrics,
    correlation_matrices,
    interpret,
    pairs_above_threshold,
)


def _sample_df():
    return pd.DataFrame(
        {
            "age_days": [100, 200, 300, 400],
            "merged_pull_requests": [0, 100, 0, 50],
            "releases": [5, 5, 5, 5],
            "update_frequency_days": [0, 10, 0, 400],
            "primary_language": ["Python", "Python", "COBOL", "Python"],
            "closed_issues_ratio": [0.5, 0.2, 0.9, None],
        }
    )


def test_build_normalized_metrics_returns_values_between_0_and_1():
    normalizado = build_normalized_metrics(_sample_df())

    for coluna in normalizado.columns:
        valores = normalizado[coluna].dropna()
        assert valores.between(0, 1).all()


def test_build_normalized_metrics_inverts_update_frequency():
    normalizado = build_normalized_metrics(_sample_df())

    # Linha 0 tem o menor update_frequency_days (mais recente) -> deve
    # virar o maior valor normalizado (mais "saudável").
    assert normalizado["update_frequency_days"].idxmax() == 0


def test_build_normalized_metrics_constant_column_is_nan():
    normalizado = build_normalized_metrics(_sample_df())  # releases é constante

    assert normalizado["releases"].isna().all()


def test_correlation_matrices_are_symmetric_with_unit_diagonal():
    normalizado = build_normalized_metrics(_sample_df()).drop(columns=["releases"])
    pearson, spearman = correlation_matrices(normalizado)

    assert np.allclose(pearson.to_numpy(), pearson.to_numpy().T, equal_nan=True)
    assert np.allclose(spearman.to_numpy(), spearman.to_numpy().T, equal_nan=True)
    assert (pearson.to_numpy().diagonal() == 1.0).all()


def test_pairs_above_threshold_filters_and_deduplicates():
    matriz = pd.DataFrame(
        {
            "a": [1.0, 0.9, 0.1],
            "b": [0.9, 1.0, 0.2],
            "c": [0.1, 0.2, 1.0],
        },
        index=["a", "b", "c"],
    )

    pares = pairs_above_threshold(matriz, threshold=0.3)

    assert pares == [("a", "b", 0.9)]


def test_pairs_above_threshold_sorted_by_absolute_value():
    matriz = pd.DataFrame(
        {
            "a": [1.0, 0.4, -0.8],
            "b": [0.4, 1.0, 0.35],
            "c": [-0.8, 0.35, 1.0],
        },
        index=["a", "b", "c"],
    )

    pares = pairs_above_threshold(matriz, threshold=0.3)

    assert [par[:2] for par in pares] == [("a", "c"), ("a", "b"), ("b", "c")]


def test_correlation_matrix_detects_perfect_linear_relationship():
    normalizado = pd.DataFrame(
        {
            "x": [0.1, 0.2, 0.3, 0.4, 0.5],
            "y": [0.2, 0.4, 0.6, 0.8, 1.0],
        }
    )

    pearson, _ = correlation_matrices(normalizado)

    assert abs(pearson.loc["x", "y"] - 1.0) < 1e-9


def test_interpret_reports_direction_and_strength():
    frase = interpret("age_days", "releases", 0.75, 0.7)

    assert "Idade" in frase
    assert "Releases" in frase
    assert "positiva forte" in frase
    assert "r=0.75" in frase
    assert "rho=0.70" in frase


def test_interpret_reports_negative_direction():
    frase = interpret("update_frequency_days", "closed_issues_ratio", -0.6, -0.55)

    assert "negativa moderada" in frase

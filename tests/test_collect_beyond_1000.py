"""
Testa a lógica de descoberta de faixas de stars: (busca binária) sem
bater na API real, mocka count_repositories com uma distribuição de
repositórios por estrela conhecida de antemão.
"""
import pytest

from scripts.experimental import collect_beyond_1000 as mod


def fake_repo_counts_by_star_threshold(threshold: int) -> int:
    """
    Simula uma distribuição de estrelas parecida com a real do GitHub:
    muitos repositórios com poucas estrelas, poucos com muitas,
    decrescente suave (sem platôs), pra dar espaço real de busca binária
    em qualquer sub-faixa.
    """
    return max(0, round(10_000 / max(threshold, 1)))


def fake_count_repositories(search_query: str) -> int:
    if search_query.startswith("stars:>="):
        threshold = int(search_query.removeprefix("stars:>="))
        return fake_repo_counts_by_star_threshold(threshold)

    low_str, high_str = search_query.removeprefix("stars:").split("..")
    low, high = int(low_str), int(high_str)
    return fake_repo_counts_by_star_threshold(low) - fake_repo_counts_by_star_threshold(high + 1)


def test_range_query_formats_unbounded_and_bounded_ranges():
    assert mod.range_query(100, None) == "stars:>=100"
    assert mod.range_query(50, 99) == "stars:50..99"


def test_find_lower_bound_respects_safe_max(monkeypatch):
    monkeypatch.setattr(mod, "count_repositories", fake_count_repositories)

    low = mod.find_lower_bound(upper=None, safe_max=500)

    assert fake_count_repositories(mod.range_query(low, None)) <= 500
    assert fake_count_repositories(mod.range_query(low - 1, None)) > 500


def test_find_star_ranges_covers_total_desired_without_overlap(monkeypatch):
    monkeypatch.setattr(mod, "count_repositories", fake_count_repositories)

    ranges = mod.find_star_ranges(total_desired=1000, safe_max_per_range=500)

    for low, upper in ranges:
        assert fake_count_repositories(mod.range_query(low, upper)) <= 500

    for i in range(1, len(ranges)):
        low_anterior, _ = ranges[i - 1]
        _, upper_atual = ranges[i]
        assert upper_atual == low_anterior - 1

    total_coberto = sum(fake_count_repositories(mod.range_query(low, upper)) for low, upper in ranges)
    assert total_coberto >= 1000


def test_find_star_ranges_raises_instead_of_masking_an_oversized_range(monkeypatch):
    """
    Simula uma faixa densa demais pra ser subdividida dentro do piso de
    estrelas (ex.: muitos repositórios com a mesma contagem baixa de
    estrelas). Nesse caso, usar a faixa do jeito que está reproduziria,
    escondido, o mesmo teto de ~1.000 que o particionamento existe pra
    contornar, deve levantar erro em vez de mascarar isso.
    """
    def fake_count_always_too_dense(search_query: str) -> int:
        return 1000  

    monkeypatch.setattr(mod, "count_repositories", fake_count_always_too_dense)

    with pytest.raises(RuntimeError, match="acima do safe_max_per_range"):
        mod.find_star_ranges(total_desired=2000, safe_max_per_range=10)


def test_find_star_ranges_with_max_stars_starts_below_the_ceiling(monkeypatch):
    monkeypatch.setattr(mod, "count_repositories", fake_count_repositories)

    ranges = mod.find_star_ranges(total_desired=500, safe_max_per_range=500, max_stars=200)

    primeiro_low, primeiro_upper = ranges[0]
    assert primeiro_upper == 200
    assert primeiro_low <= 200


FAKE_REPO = {
    "name": "example-repo",
    "owner": {"login": "example-owner"},
    "stargazerCount": 42,
    "createdAt": "2015-01-01T00:00:00Z",
    "pushedAt": "2024-01-01T00:00:00Z",
    "primaryLanguage": {"name": "Python"},
    "pullRequests": {"totalCount": 10},
    "releases": {"totalCount": 2},
    "closedIssues": {"totalCount": 3},
    "totalIssues": {"totalCount": 4},
}


def test_collect_range_adaptive_grows_and_returns_final_page_size(monkeypatch):
    """
    SUCCESS_STREAK_TO_GROW=3 e PAGE_SIZE_STEP=5 (tuning de produção,
    reaproveitado aqui): depois de 3 páginas bem-sucedidas seguidas, a
    próxima requisição já deve pedir page_size+5.
    """
    requests_made = []

    def fake_run_query(query, variables):
        requests_made.append(variables["first"])
        page_number = len(requests_made)
        has_next = page_number < 4  
        return {
            "search": {
                "pageInfo": {"hasNextPage": has_next, "endCursor": f"cursor-{page_number}"},
                "nodes": [FAKE_REPO],
            }
        }

    monkeypatch.setattr(mod, "run_query", fake_run_query)

    rows, final_page_size = mod.collect_range_adaptive(low=1, upper=10, start_page_size=10)

    assert len(rows) == 4
    assert requests_made == [10, 10, 10, 15]
    assert final_page_size == 15


def test_collect_across_ranges_adaptive_carries_page_size_between_ranges(monkeypatch):
    """
    A 2ª faixa deve começar do page_size final da 1ª (15), não reiniciar
    em `page_size` (10), é o comportamento que substituiu o reset por
    faixa (ver docs/benchmark_pagination.md).
    """
    requests_made = []

    def fake_run_query(query, variables):
        search_query = variables["searchQuery"]
        requests_made.append((search_query, variables["first"]))
        page_number = sum(1 for q, _ in requests_made if q == search_query)
        has_next = page_number < 4
        return {
            "search": {
                "pageInfo": {"hasNextPage": has_next, "endCursor": f"cursor-{page_number}"},
                "nodes": [FAKE_REPO],
            }
        }

    monkeypatch.setattr(mod, "run_query", fake_run_query)

    ranges = [(100, None), (50, 99)]
    mod.collect_across_ranges(ranges, page_size=10, strategy="adaptive")

    segunda_faixa_query = mod.range_query(50, 99)
    primeira_requisicao_segunda_faixa = next(
        first for query, first in requests_made if query == segunda_faixa_query
    )

    assert primeira_requisicao_segunda_faixa == 15  

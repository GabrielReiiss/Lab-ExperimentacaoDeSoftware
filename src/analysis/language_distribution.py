def language_distribution(df) -> list[dict]:
    total = len(df)
    contagem = df["primary_language"].fillna("Sem linguagem").value_counts()

    return [
        {"language": linguagem, "count": int(count), "share": count / total}
        for linguagem, count in contagem.items()
    ]


def compare_with_reference(distribution: list[dict], reference: list[str]) -> list[dict]:
    posicoes = {item["language"]: i + 1 for i, item in enumerate(distribution)}
    shares = {item["language"]: item["share"] for item in distribution}

    return [
        {
            "language": linguagem,
            "reference_rank": i + 1,
            "collected_rank": posicoes.get(linguagem),
            "collected_share": shares.get(linguagem, 0.0),
        }
        for i, linguagem in enumerate(reference)
    ]

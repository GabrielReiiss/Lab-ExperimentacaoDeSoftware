"""
Métrica da RQ01: sistemas populares são maduros/antigos?

Métrica: quantos dias se passaram entre a criação (`createdAt`) do
repositório e hoje. Quanto maior o número, mais antigo/maduro o
repositório.
"""
from datetime import datetime, timezone


def extract_rq01(repo: dict, now: datetime = None) -> int:
    """
    Recebe um node de repositório (precisa ter o campo `createdAt`, no
    formato ISO 8601 retornado pela API) e devolve o número de dias desde
    a criação até `now` (default: agora, em UTC).
    """
    if now is None:
        now = datetime.now(timezone.utc)

    created_at = datetime.fromisoformat(repo["createdAt"].replace("Z", "+00:00"))
    return (now - created_at).days

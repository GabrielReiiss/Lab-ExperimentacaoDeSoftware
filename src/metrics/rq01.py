"""
Métrica da RQ01: idade do repositório em dias, contada a partir do
createdAt.
"""
from datetime import datetime, timezone


def extract_rq01(repo: dict, now: datetime = None) -> int:
    """Dias entre a criação do repositório e now (UTC por padrão)."""
    if now is None:
        now = datetime.now(timezone.utc)

    created_at = datetime.fromisoformat(repo["createdAt"].replace("Z", "+00:00"))
    return (now - created_at).days

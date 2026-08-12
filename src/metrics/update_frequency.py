"""
Métrica da RQ04: sistemas populares são atualizados com frequência?

Métrica: quantos dias se passaram entre o último push (`pushedAt`) do
repositório e hoje. Quanto menor o número, mais recente a atualização.
"""
from datetime import datetime, timezone


def extract_update_frequency(repo: dict, now: datetime = None) -> int:
    """
    Recebe um node de repositório (precisa ter o campo `pushedAt`, no
    formato ISO 8601 retornado pela API) e devolve o número de dias desde
    a última atualização até `now` (default: agora, em UTC).
    """
    if now is None:
        now = datetime.now(timezone.utc)

    pushed_at = datetime.fromisoformat(repo["pushedAt"].replace("Z", "+00:00"))
    return (now - pushed_at).days

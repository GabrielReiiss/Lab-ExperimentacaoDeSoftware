def extract_snapshot_row(node: dict, sprint: str, data_snapshot: str) -> dict | None:
    content = node.get("content") or {}

    if "number" not in content:
        return None

    status = node.get("fieldValueByName")
    assignees = content.get("assignees", {}).get("nodes", [])

    return {
        "sprint": sprint,
        "data_snapshot": data_snapshot,
        "issue_number": content["number"],
        "titulo": content["title"],
        "status": status["name"] if status else None,
        "assignees": ";".join(a["login"] for a in assignees),
        "url": content["url"],
    }

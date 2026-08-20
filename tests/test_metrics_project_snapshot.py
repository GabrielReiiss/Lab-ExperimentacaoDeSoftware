from src.metrics.project_snapshot import extract_snapshot_row


def test_extract_snapshot_row_reads_status_and_assignees():
    node = {
        "fieldValueByName": {"name": "Doing"},
        "content": {
            "number": 25,
            "title": "Primeiro snapshot de fechamento de sprint",
            "url": "https://github.com/GabrielReiiss/Lab-ExperimentacaoDeSoftware/issues/25",
            "assignees": {"nodes": [{"login": "ArthurPanzera13"}]},
        },
    }

    linha = extract_snapshot_row(node, sprint="S02", data_snapshot="2026-08-19")

    assert linha == {
        "sprint": "S02",
        "data_snapshot": "2026-08-19",
        "issue_number": 25,
        "titulo": "Primeiro snapshot de fechamento de sprint",
        "status": "Doing",
        "assignees": "ArthurPanzera13",
        "url": "https://github.com/GabrielReiiss/Lab-ExperimentacaoDeSoftware/issues/25",
    }


def test_extract_snapshot_row_joins_multiple_assignees():
    node = {
        "fieldValueByName": {"name": "Review"},
        "content": {
            "number": 12,
            "title": "Issue com dois responsáveis",
            "url": "https://example.com/12",
            "assignees": {"nodes": [{"login": "a"}, {"login": "b"}]},
        },
    }

    linha = extract_snapshot_row(node, sprint="S02", data_snapshot="2026-08-19")

    assert linha["assignees"] == "a;b"


def test_extract_snapshot_row_ignores_draft_issues():
    node = {
        "fieldValueByName": {"name": "Backlog"},
        "content": {"title": "Draft sem Issue"},
    }

    assert extract_snapshot_row(node, sprint="S02", data_snapshot="2026-08-19") is None


def test_extract_snapshot_row_status_none_when_field_missing():
    node = {
        "fieldValueByName": None,
        "content": {
            "number": 30,
            "title": "Issue sem status definido",
            "url": "https://example.com/30",
            "assignees": {"nodes": []},
        },
    }

    linha = extract_snapshot_row(node, sprint="S02", data_snapshot="2026-08-19")

    assert linha["status"] is None
    assert linha["assignees"] == ""

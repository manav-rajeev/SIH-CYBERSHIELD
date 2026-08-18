from pathlib import Path

from services.event_ingestion_service import load_events_from_file, normalize_event
from services.remediation_service import create_remediation_ticket, simulate_verification


def test_csv_event_ingestion(tmp_path: Path):
    csv_file = tmp_path / "events.csv"
    csv_file.write_text(
        "event_id,timestamp,asset_id,event_type,source,message\n"
        "T-1,2026-08-18T09:00:00Z,WEB-SRV-01,exploit_attempt,198.51.100.1,Demo event\n",
        encoding="utf-8",
    )
    events = load_events_from_file(csv_file)
    assert events[0]["severity"] == "LOW"
    assert events[0]["cve"] == ""


def test_event_validation_requires_core_fields():
    try:
        normalize_event({"event_id": "bad"})
    except ValueError as error:
        assert "missing required fields" in str(error)
    else:
        raise AssertionError("Expected ValueError for incomplete event")


def test_remediation_ticket_and_verification_are_simulated():
    vulnerability = {"id": "VULN-001", "cve": "CVE-2021-44228", "asset_id": "WEB-SRV-01", "status": "OPEN"}
    ticket = create_remediation_ticket(vulnerability, "CRITICAL")
    resolved = simulate_verification(vulnerability)
    assert ticket["summary"].startswith("[SIMULATED]")
    assert resolved["status"] == "RESOLVED"

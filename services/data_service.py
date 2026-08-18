"""JSON data loading and demo scenario helpers."""
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_json(name: str) -> list[dict]:
    try:
        with (DATA_DIR / name).open("r", encoding="utf-8-sig") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_json(name: str, rows: list[dict]) -> None:
    with (DATA_DIR / name).open("w", encoding="utf-8") as file:
        json.dump(rows, file, indent=2)


def load_all() -> tuple[list[dict], list[dict], list[dict]]:
    return load_json("assets.json"), load_json("vulnerabilities.json"), load_json("security_events.json")


def attack_scenario_events() -> list[dict]:
    return [
        {"event_id":"SIM-001","timestamp":"2026-08-18T09:41:00Z","asset_id":"WEB-SRV-01","event_type":"suspicious_http_request","source":"198.51.100.77","cve":"CVE-2021-44228","message":"Repeated suspicious requests in controlled demo.","severity":"HIGH"},
        {"event_id":"SIM-002","timestamp":"2026-08-18T09:42:00Z","asset_id":"WEB-SRV-01","event_type":"exploit_attempt","source":"198.51.100.77","cve":"CVE-2021-44228","message":"Harmless exploit-attempt indicator for SIH demo.","severity":"CRITICAL"},
        {"event_id":"SIM-003","timestamp":"2026-08-18T09:42:30Z","asset_id":"WEB-SRV-01","event_type":"suspicious_process_execution","source":"WEB-SRV-01","cve":"CVE-2021-44228","message":"Simulated suspicious process event.","severity":"HIGH"},
        {"event_id":"SIM-004","timestamp":"2026-08-18T09:43:00Z","asset_id":"WEB-SRV-01","event_type":"unusual_outbound_transfer","source":"WEB-SRV-01","cve":"CVE-2021-44228","message":"Simulated outbound callback indicator.","severity":"HIGH"},
    ]

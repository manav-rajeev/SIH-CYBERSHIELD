"""Controlled CSV/JSON event ingestion helpers for demo data."""
import csv
import json
from pathlib import Path

REQUIRED_EVENT_FIELDS = {"event_id", "timestamp", "asset_id", "event_type", "source", "message"}
OPTIONAL_EVENT_DEFAULTS = {"cve": "", "severity": "LOW"}


def normalize_event(event: dict) -> dict:
    """Validate one event and fill optional fields used by the engines."""
    missing = REQUIRED_EVENT_FIELDS - set(event)
    if missing:
        raise ValueError(f"Event is missing required fields: {sorted(missing)}")
    normalized = {key: str(value) for key, value in event.items()}
    for key, value in OPTIONAL_EVENT_DEFAULTS.items():
        normalized.setdefault(key, value)
    return normalized


def load_events_from_file(path: str | Path) -> list[dict]:
    """Load controlled demo events from a JSON or CSV file."""
    file_path = Path(path)
    if file_path.suffix.lower() == ".json":
        events = json.loads(file_path.read_text(encoding="utf-8"))
    elif file_path.suffix.lower() == ".csv":
        with file_path.open("r", encoding="utf-8", newline="") as file:
            events = list(csv.DictReader(file))
    else:
        raise ValueError("Only .json and .csv event files are supported")
    return [normalize_event(event) for event in events]

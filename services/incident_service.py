"""Incident helpers used by the Streamlit UI and tests."""

VALID_STATUSES = ["New", "Investigating", "Contained", "Remediating", "Resolved", "Reopened"]


def update_incident_status(incident: dict, status: str) -> dict:
    """Return a copy of an incident with a validated status update."""
    if status not in VALID_STATUSES:
        raise ValueError(f"Unsupported incident status: {status}")
    updated = dict(incident)
    updated["status"] = status
    return updated


def append_response_history(incident: dict, actions: list[dict]) -> dict:
    """Attach simulated response actions to an incident record."""
    updated = dict(incident)
    updated["response_history"] = list(updated.get("response_history", [])) + actions
    return updated

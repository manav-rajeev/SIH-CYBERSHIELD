"""Simple rule-based detection for controlled demo events."""

SEVERITY_ORDER = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}

RULES = {
    "failed_login": ("MEDIUM", "Repeated authentication failures"),
    "successful_login_after_failures": ("HIGH", "Successful login after repeated failures"),
    "suspicious_http_request": ("HIGH", "Suspicious HTTP request pattern"),
    "exploit_attempt": ("CRITICAL", "Exploit attempt detected"),
    "suspicious_process_execution": ("HIGH", "Suspicious process execution"),
    "unusual_outbound_transfer": ("HIGH", "Unusual outbound data transfer"),
    "privilege_escalation": ("CRITICAL", "Privilege escalation indicator"),
}


def detect_event(event: dict) -> dict:
    severity, reason = RULES.get(event.get("event_type"), ("LOW", "Informational event"))
    provided = event.get("severity", severity)
    if SEVERITY_ORDER.get(provided, 1) > SEVERITY_ORDER[severity]:
        severity = provided
    detected = dict(event)
    detected["severity"] = severity
    detected["detection_reason"] = reason
    return detected


def detect_events(events: list[dict]) -> list[dict]:
    return [detect_event(event) for event in events]

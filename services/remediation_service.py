"""Simulated remediation and verification workflow helpers."""


def create_remediation_ticket(vulnerability: dict, priority: str) -> dict:
    """Create a safe demo remediation ticket record."""
    return {
        "ticket_id": f"TKT-{vulnerability.get('id', 'UNKNOWN')}",
        "vulnerability_id": vulnerability.get("id"),
        "cve": vulnerability.get("cve"),
        "priority": priority,
        "status": "OPEN",
        "summary": f"[SIMULATED] Remediate {vulnerability.get('cve')} on {vulnerability.get('asset_id')}",
    }


def simulate_verification(vulnerability: dict) -> dict:
    """Simulate a verification scan and mark the vulnerability resolved."""
    updated = dict(vulnerability)
    updated["status"] = "RESOLVED"
    updated["verification_result"] = "[SIMULATED] Verification scan passed; vulnerability marked resolved."
    return updated


def reopen_after_failed_verification(vulnerability: dict) -> dict:
    """Simulate a failed verification scan and keep work open."""
    updated = dict(vulnerability)
    updated["status"] = "OPEN"
    updated["verification_result"] = "[SIMULATED] Verification scan still detects exposure; ticket reopened."
    return updated

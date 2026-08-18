"""Safe simulated response playbooks. No real system changes are performed."""

PLAYBOOKS = {
    "LOW": ["[SIMULATED] Create monitoring alert"],
    "MEDIUM": ["[SIMULATED] Create security ticket", "[SIMULATED] Notify analyst"],
    "HIGH": ["[SIMULATED] Flag affected asset", "[SIMULATED] Block suspicious source", "[SIMULATED] Create remediation ticket"],
    "CRITICAL": ["[SIMULATED] Isolate endpoint", "[SIMULATED] Block suspicious source", "[SIMULATED] Create urgent remediation ticket", "[SIMULATED] Notify security analyst", "[SIMULATED] Schedule verification scan"],
}


def recommended_actions(priority: str) -> list[str]:
    return PLAYBOOKS.get(priority, PLAYBOOKS["LOW"])


def execute_simulated_response(incident: dict) -> list[dict]:
    actions = recommended_actions(incident.get("severity", "LOW"))
    return [{"incident_id": incident.get("incident_id"), "action": action, "result": "SIMULATED_SUCCESS"} for action in actions]

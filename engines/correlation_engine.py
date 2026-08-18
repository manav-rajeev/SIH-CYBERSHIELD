"""Correlates security events to assets and vulnerabilities."""
from engines.risk_engine import calculate_risk
from engines.response_engine import recommended_actions


def correlate_events(assets: list[dict], vulnerabilities: list[dict], events: list[dict]) -> list[dict]:
    asset_by_id = {asset["asset_id"]: asset for asset in assets}
    incidents = []
    for vuln in vulnerabilities:
        asset = asset_by_id.get(vuln.get("asset_id"), {})
        related = [event for event in events if event.get("asset_id") == vuln.get("asset_id") and (not event.get("cve") or event.get("cve") == vuln.get("cve"))]
        risk = calculate_risk(vuln, asset, related)
        if related:
            strongest = sorted(related, key=lambda e: e.get("timestamp", ""))[-1]
            incidents.append({
                "incident_id": f"INC-{len(incidents)+1:03d}",
                "timestamp": strongest.get("timestamp"),
                "asset_id": vuln.get("asset_id"),
                "asset_name": asset.get("name", vuln.get("asset_id")),
                "cve": vuln.get("cve"),
                "source": strongest.get("source"),
                "event_type": strongest.get("event_type"),
                "severity": risk["priority"],
                "risk_score": risk["score"],
                "status": "New",
                "recommended_action": "; ".join(recommended_actions(risk["priority"])),
                "response_history": [],
                "risk_reasons": risk["reasons"],
                "events": related,
            })
    return incidents

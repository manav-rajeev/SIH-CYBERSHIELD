"""Transparent context-aware vulnerability risk scoring."""

DEFAULT_WEIGHTS = {
    "cvss": 35,
    "asset_criticality": 20,
    "internet_exposure": 15,
    "kev": 15,
    "exploit_activity": 10,
    "incident_correlation": 5,
}


def priority_from_score(score: float) -> str:
    if score >= 80:
        return "CRITICAL"
    if score >= 60:
        return "HIGH"
    if score >= 40:
        return "MEDIUM"
    return "LOW"


def calculate_risk(vulnerability: dict, asset: dict, correlated_events=None, weights=None) -> dict:
    """Return score, priority, and human-readable reasons for a vulnerability."""
    weights = weights or DEFAULT_WEIGHTS
    correlated_events = correlated_events or []
    cvss = float(vulnerability.get("cvss", 0))
    criticality = int(asset.get("criticality", 1))
    internet_exposed = bool(asset.get("internet_exposed", False))
    kev = bool(vulnerability.get("kev", False))
    exploit_activity = bool(vulnerability.get("exploit_activity", False)) or any(
        event.get("event_type") == "exploit_attempt" for event in correlated_events
    )
    incident_correlation = len(correlated_events) > 0

    components = {
        "cvss": (cvss / 10) * weights["cvss"],
        "asset_criticality": (criticality / 5) * weights["asset_criticality"],
        "internet_exposure": weights["internet_exposure"] if internet_exposed else 0,
        "kev": weights["kev"] if kev else 0,
        "exploit_activity": weights["exploit_activity"] if exploit_activity else 0,
        "incident_correlation": weights["incident_correlation"] if incident_correlation else 0,
    }
    score = min(100, round(sum(components.values()), 1))
    reasons = []
    if cvss >= 9:
        reasons.append("High CVSS severity")
    elif cvss >= 7:
        reasons.append("Elevated CVSS severity")
    else:
        reasons.append("Lower CVSS severity")
    if criticality >= 4:
        reasons.append("Asset is business-critical")
    if internet_exposed:
        reasons.append("Asset is internet-facing")
    if kev:
        reasons.append("Listed as known exploited / KEV")
    if exploit_activity:
        reasons.append("Exploit activity detected")
    if incident_correlation:
        reasons.append("Active security event correlated to this CVE and asset")
    return {"score": score, "priority": priority_from_score(score), "reasons": reasons, "components": components}

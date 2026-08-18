from engines.risk_engine import calculate_risk, priority_from_score


def test_log4shell_context_becomes_critical():
    vuln = {"cvss": 10.0, "kev": True, "exploit_activity": True}
    asset = {"criticality": 5, "internet_exposed": True}
    risk = calculate_risk(vuln, asset, [{"event_type": "exploit_attempt"}])
    assert risk["score"] == 100
    assert risk["priority"] == "CRITICAL"
    assert "Active security event correlated to this CVE and asset" in risk["reasons"]


def test_priority_thresholds():
    assert priority_from_score(39) == "LOW"
    assert priority_from_score(40) == "MEDIUM"
    assert priority_from_score(60) == "HIGH"
    assert priority_from_score(80) == "CRITICAL"

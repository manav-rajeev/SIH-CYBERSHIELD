from engines.correlation_engine import correlate_events


def test_event_vulnerability_asset_correlation_creates_incident():
    assets = [{"asset_id": "WEB-SRV-01", "name": "Web", "criticality": 5, "internet_exposed": True}]
    vulnerabilities = [{"asset_id": "WEB-SRV-01", "cve": "CVE-2021-44228", "cvss": 10, "kev": True, "exploit_activity": True}]
    events = [{"timestamp": "2026-08-18T09:42:00Z", "asset_id": "WEB-SRV-01", "cve": "CVE-2021-44228", "event_type": "exploit_attempt", "source": "198.51.100.77"}]
    incidents = correlate_events(assets, vulnerabilities, events)
    assert len(incidents) == 1
    assert incidents[0]["severity"] == "CRITICAL"
    assert incidents[0]["cve"] == "CVE-2021-44228"

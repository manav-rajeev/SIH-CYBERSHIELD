"""Model field documentation for JSON data and future database tables."""

ASSET_FIELDS = ["asset_id", "name", "owner", "environment", "criticality", "internet_exposed", "tags"]
VULNERABILITY_FIELDS = ["id", "cve", "title", "asset_id", "cvss", "kev", "exploit_activity", "status", "description", "mitigation"]
EVENT_FIELDS = ["event_id", "timestamp", "asset_id", "event_type", "source", "cve", "message", "severity"]
INCIDENT_FIELDS = ["incident_id", "timestamp", "asset_id", "cve", "source", "event_type", "severity", "risk_score", "status", "recommended_action", "response_history"]

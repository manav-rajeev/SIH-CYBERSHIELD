from engines.detection_engine import detect_event


def test_exploit_attempt_is_critical():
    event = detect_event({"event_type": "exploit_attempt"})
    assert event["severity"] == "CRITICAL"
    assert "Exploit attempt" in event["detection_reason"]

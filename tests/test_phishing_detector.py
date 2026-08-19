from phishing.detector import detect_phishing


def test_safe_url_detection():
    result = detect_phishing("https://example.com")

    assert result["classification"] == "SAFE"
    assert result["score"] < 30
    assert result["url"] == "https://example.com"
    assert isinstance(result["features"], dict)
    assert isinstance(result["reasons"], list)


def test_suspicious_url_detection():
    url = "http://secure-login.example.com/account/verify"

    result = detect_phishing(url)

    assert result["score"] >= 30
    assert result["classification"] in {
        "SUSPICIOUS",
        "HIGH RISK",
        "PHISHING",
    }
    assert result["reasons"]


def test_ip_url_detection():
    result = detect_phishing("http://192.168.1.10/login")

    assert result["score"] >= 40
    assert result["features"]["has_ip_address"] is True


def test_encoded_url_detection():
    result = detect_phishing(
        "https://example.com/login?redirect=%2Fadmin"
    )

    assert result["features"]["has_encoded_characters"] is True
    assert result["score"] > 0


def test_result_contains_all_expected_fields():
    result = detect_phishing("https://example.com")

    expected_fields = {
        "url",
        "score",
        "classification",
        "reasons",
        "features",
    }

    assert expected_fields.issubset(result.keys())
from phishing.risk_scorer import calculate_risk_score
from phishing.url_features import extract_url_features


def test_safe_url_has_low_risk():
    features = extract_url_features("https://example.com")

    result = calculate_risk_score(features)

    assert result["score"] < 30
    assert result["classification"] == "SAFE"


def test_http_url_increases_risk():
    features = extract_url_features("http://example.com")

    result = calculate_risk_score(features)

    assert result["score"] >= 15
    assert "HTTPS" in " ".join(result["reasons"])


def test_ip_based_url_is_high_risk():
    features = extract_url_features(
        "http://192.168.1.10/login"
    )

    result = calculate_risk_score(features)

    assert result["score"] >= 40
    assert "IP address" in " ".join(result["reasons"])


def test_suspicious_url_gets_high_score():
    url = (
        "http://secure-login.example.com/"
        "account/verify/password"
    )

    features = extract_url_features(url)
    result = calculate_risk_score(features)

    assert result["score"] >= 30
    assert result["classification"] in {
        "SUSPICIOUS",
        "HIGH RISK",
        "PHISHING",
    }


def test_score_never_exceeds_100():
    features = {
        "uses_https": False,
        "has_ip_address": True,
        "has_at_symbol": True,
        "has_encoded_characters": True,
        "suspicious_keyword_count": 10,
        "subdomain_count": 10,
        "url_length": 500,
        "query_parameter_count": 10,
        "hyphen_count": 10,
    }

    result = calculate_risk_score(features)

    assert 0 <= result["score"] <= 100
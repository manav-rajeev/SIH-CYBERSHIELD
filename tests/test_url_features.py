from phishing.url_features import extract_url_features


def test_safe_https_url_features():
    features = extract_url_features("https://example.com")

    assert features["uses_https"] is True
    assert features["has_ip_address"] is False
    assert features["has_at_symbol"] is False
    assert features["suspicious_keyword_count"] == 0


def test_suspicious_url_features():
    url = "http://secure-login.example.com/account/verify"

    features = extract_url_features(url)

    assert features["uses_https"] is False
    assert features["subdomain_count"] == 1
    assert features["suspicious_keyword_count"] >= 3


def test_ip_address_detection():
    features = extract_url_features("http://192.168.1.10/login")

    assert features["has_ip_address"] is True


def test_encoded_character_detection():
    features = extract_url_features(
        "https://example.com/login?redirect=%2Fadmin"
    )

    assert features["has_encoded_characters"] is True


def test_at_symbol_detection():
    features = extract_url_features(
        "https://example.com@evil.example/login"
    )

    assert features["has_at_symbol"] is True
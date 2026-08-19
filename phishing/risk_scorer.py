"""Explainable phishing URL risk scoring."""

from typing import Any


def calculate_risk_score(features: dict[str, Any]) -> dict[str, Any]:
    """
    Calculate a 0-100 phishing risk score from extracted URL features.

    Returns:
        score: Numerical risk score from 0 to 100.
        classification: SAFE, SUSPICIOUS, HIGH RISK, or PHISHING.
        reasons: Human-readable explanations for the score.
    """

    score = 0
    reasons = []

    # HTTP instead of HTTPS
    if not features.get("uses_https", False):
        score += 15
        reasons.append("The URL does not use HTTPS")

    # IP address instead of a normal domain
    if features.get("has_ip_address", False):
        score += 25
        reasons.append("The hostname is an IP address")

    # @ can hide the actual destination
    if features.get("has_at_symbol", False):
        score += 20
        reasons.append("The URL contains an @ symbol")

    # URL encoding can be used for obfuscation
    if features.get("has_encoded_characters", False):
        score += 10
        reasons.append("The URL contains encoded characters")

    # Suspicious keywords
    keyword_count = features.get("suspicious_keyword_count", 0)

    if keyword_count >= 4:
        score += 25
        reasons.append(
            f"The URL contains {keyword_count} suspicious keywords"
        )
    elif keyword_count >= 2:
        score += 15
        reasons.append(
            f"The URL contains {keyword_count} suspicious keywords"
        )
    elif keyword_count == 1:
        score += 7
        reasons.append("The URL contains a suspicious keyword")

    # Excessive subdomains
    subdomain_count = features.get("subdomain_count", 0)

    if subdomain_count >= 3:
        score += 15
        reasons.append("The URL contains many subdomains")
    elif subdomain_count == 2:
        score += 8
        reasons.append("The URL contains multiple subdomains")

    # Very long URLs
    url_length = features.get("url_length", 0)

    if url_length > 150:
        score += 15
        reasons.append("The URL is unusually long")
    elif url_length > 100:
        score += 8
        reasons.append("The URL is relatively long")

    # Many query parameters
    parameter_count = features.get("query_parameter_count", 0)

    if parameter_count >= 5:
        score += 10
        reasons.append("The URL contains many query parameters")
    elif parameter_count >= 3:
        score += 5
        reasons.append("The URL contains several query parameters")

    # Many hyphens can be a weak phishing indicator
    hyphen_count = features.get("hyphen_count", 0)

    if hyphen_count >= 4:
        score += 8
        reasons.append("The domain contains many hyphens")

    # Cap score at 100
    score = min(score, 100)

    if score >= 80:
        classification = "PHISHING"
    elif score >= 60:
        classification = "HIGH RISK"
    elif score >= 30:
        classification = "SUSPICIOUS"
    else:
        classification = "SAFE"

    if not reasons:
        reasons.append("No significant phishing indicators detected")

    return {
        "score": score,
        "classification": classification,
        "reasons": reasons,
    }
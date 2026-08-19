"""Combined URL + webpage analysis for CyberShield."""

from typing import Any

from phishing.risk_scorer import calculate_risk_score
from phishing.url_features import extract_url_features
from phishing.website_features import extract_website_features


def analyze_website(url: str, html: str) -> dict[str, Any]:
    """Analyze a URL together with passive webpage features."""

    url_features = extract_url_features(url)

    website_features = extract_website_features(
        html,
        page_url=url,
    )

    risk = calculate_risk_score(url_features)

    website_reasons = []

    if website_features["password_field_count"] > 0:
        website_reasons.append(
            "Page contains a password input field"
        )

    if website_features["iframe_count"] > 0:
        website_reasons.append(
            "Page contains embedded iframe content"
        )

    if website_features["obfuscation_detected"]:
        website_reasons.append(
            "Potential JavaScript obfuscation indicators detected"
        )

    if website_features["meta_refresh"]:
        website_reasons.append(
            "Page contains a meta refresh redirect"
        )

    if website_features["form_action_count"] > 0:
        website_reasons.append(
            "Form submits to an external URL"
        )

    if website_features["suspicious_keyword_count"] > 0:
        website_reasons.append(
            "Page contains suspicious security-related keywords"
        )

    combined_reasons = list(risk["reasons"])

    for reason in website_reasons:
        if reason not in combined_reasons:
            combined_reasons.append(reason)

    return {
        "url": url,
        "score": risk["score"],
        "classification": risk["classification"],
        "reasons": combined_reasons,
        "url_features": url_features,
        "website_features": website_features,
    }
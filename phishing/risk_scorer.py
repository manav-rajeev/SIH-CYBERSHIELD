"""Explainable phishing URL and webpage risk scoring."""

from typing import Any


def calculate_risk_score(
    features: dict[str, Any],
    website_features: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Calculate an explainable phishing risk score from 0 to 100.

    URL indicators are the primary signal.
    Webpage indicators provide supporting evidence.

    When website_features is not supplied, the function preserves
    the original URL-only scoring behavior.
    """

    # ============================================================
    # URL RISK
    # ============================================================

    url_score = 0
    reasons: list[str] = []

    if not features.get("uses_https", False):
        url_score += 15
        reasons.append("The URL does not use HTTPS")

    if features.get("has_ip_address", False):
        url_score += 25
        reasons.append("The hostname is an IP address")

    if features.get("has_at_symbol", False):
        url_score += 20
        reasons.append("The URL contains an @ symbol")

    if features.get("has_encoded_characters", False):
        url_score += 10
        reasons.append("The URL contains encoded characters")

    keyword_count = features.get(
        "suspicious_keyword_count",
        0,
    )

    if keyword_count >= 4:
        url_score += 25
        reasons.append(
            f"The URL contains {keyword_count} suspicious keywords"
        )
    elif keyword_count >= 2:
        url_score += 15
        reasons.append(
            f"The URL contains {keyword_count} suspicious keywords"
        )
    elif keyword_count == 1:
        url_score += 7
        reasons.append(
            "The URL contains a suspicious keyword"
        )

    subdomain_count = features.get(
        "subdomain_count",
        0,
    )

    if subdomain_count >= 3:
        url_score += 15
        reasons.append(
            "The URL contains many subdomains"
        )
    elif subdomain_count == 2:
        url_score += 8
        reasons.append(
            "The URL contains multiple subdomains"
        )

    url_length = features.get(
        "url_length",
        0,
    )

    if url_length > 150:
        url_score += 15
        reasons.append(
            "The URL is unusually long"
        )
    elif url_length > 100:
        url_score += 8
        reasons.append(
            "The URL is relatively long"
        )

    parameter_count = features.get(
        "query_parameter_count",
        0,
    )

    if parameter_count >= 5:
        url_score += 10
        reasons.append(
            "The URL contains many query parameters"
        )
    elif parameter_count >= 3:
        url_score += 5
        reasons.append(
            "The URL contains several query parameters"
        )

    hyphen_count = features.get(
        "hyphen_count",
        0,
    )

    if hyphen_count >= 4:
        url_score += 8
        reasons.append(
            "The domain contains many hyphens"
        )

    url_score = min(url_score, 100)

    # ============================================================
    # WEBSITE RISK
    # ============================================================

    website_score = 0

    if website_features:

        password_fields = website_features.get(
            "password_field_count",
            0,
        )

        if password_fields > 0:
            website_score += 8
            reasons.append(
                "Page contains a password input field"
            )

        form_action_count = website_features.get(
            "form_action_count",
            0,
        )

        if form_action_count > 0:
            website_score += 12
            reasons.append(
                "Form submits to an external URL"
            )

        iframe_count = website_features.get(
            "iframe_count",
            0,
        )

        if iframe_count > 0:
            website_score += 4
            reasons.append(
                "Page contains embedded iframe content"
            )

        if website_features.get(
            "obfuscation_detected",
            False,
        ):
            website_score += 12
            reasons.append(
                "Potential JavaScript obfuscation indicators detected"
            )

        if website_features.get(
            "meta_refresh",
            False,
        ):
            website_score += 6
            reasons.append(
                "Page contains a meta refresh redirect"
            )

        webpage_keyword_count = website_features.get(
            "suspicious_keyword_count",
            0,
        )

        if webpage_keyword_count >= 4:
            website_score += 8
            reasons.append(
                "Page contains multiple suspicious security-related keywords"
            )
        elif webpage_keyword_count > 0:
            website_score += 4
            reasons.append(
                "Page contains suspicious security-related keywords"
            )

        external_script_count = website_features.get(
            "external_script_count",
            0,
        )

        if external_script_count >= 3:
            website_score += 4
            reasons.append(
                "Page loads multiple external scripts"
            )

        hidden_element_count = website_features.get(
            "hidden_element_count",
            0,
        )

        if hidden_element_count >= 5:
            website_score += 4
            reasons.append(
                "Page contains multiple hidden elements"
            )

        eval_count = website_features.get(
            "eval_count",
            0,
        )

        if eval_count > 0:
            website_score += 6
            reasons.append(
                "Page contains JavaScript eval() usage"
            )

    website_score = min(website_score, 20)

    # ============================================================
    # COMBINED SCORE
    # ============================================================

    # URL risk is the primary signal.
    # Website risk is supporting evidence worth 25%.
    combined_score = min(
        100,
        round(
            url_score + (website_score * 0.25)
        ),
    )

    # ============================================================
    # CLASSIFICATION
    # ============================================================

    if combined_score >= 80:
        classification = "PHISHING"
    elif combined_score >= 60:
        classification = "HIGH RISK"
    elif combined_score >= 30:
        classification = "SUSPICIOUS"
    else:
        classification = "SAFE"

    if not reasons:
        reasons.append(
            "No significant phishing indicators detected"
        )

    return {
        "url_score": url_score,
        "website_score": website_score,
        "score": combined_score,
        "classification": classification,
        "reasons": reasons,
    }
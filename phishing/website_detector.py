"""Combined URL + webpage analysis for CyberShield."""

from typing import Any

from phishing.risk_scorer import calculate_risk_score
from phishing.url_features import extract_url_features
from phishing.website_features import extract_website_features


def analyze_website(
    url: str,
    html: str,
) -> dict[str, Any]:
    """Analyze a URL together with passive webpage features."""

    # Extract URL features
    url_features = extract_url_features(url)

    # Extract passive webpage features
    website_features = extract_website_features(
        html,
        page_url=url,
    )

    # Calculate combined URL + webpage risk
    risk = calculate_risk_score(
        url_features,
        website_features,
    )

    return {
        "url": url,
        "url_score": risk["url_score"],
        "website_score": risk["website_score"],
        "score": risk["score"],
        "classification": risk["classification"],
        "reasons": risk["reasons"],
        "url_features": url_features,
        "website_features": website_features,
    }
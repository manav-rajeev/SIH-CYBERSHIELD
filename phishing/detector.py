"""Unified phishing detection pipeline for CyberShield."""

from typing import Any

from phishing.risk_scorer import calculate_risk_score
from phishing.url_features import extract_url_features


def detect_phishing(url: str) -> dict[str, Any]:
    """
    Analyze a URL and return a complete explainable detection result.

    Pipeline:
        URL -> Feature Extraction -> Risk Scoring -> Classification
    """
    features = extract_url_features(url)
    risk = calculate_risk_score(features)

    return {
        "url": url,
        "score": risk["score"],
        "classification": risk["classification"],
        "reasons": risk["reasons"],
        "features": features,
    }
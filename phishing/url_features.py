"""Feature extraction for CyberShield browser URL analysis."""

import ipaddress
import re
from urllib.parse import parse_qs, urlparse


SUSPICIOUS_KEYWORDS = {
    "login",
    "signin",
    "verify",
    "verification",
    "account",
    "secure",
    "security",
    "update",
    "confirm",
    "password",
    "payment",
    "wallet",
    "authenticate",
}


def _is_ip_address(hostname: str) -> bool:
    """Return True when the hostname is an IPv4 or IPv6 address."""
    if not hostname:
        return False

    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        return False


def _count_suspicious_keywords(url: str) -> int:
    """Count suspicious keywords found in the URL."""
    lowered = url.lower()

    return sum(
        1
        for keyword in SUSPICIOUS_KEYWORDS
        if re.search(rf"\b{re.escape(keyword)}\b", lowered)
    )


def extract_url_features(url: str) -> dict:
    """
    Extract explainable URL features.

    This function only extracts features.
    It does not classify the URL as safe or malicious.
    """
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL must be a non-empty string")

    url = url.strip()
    parsed = urlparse(url)

    hostname = parsed.hostname or ""
    domain = hostname.lower()

    path = parsed.path or ""
    query = parsed.query or ""

    subdomain_count = 0

    if domain and not _is_ip_address(domain):
        parts = domain.split(".")

        if len(parts) > 2:
            subdomain_count = len(parts) - 2

    special_characters = sum(
        1
        for character in url
        if character in "@?=&%_"
    )

    return {
        "url": url,
        "scheme": parsed.scheme.lower(),
        "uses_https": parsed.scheme.lower() == "https",
        "url_length": len(url),
        "domain_length": len(domain),
        "path_length": len(path),
        "query_length": len(query),
        "subdomain_count": subdomain_count,
        "dot_count": url.count("."),
        "hyphen_count": url.count("-"),
        "slash_count": url.count("/"),
        "special_character_count": special_characters,
        "has_at_symbol": "@" in url,
        "has_ip_address": _is_ip_address(domain),
        "has_encoded_characters": bool(
            re.search(r"%[0-9a-fA-F]{2}", url)
        ),
        "has_port": parsed.port is not None,
        "query_parameter_count": len(parse_qs(query)),
        "suspicious_keyword_count": _count_suspicious_keywords(url),
    }
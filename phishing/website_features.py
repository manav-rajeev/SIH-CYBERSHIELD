"""Passive webpage feature extraction for CyberShield."""

from __future__ import annotations

import re
from typing import Any


SUSPICIOUS_KEYWORDS = {
    "login",
    "log in",
    "signin",
    "sign in",
    "verify",
    "verification",
    "password",
    "account",
    "security",
    "confirm",
    "urgent",
    "suspended",
    "wallet",
}


def extract_website_features(
    html: str,
    page_url: str = "",
) -> dict[str, Any]:
    """
    Extract passive security indicators from webpage HTML.

    This function does not execute JavaScript or interact with
    external systems. It only analyzes supplied HTML text.
    """

    if not isinstance(html, str):
        html = ""

    html_lower = html.lower()

    # Basic HTML counts
    form_count = len(re.findall(r"<form\b", html_lower))
    password_field_count = len(
        re.findall(
            r'<input[^>]+type\s*=\s*["\']?password',
            html_lower,
        )
    )

    iframe_count = len(re.findall(r"<iframe\b", html_lower))
    script_count = len(re.findall(r"<script\b", html_lower))
    external_script_count = len(
        re.findall(
            r'<script[^>]+src\s*=\s*["\']https?://',
            html_lower,
        )
    )

    link_count = len(re.findall(r"<a\b", html_lower))

    hidden_element_count = len(
        re.findall(
            r'display\s*:\s*none|visibility\s*:\s*hidden|hidden\b',
            html_lower,
        )
    )

    # Potential JavaScript obfuscation indicators.
    eval_count = len(re.findall(r"\beval\s*\(", html_lower))
    encoded_function_count = len(
        re.findall(
            r"(atob\s*\(|fromcharcode\s*\(|unescape\s*\()",
            html_lower,
        )
    )

    # Meta refresh can indicate redirect behavior.
    meta_refresh = bool(
        re.search(
            r'<meta[^>]+http-equiv\s*=\s*["\']?refresh',
            html_lower,
        )
    )

    # Suspicious language appearing in visible/source content.
    suspicious_keyword_count = sum(
        html_lower.count(keyword)
        for keyword in SUSPICIOUS_KEYWORDS
    )

    # Forms posting to another URL/domain.
    form_action_count = len(
        re.findall(
            r'<form[^>]+action\s*=\s*["\']https?://',
            html_lower,
        )
    )

    # Very basic indication of obfuscated JavaScript.
    obfuscation_detected = (
        eval_count > 0
        or encoded_function_count > 0
    )

    return {
        "page_url": page_url,
        "html_length": len(html),
        "form_count": form_count,
        "password_field_count": password_field_count,
        "iframe_count": iframe_count,
        "script_count": script_count,
        "external_script_count": external_script_count,
        "link_count": link_count,
        "hidden_element_count": hidden_element_count,
        "eval_count": eval_count,
        "encoded_function_count": encoded_function_count,
        "meta_refresh": meta_refresh,
        "suspicious_keyword_count": suspicious_keyword_count,
        "form_action_count": form_action_count,
        "obfuscation_detected": obfuscation_detected,
    }
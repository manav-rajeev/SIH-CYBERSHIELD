"""Local API for the CyberShield browser extension prototype."""

from flask import Flask, jsonify, request

from phishing.website_detector import analyze_website

app = Flask(__name__)


@app.post("/analyze")
def analyze_url():
    """Analyze a URL together with optional webpage HTML."""
    data = request.get_json(silent=True) or {}

    url = data.get("url", "")
    html = data.get("html", "")

    if not isinstance(url, str) or not url.strip():
        return jsonify({"error": "URL is required"}), 400

    if not isinstance(html, str):
        html = ""

    try:
        result = analyze_website(
            url.strip(),
            html,
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify(result)


@app.get("/health")
def health():
    """Health check for the extension."""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
    )
from phishing.website_detector import analyze_website


def test_safe_website_analysis():
    html = """
    <html>
        <body>
            <h1>Welcome to Example</h1>
            <p>This is a normal page.</p>
        </body>
    </html>
    """

    result = analyze_website(
        "https://example.com",
        html,
    )

    assert result["classification"] == "SAFE"
    assert result["score"] == 0
    assert result["url"] == "https://example.com"
    assert "url_features" in result
    assert "website_features" in result


def test_suspicious_login_page():
    html = """
    <html>
        <body>
            <h1>Verify your account immediately</h1>

            <form action="https://evil.example/login">
                <input type="text" name="username">
                <input type="password" name="password">
            </form>

            <iframe src="https://example.net/frame"></iframe>

            <script>
                eval("hidden code");
            </script>
        </body>
    </html>
    """

    result = analyze_website(
        "http://secure-login.example.com/account/verify",
        html,
    )

    assert result["score"] >= 40
    assert result["classification"] == "SUSPICIOUS"

    assert result["website_features"]["password_field_count"] == 1
    assert result["website_features"]["iframe_count"] == 1
    assert result["website_features"]["obfuscation_detected"] is True

    assert any(
        "password" in reason.lower()
        for reason in result["reasons"]
    )
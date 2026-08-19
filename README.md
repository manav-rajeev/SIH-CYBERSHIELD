# 🛡️ CyberShield - Automated Cybersecurity Detection, Prioritization & Response

CyberShield is a student-built cybersecurity prototype developed for **Smart India Hackathon (SIH) 2026**.

The project is designed to demonstrate an end-to-end cybersecurity workflow that can detect suspicious activity, analyze risk, prioritize threats, and provide explainable security responses in a controlled environment.

---

## 🚀 Current Focus: AI-Powered Browser Security

CyberShield is being extended with an **AI-powered browser security and phishing detection layer**.

The browser extension analyzes the current webpage using multiple security indicators and produces an explainable risk assessment.

### Current workflow

```text
Current Webpage
      │
      ▼
Browser Extension
      │
      ├───────────────► URL Feature Extraction
      │
      └───────────────► Webpage/HTML Feature Extraction
                              │
                              ▼
                       Risk Analysis Engine
                              │
                              ▼
                    Risk Score + Classification
                              │
                  ┌───────────┼───────────┐
                  ▼           ▼           ▼
                SAFE      SUSPICIOUS    HIGH RISK

🔐 Browser Security Features
1. URL Analysis

CyberShield extracts multiple features from the current URL, including:

HTTPS usage
URL length
Domain length
Subdomain count
Dot count
Hyphen count
Query parameter count
Suspicious keywords
IP address usage
@ symbol usage
Encoded characters
Non-standard ports
URL structure indicators

These features are used by the explainable phishing risk scorer.

2. Webpage / HTML Analysis

CyberShield can also perform passive analysis of webpage HTML.

The current prototype checks for:

Number of forms
Password input fields
Iframes
JavaScript elements
External scripts
Links
Hidden elements
eval() usage
Encoded JavaScript functions
Meta refresh redirects
Suspicious security-related keywords
Forms submitting to external URLs
Potential JavaScript obfuscation

The webpage analysis is passive. JavaScript is not executed by the analyzer and the analyzer does not interact with external systems.

📊 Explainable Risk Scoring

The phishing detection engine produces:

A risk score from 0-100
A classification
Human-readable reasons explaining the result
Extracted URL features
Extracted webpage features

Example:

URL: https://example.com


Score: 0
Classification: SAFE


Reason:
No significant phishing indicators detected.

A suspicious URL may produce a result such as:

URL: http://secure-login.example.com/account/verify


Score: 40
Classification: SUSPICIOUS


Reasons:
- The URL does not use HTTPS
- The URL contains suspicious keywords

The goal is not simply to say "malicious" or "safe", but to explain why the system reached its conclusion.

🌐 Browser Extension

CyberShield includes a Chromium-compatible browser extension prototype.

The extension:

Detects the active webpage.
Collects passive webpage information.
Extracts the current URL.
Sends the analysis request to the local CyberShield API.
Displays the resulting security assessment.
Shows the risk score, classification, reasons, and important features.

The current prototype has been tested with Opera, which supports Chromium extensions.

🔒 Privacy & Safety

CyberShield is designed for controlled security analysis.

The browser content script:

Does not collect passwords.
Does not collect cookies.
Does not collect form values.
Removes user-entered values from copied HTML.
Limits the HTML sent for analysis to prevent excessive data transfer.
Performs passive structural analysis.
Does not execute webpage JavaScript as part of the analyzer.
Does not perform offensive actions.

The current browser API runs locally on:

http://127.0.0.1:5000

This keeps the prototype suitable for a controlled laboratory/demo environment.

🧩 System Architecture
                  ┌─────────────────────┐
                  │   Opera / Browser   │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ CyberShield         │
                  │ Browser Extension   │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Local Flask API     │
                  │ browser_api.py      │
                  └──────────┬──────────┘
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
          ┌─────────────────┐ ┌──────────────────┐
          │ URL Feature     │ │ Website Feature  │
          │ Extraction      │ │ Extraction       │
          └────────┬────────┘ └────────┬─────────┘
                   │                   │
                   └─────────┬─────────┘
                             ▼
                  ┌─────────────────────┐
                  │ Risk Scoring Engine │
                  └──────────┬──────────┘
                             ▼
                  ┌─────────────────────┐
                  │ Explainable Result  │
                  │ Score + Reasons     │
                  └─────────────────────┘
📁 Project Structure
SIH-CYBERSHIELD/
│
├── browser_api.py
│
├── extension/
│   ├── background.js
│   ├── content.js
│   ├── manifest.json
│   ├── popup.css
│   ├── popup.html
│   └── popup.js
│
├── phishing/
│   ├── risk_scorer.py
│   ├── url_features.py
│   ├── website_detector.py
│   └── website_features.py
│
├── engines/
├── services/
├── database/
├── data/
├── ui/
│
├── tests/
│   ├── test_detection.py
│   ├── test_risk_engine.py
│   ├── test_risk_scorer.py
│   ├── test_url_features.py
│   └── test_website_detector.py
│
├── app.py
├── requirements.txt
└── README.md
🧪 Testing

The project uses pytest for automated testing.

Tests cover:

URL feature extraction
Phishing detection
Risk scoring
Website feature extraction
Website detection
Existing CyberShield engines and services

Run the test suite with:

.\.venv\Scripts\python.exe -m pytest -q
▶️ Running the Browser Security Prototype
1. Activate the virtual environment
.\.venv\Scripts\Activate.ps1
2. Install dependencies
pip install -r requirements.txt
3. Start the local browser API
python browser_api.py

The API will run on:

http://127.0.0.1:5000
4. Check the API

Open or request:

http://127.0.0.1:5000/health

Expected response:

{
  "status": "ok"
}
5. Load the browser extension

In Opera:

opera://extensions

Enable:

Developer Mode

Select:

Load unpacked

and choose the project's:

extension/

directory.

🖥️ Existing CyberShield Security Platform

The original CyberShield prototype also contains a broader cybersecurity workflow for:

Security event ingestion
Vulnerability intelligence
Asset context
Event correlation
Context-aware risk scoring
Incident creation
Simulated response
Remediation
Verification

The browser security module extends this platform toward real-time endpoint/browser-side threat detection.

🛣️ Future Development

The current browser security system is a prototype foundation.

Planned future capabilities include:

Phase 6

Improved risk-alert UI and clearer threat explanations.

Phase 7

Combined URL + webpage risk scoring.

Phase 8

Real-time webpage change monitoring.

Phase 9

Security event history and attack/detection logging.

Phase 10

AI-assisted threat classification and explanation.

Phase 11

Historical detection dashboard and threat analytics.

Phase 12

Integration with additional threat intelligence and security data sources.

The long-term goal is to move from simple phishing detection toward an intelligent cybersecurity platform capable of detecting, prioritizing, explaining, and responding to browser-based threats.

⚠️ Prototype Disclaimer

CyberShield is a research and demonstration prototype intended for controlled environments.

It should not currently be treated as a replacement for commercial antivirus, endpoint detection and response (EDR), secure web gateways, or enterprise security products.

The system is designed to assist with security analysis and demonstrate the underlying cybersecurity concepts.


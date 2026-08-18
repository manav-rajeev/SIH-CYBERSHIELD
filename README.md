# CyberShield - SIH 2026 MVP

CyberShield is a student-friendly prototype for **Automated Cybersecurity Detection, Prioritization & Response**.

It combines vulnerability intelligence, security events, and asset context to demonstrate the complete workflow:

```text
Detect -> Correlate -> Prioritize -> Respond -> Remediate -> Verify

Safety limitation: This MVP is designed for a controlled lab/demo environment. It never performs real firewall changes, endpoint isolation, process termination, credential access, persistence, or offensive actions. Every response action is explicitly marked [SIMULATED].

What CyberShield Does
Tracks lab assets, vulnerabilities, and security events.
Scores vulnerabilities using contextual factors instead of CVSS alone.
Explains every risk score using transparent reasons and weighted components.
Detects controlled JSON/CSV demo events using deterministic rules.
Correlates security events with affected assets and related CVEs.
Creates incident records with severity, status, recommended actions, and response history.
Provides safe simulated response playbooks and action logs.
Demonstrates remediation verification by changing vulnerabilities from OPEN to RESOLVED.

Security Event
      |
      v
   Detection
      |
      v
Event + Asset + Vulnerability Correlation
      |
      v
Context-Aware Risk Scoring
      |
      v
Prioritization
      |
      v
Incident Creation
      |
      v
Simulated Response
      |
      v
Remediation
      |
      v
Verification

Architecture
Frontend: Streamlit (app.py) with modular page renderers in ui/.
Business Logic: Explainable engines in engines/.
Services: JSON loading, controlled CSV/JSON ingestion, vulnerability enrichment, incident helpers, and remediation helpers in services/.
Database Extension Point: SQLite helper in database/, designed so PostgreSQL can replace it later.
Sample Data: Local JSON/CSV demo data in data/.
Testing: pytest unit tests in tests/.

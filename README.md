# CyberShield — SIH 2026 MVP

CyberShield is a student-friendly prototype for **Automated Cybersecurity Detection, Prioritization & Response**. It combines vulnerability intelligence, security events, and asset context to demonstrate:

```text
Detect → Correlate → Prioritize → Respond → Remediate → Verify
```

> **Safety limitation:** this MVP is for a controlled lab/demo. It never performs real firewall changes, endpoint isolation, process termination, credential access, persistence, or offensive actions. Every response action is explicitly marked `[SIMULATED]`.

## What CyberShield Does

- Tracks lab assets, vulnerabilities, and security events.
- Scores vulnerabilities using contextual factors instead of CVSS alone.
- Explains every risk score with transparent reasons and weighted components.
- Detects controlled JSON/CSV demo events using deterministic rules.
- Correlates security events with affected assets and related CVEs.
- Creates incident records with severity, status, recommended action, and response history fields.
- Provides safe simulated playbooks and action logs.
- Demonstrates remediation verification by changing vulnerabilities from `OPEN` to `RESOLVED`.

## Architecture

- **Frontend:** Streamlit (`app.py`) with modular page renderers in `ui/`.
- **Business logic:** explainable engines in `engines/`.
- **Services:** JSON loading, controlled CSV/JSON ingestion, vulnerability enrichment, incident helpers, and remediation helpers in `services/`.
- **Database extension point:** SQLite helper in `database/`, designed so PostgreSQL can replace it later.
- **Sample data:** local JSON/CSV demo data in `data/`.
- **Tests:** `pytest` unit tests in `tests/`.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## How to Run

```bash
streamlit run app.py
```

Open the local Streamlit URL shown in the terminal.

## Demo Flow

1. Open **Dashboard** and review the SOC summary cards.
2. Click **Simulate Attack Scenario** in the sidebar.
3. Open **Correlation** to see `CVE-2021-44228 → WEB-SRV-01 → exploit attempt → CRITICAL risk → simulated response`.
4. Open **Incidents** to review incident records and the timeline.
5. Open **Response & Remediation**.
6. Click **Execute Simulated Response** to write safe playbook actions to the action log.
7. Click **Simulate Remediation Verification** to demonstrate `OPEN → RESOLVED`.
8. Optionally upload a controlled CSV/JSON event file using the sidebar ingestion control.

## Risk Calculation

The risk engine normalizes to a 0–100 score using configurable weights:

| Factor | Default Weight |
| --- | ---: |
| CVSS | 35 |
| Asset criticality | 20 |
| Internet exposure | 15 |
| Known exploitation / KEV | 15 |
| Exploit activity | 10 |
| Incident correlation | 5 |

Priority mapping:

```text
0–39    LOW
40–59   MEDIUM
60–79   HIGH
80–100  CRITICAL
```

Each score includes reasons such as high CVSS, business-critical asset, internet exposure, KEV status, exploit activity, and active incident correlation.

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── assets.json
│   ├── security_events.csv
│   ├── security_events.json
│   └── vulnerabilities.json
├── database/
├── engines/
├── services/
├── ui/
└── tests/
```

## Future Improvements

- Import CVE/NVD and CISA KEV feeds.
- Persist session actions, incidents, and tickets in SQLite/PostgreSQL.
- Add MITRE ATT&CK mapping.
- Add optional scikit-learn anomaly detection as a non-mandatory extension.
- Add authentication and role separation for a lab deployment.

## Safety Limitations

- No offensive capability is implemented.
- No real network blocking, endpoint isolation, or system modification occurs.
- Demo events are harmless local records.
- The system is an MVP and does not claim to detect every cyberattack.

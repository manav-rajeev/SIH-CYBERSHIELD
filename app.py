"""CyberShield Streamlit application entry point."""
import tempfile

import streamlit as st

from engines.correlation_engine import correlate_events
from engines.detection_engine import detect_events
from services.data_service import attack_scenario_events, load_all
from services.event_ingestion_service import load_events_from_file
from services.vulnerability_service import enrich_vulnerabilities
from ui.correlation import render_correlation
from ui.dashboard import render_dashboard
from ui.incidents import render_incidents
from ui.response import render_response_remediation
from ui.vulnerabilities import render_vulnerabilities

st.set_page_config(page_title="CyberShield SIH 2026", page_icon="🛡️", layout="wide")
st.markdown(
    """
<style>
.stApp {background:#0b1220;color:#e5e7eb}
[data-testid="stMetric"] {background:#111827;border:1px solid #1f2937;border-radius:12px;padding:1rem}
.stButton>button {border-radius:8px;border:1px solid #38bdf8}
</style>
""",
    unsafe_allow_html=True,
)

if "events" not in st.session_state:
    assets, vulnerabilities, events = load_all()
    st.session_state.events = events
    st.session_state.vulnerabilities = vulnerabilities
    st.session_state.actions = []
else:
    assets, vulnerabilities, _ = load_all()
    vulnerabilities = st.session_state.vulnerabilities

events = detect_events(st.session_state.events)
enriched = enrich_vulnerabilities(assets, vulnerabilities, events)
incidents = correlate_events(assets, vulnerabilities, events)

st.title("🛡️ CyberShield — Detection, Prioritization & Simulated Response")
st.caption("Student MVP for a controlled cybersecurity lab. All response/remediation actions are simulated.")

page = st.sidebar.radio("Navigate", ["Dashboard", "Vulnerabilities", "Correlation", "Incidents", "Response & Remediation"])
if st.sidebar.button("Simulate Attack Scenario"):
    existing = {event["event_id"] for event in st.session_state.events}
    st.session_state.events.extend([event for event in attack_scenario_events() if event["event_id"] not in existing])
    st.sidebar.success("Harmless demo events injected.")
    st.rerun()

uploaded_file = st.sidebar.file_uploader("Ingest demo CSV/JSON events", type=["csv", "json"])
if uploaded_file is not None and st.sidebar.button("Load Uploaded Events"):
    suffix = ".csv" if uploaded_file.name.endswith(".csv") else ".json"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_path = temp_file.name
    new_events = load_events_from_file(temp_path)
    existing = {event["event_id"] for event in st.session_state.events}
    st.session_state.events.extend([event for event in new_events if event["event_id"] not in existing])
    st.sidebar.success(f"Loaded {len(new_events)} controlled demo events.")
    st.rerun()

if page == "Dashboard":
    render_dashboard(assets, vulnerabilities, events, enriched, incidents, st.session_state.actions)
elif page == "Vulnerabilities":
    render_vulnerabilities(enriched)
elif page == "Correlation":
    render_correlation(incidents)
elif page == "Incidents":
    render_incidents(incidents)
elif page == "Response & Remediation":
    render_response_remediation(incidents, vulnerabilities)

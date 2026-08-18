"""Safe response and remediation page."""
import streamlit as st

from engines.response_engine import execute_simulated_response, recommended_actions
from services.remediation_service import create_remediation_ticket, reopen_after_failed_verification, simulate_verification


def render_response_remediation(incidents, vulnerabilities):
    st.subheader("Safe Simulated Playbooks")
    incident_ids = [incident["incident_id"] for incident in incidents]
    selected_incident = st.selectbox("Incident", incident_ids) if incident_ids else None
    if selected_incident:
        incident = next(i for i in incidents if i["incident_id"] == selected_incident)
        st.write("Recommended actions:", recommended_actions(incident["severity"]))
        if st.button("Execute Simulated Response"):
            actions = execute_simulated_response(incident)
            st.session_state.actions.extend(actions)
            st.success("Simulated response executed. No real system changes were made.")

    st.subheader("Remediation Verification")
    open_vulns = [v for v in vulnerabilities if v["status"] == "OPEN"]
    if not open_vulns:
        st.success("All vulnerabilities are resolved in this demo session.")
    else:
        selected_vuln = st.selectbox("Vulnerability to verify", [v["id"] for v in open_vulns])
        vuln = next(v for v in open_vulns if v["id"] == selected_vuln)
        st.write("Remediation ticket preview", create_remediation_ticket(vuln, "CRITICAL"))
        col1, col2 = st.columns(2)
        if col1.button("Simulate Remediation Verification"):
            st.session_state.vulnerabilities = [simulate_verification(v) if v["id"] == selected_vuln else v for v in vulnerabilities]
            st.success("OPEN â†’ RESOLVED using simulated verification.")
            st.rerun()
        if col2.button("Simulate Failed Verification"):
            st.session_state.vulnerabilities = [reopen_after_failed_verification(v) if v["id"] == selected_vuln else v for v in vulnerabilities]
            st.warning("Verification failed in simulation; vulnerability remains OPEN / Reopened.")
            st.rerun()
    st.write("Action log", st.session_state.actions)

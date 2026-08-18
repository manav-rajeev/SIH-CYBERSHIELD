"""Dashboard page for the CyberShield Streamlit app."""
import pandas as pd
import streamlit as st


def render_dashboard(assets, vulnerabilities, events, enriched_vulnerabilities, incidents, actions):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Assets Monitored", len(assets))
    c2.metric("Open Vulnerabilities", sum(v["status"] == "OPEN" for v in vulnerabilities))
    c3.metric("Active Incidents", len([incident for incident in incidents if incident["status"] != "Resolved"]))
    c4.metric("Critical Risks", len([v for v in enriched_vulnerabilities if v["priority"] == "CRITICAL" and v["status"] == "OPEN"]))

    st.subheader("Workflow: Detect â†’ Correlate â†’ Prioritize â†’ Respond â†’ Remediate â†’ Verify")
    st.dataframe(
        pd.DataFrame(enriched_vulnerabilities)[
            ["cve", "asset", "cvss", "kev", "internet_exposed", "asset_criticality", "risk_score", "priority", "status"]
        ],
        use_container_width=True,
    )
    st.subheader("Recent Security Events")
    st.dataframe(pd.DataFrame(events).tail(8), use_container_width=True)
    st.subheader("Recent Automated Actions")
    st.write(actions[-10:] or "No simulated actions executed yet.")

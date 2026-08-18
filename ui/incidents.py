"""Incident management page."""
import pandas as pd
import streamlit as st


def render_incidents(incidents):
    st.subheader("Incident Management")
    if not incidents:
        st.info("No correlated incidents yet.")
        return
    st.dataframe(
        pd.DataFrame(incidents).drop(columns=["events", "risk_reasons", "response_history"]),
        use_container_width=True,
    )
    st.subheader("Incident Timeline")
    for incident in sorted(incidents, key=lambda row: row.get("timestamp", "")):
        st.markdown(f"- `{incident['timestamp']}` **{incident['severity']}** {incident['asset_id']} {incident['event_type']} â†’ {incident['cve']}")

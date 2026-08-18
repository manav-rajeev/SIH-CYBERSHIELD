"""Correlation page showing Vulnerability â†’ Asset â†’ Event â†’ Risk â†’ Response."""
import pandas as pd
import streamlit as st


def render_correlation(incidents):
    st.subheader("Correlation: Vulnerability â†’ Asset â†’ Event â†’ Risk â†’ Recommended Response")
    if not incidents:
        st.info("No correlated incidents yet. Use the sidebar demo button to inject controlled events.")
        return
    for incident in incidents:
        expanded = incident["severity"] == "CRITICAL"
        label = f"{incident['severity']} | {incident['asset_id']} | {incident['cve']} | Risk {incident['risk_score']}"
        with st.expander(label, expanded=expanded):
            st.markdown(
                f"**Vulnerability:** {incident['cve']}  â†’ **Asset:** {incident['asset_name']}  â†’ "
                f"**Event:** {incident['event_type']}  â†’ **Risk:** {incident['risk_score']}  â†’ "
                f"**Response:** {incident['recommended_action']}"
            )
            st.write("Risk reasons:", incident["risk_reasons"])
            st.dataframe(pd.DataFrame(incident["events"]), use_container_width=True)

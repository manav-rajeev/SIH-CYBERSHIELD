"""Vulnerability management page."""
import pandas as pd
import streamlit as st


def render_vulnerabilities(enriched_vulnerabilities):
    st.subheader("Vulnerability Management")
    query = st.text_input("Search CVE / asset / title")
    priority = st.selectbox("Priority filter", ["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"])
    status = st.selectbox("Status filter", ["ALL", "OPEN", "RESOLVED"])

    df = pd.DataFrame(enriched_vulnerabilities)
    if query:
        df = df[df.apply(lambda row: query.lower() in " ".join(map(str, row.values)).lower(), axis=1)]
    if priority != "ALL":
        df = df[df["priority"] == priority]
    if status != "ALL":
        df = df[df["status"] == status]

    st.dataframe(
        df[["cve", "title", "asset", "cvss", "kev", "internet_exposed", "asset_criticality", "exploit_activity", "risk_score", "priority", "status"]],
        use_container_width=True,
    )
    selected = st.selectbox("View vulnerability details", [v["id"] for v in enriched_vulnerabilities])
    detail = next(v for v in enriched_vulnerabilities if v["id"] == selected)
    st.json(
        {
            "CVE": detail["cve"],
            "Risk Score": detail["risk_score"],
            "Priority": detail["priority"],
            "Reasons": detail["risk_reasons"],
            "Mitigation": detail["mitigation"],
        }
    )

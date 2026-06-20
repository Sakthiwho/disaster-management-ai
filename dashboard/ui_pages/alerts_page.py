import sys
import os
import streamlit as st
import pandas as pd

# Allow access to project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from database.db_manager import get_alerts


# ----------------------------------------------------
# ALERT PAGE
# ----------------------------------------------------

def show_alerts():

    st.title("🚨 Disaster Alert Center")

    alerts = get_alerts()

    if not alerts:
        st.info("No disaster alerts detected yet.")
        return

    df = pd.DataFrame(alerts)

    # ------------------------------------------------
    # ALERT STATS
    # ------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Alerts", len(df))

    col2.metric(
        "High Risk Alerts",
        len(df[df["severity"].isin(["CRITICAL", "HIGH"])])
    )

    col3.metric(
        "Moderate Alerts",
        len(df[df["severity"] == "MEDIUM"])
    )

    st.divider()

    # ------------------------------------------------
    # FILTER
    # ------------------------------------------------

    disaster_filter = st.selectbox(
        "Filter by Disaster Type",
        ["All"] + list(df["disaster_type"].unique())
    )

    if disaster_filter != "All":
        df = df[df["disaster_type"] == disaster_filter]

    st.subheader("⚠️ Live Disaster Alerts")

    latest_alerts = df.head(20)

    for _, row in latest_alerts.iterrows():

        message = f"{row['disaster_type']} detected in {row['country']}"

        severity = row["severity"]

        if severity in ["CRITICAL", "HIGH"]:

            st.error(f"🚨 {message}")

        elif severity == "MEDIUM":

            st.warning(f"⚠️ {message}")

        else:

            st.info(message)

    st.divider()

    # ------------------------------------------------
    # ALERT TABLE
    # ------------------------------------------------

    st.subheader("📋 Alert History")

    st.dataframe(
        df[
            [
                "disaster_type",
                "country",
                "severity",
                "latitude",
                "longitude"
            ]
        ],
        width="stretch"
    )
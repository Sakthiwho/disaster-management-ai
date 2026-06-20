import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

from database.db_manager import get_alerts, get_broadcasts


# -----------------------------
# LOAD MAP DATA
# -----------------------------

@st.cache_data
def load_map_data():
    data = pd.read_csv("datasets/clean_alerts_dataset.csv")
    return data.sample(500, random_state=42)


# -----------------------------
# DASHBOARD
# -----------------------------

def show_dashboard():

    st.title("🌍 AI Disaster Monitoring Dashboard")
    st.markdown("""
<style>

.alert-banner {
    width: 100%;
    overflow: hidden;
    background: linear-gradient(90deg,#8b0000,#ff0000);
    color: white;
    padding: 10px 0;
    font-weight: 600;
    border-radius: 6px;
    margin-bottom: 20px;
}

.alert-text {
    display: inline-block;
    white-space: nowrap;
    padding-left: 100%;
    animation: alert-scroll 25s linear infinite;
}

@keyframes alert-scroll {
    0% { transform: translateX(0%); }
    100% { transform: translateX(-100%); }
}

</style>

<div class="alert-banner">
<div class="alert-text">
🚨 CYCLONE WARNING IN BAY OF BENGAL &nbsp;&nbsp;&nbsp;
🌊 FLOOD RISK RISING IN SOUTHEAST ASIA &nbsp;&nbsp;&nbsp;
🔥 WILDFIRE ALERT IN CALIFORNIA &nbsp;&nbsp;&nbsp;
🌍 EARTHQUAKE ACTIVITY DETECTED IN PACIFIC RING OF FIRE &nbsp;&nbsp;&nbsp;
⚠️ DROUGHT CONDITIONS WORSENING IN AFRICA
</div>
</div>
""", unsafe_allow_html=True)

    alerts = get_alerts()

    if not alerts:
        st.info("No disaster alerts yet. Run the simulation to generate alerts.")
        return

    df = pd.DataFrame(alerts)

    # -----------------------------
    # METRICS
    # -----------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric("🚨 Active Alerts", len(df))
    col2.metric("🌪 Disaster Types", df["disaster_type"].nunique())
    col3.metric("🌎 Countries Affected", df["country"].nunique())

    st.divider()

    # -----------------------------
    # GLOBAL DISASTER MAP
    # -----------------------------

    st.subheader("🗺 Live Global Disaster Map")

    data = load_map_data()

    m = folium.Map(
        location=[20, 0],
        zoom_start=2,
        tiles="cartodb dark_matter"
    )

    for _, row in data.iterrows():

        lat = row.get("latitude")
        lon = row.get("longitude")

        if pd.isna(lat) or pd.isna(lon):
            continue

        color = "orange"

        if row.get("alert_level") == "Red":
            color = "red"

        elif row.get("alert_level") == "Green":
            color = "green"

        folium.CircleMarker(
            location=[lat, lon],
            radius=4,
            color=color,
            fill=True,
            fill_opacity=0.7
        ).add_to(m)

    st_folium(m, height=600)

    st.divider()

    # -----------------------------
    # EMERGENCY BROADCASTS
    # -----------------------------

    st.subheader("📢 Emergency Broadcasts")

    broadcasts = get_broadcasts()

    if not broadcasts:
        st.info("No emergency broadcasts.")
    else:
        for b in broadcasts:
            st.warning(f"📢 {b['message']} | {b['timestamp']}")

    st.divider()

    # -----------------------------
    # LATEST ALERTS
    # -----------------------------

    st.subheader("🚨 Latest Disaster Alerts")

    latest = df.head(10)

    for _, row in latest.iterrows():

        message = f"{row['disaster_type']} detected in {row['country']}"
        severity = row["severity"]

        if severity in ["CRITICAL", "HIGH"]:
            st.error(f"🚨 {message}")

        elif severity == "MEDIUM":
            st.warning(f"⚠️ {message}")

        else:
            st.info(message)

    st.divider()

    # -----------------------------
    # AI AGENT ACTIVITY
    # -----------------------------

    st.subheader("🤖 AI Agent Activity")

    st.info("🌦 Weather Agent → Monitoring weather conditions")
    st.info("🔮 Prediction Agent → Running ML prediction model")
    st.info("📊 Assessment Agent → Evaluating disaster severity")
    st.info("🚑 Resource Agent → Allocating emergency resources")
    st.info("📡 Communication Agent → Generating alerts")
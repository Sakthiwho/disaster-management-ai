import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

# Allow project imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from database.db_manager import get_connection, update_help_status


def show_admin_help_requests():

    st.title("🚨 Rescue Command Center")

    # -----------------------------
    # FETCH HELP REQUESTS
    # -----------------------------

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, latitude, longitude, message, image_path, status, timestamp
        FROM help_requests
        ORDER BY timestamp DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        st.info("No help requests yet.")
        return

    data = []

    for r in rows:
        data.append({
            "ID": r[0],
            "Latitude": r[1],
            "Longitude": r[2],
            "Message": r[3],
            "Image": r[4],
            "Status": r[5],
            "Time": r[6]
        })

    df = pd.DataFrame(data)

    # -----------------------------
    # RESCUE METRICS
    # -----------------------------

    total_requests = len(df)
    pending = len(df[df["Status"] == "PENDING"])
    dispatched = len(df[df["Status"] == "RESCUE SENT"])
    resolved = len(df[df["Status"] == "RESOLVED"])

    st.subheader("🚑 Rescue Operations Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Requests", total_requests)
    col2.metric("Pending", pending)
    col3.metric("Rescue Sent", dispatched)
    col4.metric("Resolved", resolved)

    st.divider()

    # -----------------------------
    # HELP REQUEST TABLE
    # -----------------------------

    st.subheader("📋 Help Request Table")
    st.dataframe(df, width="stretch")

    st.divider()

    # -----------------------------
    # RESCUE ACTIVITY LOG
    # -----------------------------

    if "activity_log" not in st.session_state:
        st.session_state.activity_log = []

    st.subheader("📡 Rescue Activity Log")

    for log in reversed(st.session_state.activity_log):
        st.write(log)

    st.divider()

    # -----------------------------
    # HELP REQUEST DETAILS
    # -----------------------------

    st.subheader("📍 Help Request Details")

    for r in data:

        request_id = r["ID"]

        st.divider()

        st.write("🆔 Request ID:", request_id)
        st.write("📍 Location:", r["Latitude"], r["Longitude"])
        st.write("💬 Message:", r["Message"])
        st.write("⏱ Time:", r["Time"])

        status = r["Status"]

        if status == "PENDING":
            st.warning("Status: PENDING")

        elif status == "RESCUE SENT":
            st.info("Status: RESCUE TEAM DISPATCHED")

        elif status == "RESOLVED":
            st.success("Status: RESOLVED")

        # -----------------------------
        # DISPLAY IMAGE SAFELY
        # -----------------------------

        image_path = r["Image"]

        if image_path:

            if os.path.exists(image_path):
                st.image(image_path, width=300)

            else:
                st.warning("📷 Image not available")

        col1, col2 = st.columns(2)

        # -----------------------------
        # DISPATCH RESCUE
        # -----------------------------

        if col1.button("🚑 Dispatch Rescue Team", key=f"dispatch_{request_id}"):

            update_help_status(request_id, "RESCUE SENT")

            log = (
                f"[{datetime.now().strftime('%H:%M:%S')}] "
                f"🚑 Rescue team dispatched → Request #{request_id}"
            )

            st.session_state.activity_log.append(log)

            st.success("Rescue team dispatched")
            st.rerun()

        # -----------------------------
        # MARK RESOLVED
        # -----------------------------

        if col2.button("✅ Mark Resolved", key=f"resolve_{request_id}"):

            update_help_status(request_id, "RESOLVED")

            log = (
                f"[{datetime.now().strftime('%H:%M:%S')}] "
                f"✅ Request #{request_id} resolved"
            )

            st.session_state.activity_log.append(log)

            st.success("Request marked as resolved")
            st.rerun()
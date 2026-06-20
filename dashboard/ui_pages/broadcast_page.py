import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from database.db_manager import store_broadcast


def show_broadcast_page():

    st.title("📢 Send Emergency Broadcast")

    message = st.text_area("Emergency Message")

    if st.button("Send Broadcast"):

        if message.strip() == "":
            st.error("Message cannot be empty")
            return

        store_broadcast(message)

        st.success("Broadcast sent successfully.")
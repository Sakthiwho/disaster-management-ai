import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import os
from database.db_manager import store_help_request


def show_help_page():

    st.title("🆘 Emergency Help Request")

    st.warning("If you are in danger, request rescue assistance below.")

    latitude = st.number_input("📍 Your Latitude", format="%.6f")
    longitude = st.number_input("📍 Your Longitude", format="%.6f")

    message = st.text_area("💬 Describe the situation")

    image = st.file_uploader("📷 Upload Photo of Damage", type=["jpg","png","jpeg"])

    if st.button("🚨 I NEED HELP"):

        image_path = None

        if image:

            os.makedirs("uploads", exist_ok=True)

            image_path = os.path.join("uploads", image.name)

            with open(image_path, "wb") as f:
                f.write(image.getbuffer())

        store_help_request(latitude, longitude, message, image_path)

        st.success("Help request sent. Rescue teams have been notified.")
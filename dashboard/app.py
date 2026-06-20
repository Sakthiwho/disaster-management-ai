import streamlit as st
import sys
import os

# allow project imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.db_manager import verify_user

# PUBLIC PAGES
from ui_pages.dashboard_page import show_dashboard
from ui_pages.alerts_page import show_alerts
from ui_pages.help_page import show_help_page

# ADMIN PAGES
from ui_pages.analytics_page import show_analytics
from ui_pages.simulation_page import show_simulation
from ui_pages.resources_page import show_resources
from ui_pages.admin_help_requests import show_admin_help_requests
from ui_pages.broadcast_page import show_broadcast_page



# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="AI Disaster Monitoring System",
    layout="wide"
)

# ----------------------------------------------------
# COMMAND CENTER UI THEME
# ----------------------------------------------------

st.markdown("""
<style>

/* GLOBAL BACKGROUND */
.stApp {
    background: linear-gradient(180deg,#0b0f1a,#0e1424);
    color: #e6edf3;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #0d1321;
    border-right: 1px solid #1f2a44;
}

/* TITLES */
h1, h2, h3 {
    color: #ff4b4b;
    letter-spacing: 1px;
}

/* METRIC CARDS */
[data-testid="stMetric"] {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 12px;
    padding: 12px;
    box-shadow: 0 0 12px rgba(255,75,75,0.25);
}

/* BUTTONS */
.stButton > button {
    background: linear-gradient(90deg,#ff4b4b,#ff784b);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.4rem 1rem;
    font-weight: 600;
}

.stButton > button:hover {
    box-shadow: 0 0 10px #ff4b4b;
}

/* DATA TABLE */
[data-testid="stDataFrame"] {
    background: #0f172a;
    border-radius: 10px;
    border: 1px solid #1f2937;
}

/* DIVIDER */
hr {
    border: none;
    border-top: 1px solid #1f2a44;
}

</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------
# SESSION STATE
# ----------------------------------------------------

if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False


# ----------------------------------------------------
# SIDEBAR PORTAL SWITCH
# ----------------------------------------------------

st.sidebar.markdown("🌍 Disaster Monitoring System")

mode = st.sidebar.radio(
    "Select Portal",
    [
        "Public Portal",
        "Admin Portal"
    ]
)


# ----------------------------------------------------
# PUBLIC PORTAL
# ----------------------------------------------------

if mode == "Public Portal":

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Alerts",
            "Request Help"
        ]
    )

    if page == "Dashboard":
        show_dashboard()

    elif page == "Alerts":
        show_alerts()

    elif page == "Request Help":
        show_help_page()


# ----------------------------------------------------
# ADMIN PORTAL
# ----------------------------------------------------

else:

    if not st.session_state.admin_logged:

        st.title("🔐 Admin Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            user = verify_user(username, password)

            if user:
                st.session_state.admin_logged = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

    else:

        st.sidebar.success("Admin Logged In")

        page = st.sidebar.radio(
            "Admin Navigation",
            [
                "Analytics",
                "Simulation",
                "Resources",
                "Help Requests",
                "Broadcasts"
                
            ]
        )

        if page == "Analytics":
            show_analytics()

        elif page == "Simulation":
            show_simulation()

        elif page == "Resources":
            show_resources()

        elif page == "Help Requests":
            show_admin_help_requests()
        
        elif page == "Broadcasts":
            show_broadcast_page()

        if st.sidebar.button("Logout"):
            st.session_state.admin_logged = False
            st.rerun()
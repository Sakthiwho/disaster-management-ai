import streamlit as st
import pandas as pd


# ----------------------------------------------------
# DATA LOADERS
# ----------------------------------------------------

@st.cache_data
def load_hospitals():
    return pd.read_csv("datasets/hospital.csv")


@st.cache_data
def load_shelters():
    return pd.read_csv("datasets/shelter.csv")


@st.cache_data
def load_transport():
    return pd.read_csv("datasets/transport.csv")


@st.cache_data
def load_warehouses():
    return pd.read_csv("datasets/warehouse.csv")


# ----------------------------------------------------
# RESOURCE PAGE
# ----------------------------------------------------

def show_resources():

    st.title("🚑 Disaster Response Resources")

    hospitals = load_hospitals()
    shelters = load_shelters()
    transport = load_transport()
    warehouses = load_warehouses()

    # ----------------------------------------------------
    # RESOURCE METRICS
    # ----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🏥 Hospitals", len(hospitals))
    col2.metric("🏫 Shelters", len(shelters))
    col3.metric("🚚 Transport Routes", len(transport))
    col4.metric("📦 Warehouses", len(warehouses))

    st.divider()

    # ----------------------------------------------------
    # TABS FOR EACH RESOURCE
    # ----------------------------------------------------

    tab1, tab2, tab3, tab4 = st.tabs(
        ["🏥 Hospitals", "🏫 Shelters", "🚚 Transport", "📦 Warehouses"]
    )

    # -----------------------------
    # HOSPITALS
    # -----------------------------

    with tab1:

        st.subheader("🏥 Available Hospitals")

        st.dataframe(hospitals, width="stretch")

    # -----------------------------
    # SHELTERS
    # -----------------------------

    with tab2:

        st.subheader("🏫 Relief Shelters")

        st.dataframe(shelters, width="stretch")

    # -----------------------------
    # TRANSPORT
    # -----------------------------

    with tab3:

        st.subheader("🚚 Emergency Transport Routes")

        st.dataframe(transport, width="stretch")

    # -----------------------------
    # WAREHOUSES
    # -----------------------------

    with tab4:

        st.subheader("📦 Supply Warehouses")

        st.dataframe(warehouses, width="stretch")
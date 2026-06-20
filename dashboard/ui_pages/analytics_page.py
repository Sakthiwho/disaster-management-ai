import streamlit as st
import pandas as pd
import plotly.express as px


# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------

@st.cache_data
def load_disasters():
    return pd.read_csv("datasets/clean_disaster_dataset.csv")


# ----------------------------------------------------
# ANALYTICS PAGE
# ----------------------------------------------------

def show_analytics():

    st.title("📊 Disaster Intelligence & Analytics")

    disasters = load_disasters()

    disaster_sample = disasters.head(5000)

    # ---------------------------------------------
    # KEY METRICS
    # ---------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Disasters", len(disaster_sample))

    col2.metric(
        "Total Deaths",
        int(disaster_sample["total_deaths"].sum())
    )

    col3.metric(
        "People Affected",
        int(disaster_sample["total_affected"].sum())
    )

    st.divider()

    # ---------------------------------------------
    # MOST COMMON DISASTERS
    # ---------------------------------------------

    st.subheader("⚠️ Most Common Disaster Types")

    disaster_counts = disaster_sample["disaster_type"].value_counts().head(10)

    fig = px.bar(
        disaster_counts,
        x=disaster_counts.index,
        y=disaster_counts.values,
        labels={"x": "Disaster Type", "y": "Occurrences"},
        title="Most Frequent Disasters"
    )

    st.plotly_chart(fig, width="stretch")

    st.divider()

    # ---------------------------------------------
    # MOST AFFECTED COUNTRIES
    # ---------------------------------------------

    st.subheader("🌍 Most Affected Countries")

    country_counts = disaster_sample["Country"].value_counts().head(10)

    fig2 = px.bar(
        country_counts,
        x=country_counts.index,
        y=country_counts.values,
        labels={"x": "Country", "y": "Number of Disasters"},
        title="Countries with Most Disasters"
    )

    st.plotly_chart(fig2, width="stretch")

    st.divider()

    # ---------------------------------------------
    # SEVERITY ANALYSIS
    # ---------------------------------------------

    st.subheader("📉 Disaster Severity Analysis")

    fig3 = px.scatter(
        disaster_sample,
        x="total_affected",
        y="total_deaths",
        color="disaster_type",
        title="Disaster Impact Distribution"
    )

    st.plotly_chart(fig3, width="stretch")

    st.divider()

    # ---------------------------------------------
    # RAW DATA VIEW
    # ---------------------------------------------

    st.subheader("📋 Disaster Dataset Preview")

    st.dataframe(disaster_sample.head(200), width="stretch")
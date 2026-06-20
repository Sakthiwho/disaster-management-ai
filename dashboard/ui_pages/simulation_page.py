import sys
import os
import streamlit as st
import time

# Allow imports from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.agent_pipeline import AgentPipeline


def show_simulation():

    st.title("🚨 AI Disaster Response Command Center")

    st.markdown("Run the agentic AI pipeline to detect disasters and deploy resources.")

    console = st.empty()

    if st.button("Run AI Disaster Detection"):

        pipeline = AgentPipeline()

        logs = []

        # --------------------------------------------------
        # AGENT EXECUTION LOGS
        # --------------------------------------------------

        logs.append("🌦 Weather Agent → Monitoring environmental signals")
        console.code("\n".join(logs))
        time.sleep(1)

        logs.append("🔮 Prediction Agent → Running ML disaster prediction")
        console.code("\n".join(logs))
        time.sleep(1)

        logs.append("📊 Assessment Agent → Evaluating disaster severity")
        console.code("\n".join(logs))
        time.sleep(1)

        logs.append("🚑 Resource Agent → Allocating emergency resources")
        console.code("\n".join(logs))
        time.sleep(1)

        logs.append("📡 Communication Agent → Generating disaster alert")
        console.code("\n".join(logs))
        time.sleep(1)

        # --------------------------------------------------
        # RUN PIPELINE
        # --------------------------------------------------

        result = pipeline.run_pipeline()

        logs.append("✅ AI Pipeline Completed")
        console.code("\n".join(logs))

        st.divider()

        # --------------------------------------------------
        # AI DECISION OUTPUT
        # --------------------------------------------------

        st.subheader("🧠 AI Decision Output")

        col1, col2, col3 = st.columns(3)

        col1.metric("Disaster Type", result["disaster_type"])
        col2.metric("Country", result["country"])
        col3.metric("Severity", result["severity"])

        if "weather_risk" in result:
            st.write("Weather Risk:", result["weather_risk"])

        if "prediction" in result:
            st.write("Prediction Result:", result["prediction"])

        st.divider()

        # --------------------------------------------------
        # RESOURCE DEPLOYMENT
        # --------------------------------------------------

        st.subheader("🚑 Resource Allocation")

        resources = result["resources"]

        if isinstance(resources, dict):

            st.write("Hospital:", resources.get("hospital"))
            st.write("Shelter:", resources.get("shelter"))
            st.write("Warehouse:", resources.get("warehouse"))
            st.write("Transport Route:", resources.get("transport_route"))

            st.info(resources.get("message"))

        st.divider()

        # --------------------------------------------------
        # REAL AGENT ACTIVITY PANEL
        # --------------------------------------------------

        st.subheader("🤖 Agent Activity Log")

        if "weather_risk" in result:
            st.success(f"Weather Agent → Risk Level: {result['weather_risk']}")

        if "prediction" in result:
            st.success(f"Prediction Agent → Predicted Severity: {result['prediction']}")

        st.success(f"Assessment Agent → Disaster Level: {result['severity']}")

        if resources.get("hospital"):
            st.success(f"Resource Agent → Hospital deployed: {resources['hospital']}")

        if resources.get("shelter"):
            st.success(f"Resource Agent → Shelter activated: {resources['shelter']}")

        if resources.get("warehouse"):
            st.success(f"Resource Agent → Warehouse supplies sent: {resources['warehouse']}")

        st.success("Communication Agent → Alert issued to disaster monitoring system")
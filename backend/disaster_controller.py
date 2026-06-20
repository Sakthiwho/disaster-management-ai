import pandas as pd
import time

from agents.weather_agent import WeatherAgent
from agents.prediction_agent import PredictionAgent
from agents.alert_agent import AlertAgent
from agents.assessment_agent import AssessmentAgent
from agents.resource_agent import ResourceAgent
from agents.communication_agent import CommunicationAgent


class DisasterController:

    def __init__(self):

        # Initialize agents
        self.weather_agent = WeatherAgent()
        self.prediction_agent = PredictionAgent()
        self.alert_agent = AlertAgent()
        self.assessment_agent = AssessmentAgent()
        self.resource_agent = ResourceAgent()
        self.communication_agent = CommunicationAgent()

        # Load disaster dataset
        self.disaster_data = pd.read_csv("datasets/clean_disaster_dataset.csv")

    def run_disaster_simulation(self):

        # Pick a random disaster record
        sample = self.disaster_data.sample(1).iloc[0]

        # 1️⃣ Weather monitoring
        weather_result = self.weather_agent.detect_risk()
        weather_risk = weather_result["risk_level"]

        # 2️⃣ Predict severity using ML model
        prediction = self.prediction_agent.predict_severity(
            deaths=sample["total_deaths"],
            affected=sample["total_affected"]
        )

        # 3️⃣ Create alert
        alert_level = "Red" if sample["total_deaths"] > 1000 else "Orange"

        alert = {
            "disaster_type": sample["disaster_type"],
            "country": sample["Country"],
            "alert_level": alert_level
        }

        # 4️⃣ Assess disaster level
        disaster_level = self.assessment_agent.assess_disaster(
            weather_risk,
            prediction,
            alert_level
        )

        # 5️⃣ Allocate resources
        resources = self.resource_agent.allocate_resources(disaster_level)

        # 6️⃣ Generate response report
        report = self.communication_agent.generate_report(
            alert,
            disaster_level,
            resources
        )

        return report


    # ----------------------------------------------------
    # AUTONOMOUS AI MONITORING LOOP
    # ----------------------------------------------------

    def autonomous_monitor(self):

        print("🚨 AI Monitoring Started...")

        while True:

            report = self.run_disaster_simulation()

            print("\n⚡ AI RESPONSE GENERATED")
            print(report)

            # Run every 30 seconds
            time.sleep(30)
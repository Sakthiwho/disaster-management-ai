import sys
import os
import pandas as pd
import random

# Allow backend to access project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import agents
from agents.weather_agent import WeatherAgent
from agents.prediction_agent import PredictionAgent
from agents.assessment_agent import AssessmentAgent
from agents.alert_agent import AlertAgent
from agents.resource_agent import ResourceAgent
from agents.communication_agent import CommunicationAgent
from agents.route_agent import RouteAgent

# Import database functions
from database.db_manager import init_db, store_alert, store_resource


class AgentPipeline:

    def __init__(self):

        # Initialize database
        init_db()

        # Load agents
        self.weather_agent = WeatherAgent()
        self.prediction_agent = PredictionAgent()
        self.assessment_agent = AssessmentAgent()
        self.alert_agent = AlertAgent()
        self.resource_agent = ResourceAgent()
        self.communication_agent = CommunicationAgent()
        self.route_agent = RouteAgent()

        # Load disaster dataset
        dataset_path = os.path.join("datasets", "clean_alerts_dataset.csv")
        self.data = pd.read_csv(dataset_path)

    def run_pipeline(self):

        # -----------------------------------
        # PICK RANDOM DISASTER FROM DATASET
        # -----------------------------------
        disaster_types = self.data["disaster_type"].unique()

        chosen_type = random.choice(disaster_types)

        sample = self.data[self.data["disaster_type"] == chosen_type].sample(1).iloc[0]

        disaster_type = sample["disaster_type"]
        country = sample["country"]
        latitude = sample["latitude"]
        longitude = sample["longitude"]

        # -----------------------------------
        # SIMULATED DISASTER IMPACT
        # -----------------------------------
        deaths = random.randint(0, 8000)
        affected = random.randint(1000, 500000)

        print("Estimated deaths:", deaths)
        print("People affected:", affected)

        # -----------------------------------
        # WEATHER AGENT
        # -----------------------------------
        weather_result = self.weather_agent.detect_risk()
        weather_risk = weather_result["risk_level"]

        print("Weather Risk:", weather_risk)

        # -----------------------------------
        # PREDICTION AGENT
        # -----------------------------------
        prediction = self.prediction_agent.predict_severity(
            deaths,
            affected
        )

        print("Predicted Severity:", prediction)

        # -----------------------------------
        # ALERT LEVEL LOGIC
        # -----------------------------------
        if deaths > 5000:
            alert_level = "Red"
        elif deaths > 1000:
            alert_level = "Orange"
        else:
            alert_level = "Green"

        # -----------------------------------
        # ASSESSMENT AGENT
        # -----------------------------------
        disaster_level = self.assessment_agent.assess_disaster(
            weather_risk,
            prediction,
            alert_level
        )

        print("Disaster Level:", disaster_level)

        # -----------------------------------
        # SAFE ROUTE AGENT
        # -----------------------------------
        safe_location = self.route_agent.find_nearest_safe_location(
            latitude,
            longitude
        )

        print("Nearest Safe Location:", safe_location)

        # -----------------------------------
        # STORE ALERT
        # -----------------------------------
        store_alert(
            disaster_type,
            country,
            disaster_level,
            latitude,
            longitude
        )

        print("Alert stored in database")

        # -----------------------------------
        # RESOURCE ALLOCATION
        # -----------------------------------
        resources = self.resource_agent.allocate_resources(disaster_level)

        if isinstance(resources, dict):
            store_resource(
                resources.get("hospital"),
                resources.get("shelter"),
                resources.get("warehouse"),
                resources.get("transport_route"),
                1
            )

        print("Resources allocated:", resources)

        # -----------------------------------
        # FINAL REPORT
        # -----------------------------------
        report = {
            "disaster_type": disaster_type,
            "country": country,
            "severity": disaster_level,
            "weather_risk": weather_risk,
            "prediction": prediction,
            "latitude": latitude,
            "longitude": longitude,
            "safe_location": safe_location,
            "resources": resources
        }

        return report
import random


class WeatherAgent:

    def __init__(self):
        pass

    def detect_risk(self):
        """
        Simulates environmental monitoring and returns
        a weather risk level.
        """

        risks = ["Low", "Medium", "High"]

        risk_level = random.choice(risks)

        return {
            "agent": "Weather Agent",
            "risk_level": risk_level
        }
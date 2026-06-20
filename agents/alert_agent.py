import pandas as pd


class AlertAgent:

    def __init__(self):

        # Load alerts dataset
        self.alerts = pd.read_csv("datasets/clean_alerts_dataset.csv")

    def get_random_alert(self):

        alert = self.alerts.sample(1).iloc[0]

        return {
            "disaster_type": str(alert["disaster_type"]),
            "alert_level": str(alert["alert_level"]),
            "country": str(alert["country"]),
            "severity": float(alert["severity"])
        }
class AssessmentAgent:

    def assess_disaster(self, weather_risk, prediction, alert_level):

        # Normalize inputs
        weather_risk = weather_risk.lower()
        prediction = prediction.lower()
        alert_level = alert_level.lower()

        # CRITICAL conditions
        if (
            (prediction == "high" and weather_risk == "high")
            or alert_level == "red"
        ):
            return "CRITICAL"

        # HIGH conditions
        if (
            prediction == "high"
            or weather_risk == "high"
        ):
            return "HIGH"

        # MEDIUM conditions
        if (
            prediction == "low" and weather_risk == "medium"
        ):
            return "MEDIUM"

        # Default
        return "LOW"
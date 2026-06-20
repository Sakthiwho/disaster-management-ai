import joblib
import pandas as pd


class PredictionAgent:

    def __init__(self):

        # Load trained model
        self.model = joblib.load("models/disaster_prediction_model.pkl")

    # -----------------------------
    # PREDICT DISASTER SEVERITY
    # -----------------------------

    def predict_severity(self, deaths, affected):

        input_data = pd.DataFrame({
            "total_deaths": [deaths],
            "total_affected": [affected]
        })

        prediction = self.model.predict(input_data)

        return prediction[0]
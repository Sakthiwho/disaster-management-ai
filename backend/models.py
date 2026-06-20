import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib


class DisasterModel:

    def __init__(self):

        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )

    def train(self, dataset_path):

        data = pd.read_csv(dataset_path)

        X = data.drop(columns=["disaster_type"])
        y = data["disaster_type"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2
        )

        self.model.fit(X_train, y_train)

        joblib.dump(self.model, "models/disaster_model.pkl")

    def load(self):

        self.model = joblib.load("models/disaster_model.pkl")

    def predict(self, input_data):

        return self.model.predict(input_data)
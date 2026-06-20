import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib


# -----------------------------
# LOAD DATASET
# -----------------------------

data = pd.read_csv("datasets/clean_disaster_dataset.csv")


# -----------------------------
# FEATURES
# -----------------------------

X = data[["total_deaths", "total_affected"]]


# -----------------------------
# CREATE SEVERITY LABEL
# -----------------------------

def severity_label(row):

    if row["total_deaths"] > 2000:
        return "CRITICAL"

    if row["total_deaths"] > 500:
        return "HIGH"

    if row["total_deaths"] > 50:
        return "MEDIUM"

    return "LOW"


data["severity"] = data.apply(severity_label, axis=1)


y = data["severity"]


# -----------------------------
# TRAIN MODEL
# -----------------------------

model = RandomForestClassifier(n_estimators=200)

model.fit(X, y)


# -----------------------------
# SAVE MODEL
# -----------------------------

joblib.dump(model, "models/disaster_prediction_model.pkl")

print("Model trained and saved successfully")
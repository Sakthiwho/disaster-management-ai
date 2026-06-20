import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.prediction_agent import PredictionAgent

agent = PredictionAgent()

prediction = agent.predict_severity(
    deaths=400,
    affected=12000
)

print("Predicted Severity:", prediction)
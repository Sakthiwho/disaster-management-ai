from agents.assessment_agent import AssessmentAgent


agent = AssessmentAgent()

result = agent.assess_disaster(
    weather_risk="Storm Risk",
    prediction_severity="High",
    alert_level="Red"
)

print("Final Disaster Level:", result)
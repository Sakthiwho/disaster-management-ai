from agents.communication_agent import CommunicationAgent


alert = {
    "disaster_type": "flood",
    "country": "Mozambique",
    "alert_level": "Red",
    "severity": 7.7
}

resources = {
    "hospital": "H3",
    "shelter": "S3",
    "warehouse": "W3",
    "transport_route": "R1"
}

agent = CommunicationAgent()

report = agent.generate_report(alert, "CRITICAL", resources)

print(report)
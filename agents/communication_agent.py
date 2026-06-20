class CommunicationAgent:

    def generate_report(self, alert, disaster_level, resources):

        report = {}

        report["disaster_type"] = alert["disaster_type"]
        report["country"] = alert["country"]
        report["alert_level"] = alert["alert_level"]
        report["severity"] = disaster_level

        if "hospital" in resources:

            report["resources"] = {
                "hospital": resources["hospital"],
                "shelter": resources["shelter"],
                "warehouse": resources["warehouse"],
                "transport_route": resources["transport_route"]
            }

        else:

            report["resources"] = "No major deployment required."

        return report
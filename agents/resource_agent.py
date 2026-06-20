import pandas as pd


class ResourceAgent:

    def __init__(self):

        # Load infrastructure datasets
        self.hospitals = pd.read_csv("datasets/hospital.csv")
        self.shelters = pd.read_csv("datasets/shelter.csv")
        self.warehouses = pd.read_csv("datasets/warehouse.csv")
        self.transport = pd.read_csv("datasets/transport.csv")

    # --------------------------------------------------
    # RESOURCE ALLOCATION LOGIC
    # --------------------------------------------------

    def allocate_resources(self, disaster_level):

        response = {
            "hospital": None,
            "shelter": None,
            "warehouse": None,
            "transport_route": None,
            "message": ""
        }

        # -----------------------------------------------
        # CRITICAL DISASTER
        # -----------------------------------------------

        if disaster_level == "CRITICAL":

            hospital = self.hospitals.sort_values(
                "ICU_Beds_Available", ascending=False
            ).iloc[0]

            shelter = self.shelters.sort_values(
                "Demand_Quantity", ascending=False
            ).iloc[0]

            warehouse = self.warehouses.sort_values(
                "Rice_kg", ascending=False
            ).iloc[0]

            route = self.transport.sort_values(
                "Estimated_Time_hrs"
            ).iloc[0]

            response["hospital"] = hospital["Hospital_ID"]
            response["shelter"] = shelter["Shelter_ID"]
            response["warehouse"] = warehouse["Warehouse_ID"]
            response["transport_route"] = route["Route_ID"]

            response["message"] = "CRITICAL: Full emergency response deployed."

        # -----------------------------------------------
        # HIGH DISASTER
        # -----------------------------------------------

        elif disaster_level == "HIGH":

            hospital = self.hospitals.sort_values(
                "ICU_Beds_Available", ascending=False
            ).iloc[0]

            shelter = self.shelters.sort_values(
                "Demand_Quantity", ascending=False
            ).iloc[0]

            route = self.transport.sort_values(
                "Estimated_Time_hrs"
            ).iloc[0]

            response["hospital"] = hospital["Hospital_ID"]
            response["shelter"] = shelter["Shelter_ID"]
            response["transport_route"] = route["Route_ID"]

            response["message"] = "HIGH: Rescue teams and shelters deployed."

        # -----------------------------------------------
        # MEDIUM DISASTER
        # -----------------------------------------------

        elif disaster_level == "MEDIUM":

            shelter = self.shelters.sort_values(
                "Demand_Quantity", ascending=False
            ).iloc[0]

            response["shelter"] = shelter["Shelter_ID"]

            response["message"] = "MEDIUM: Shelter preparation activated."

        # -----------------------------------------------
        # LOW DISASTER
        # -----------------------------------------------

        else:

            response["message"] = "LOW: Monitoring situation. No deployment required."

        return response
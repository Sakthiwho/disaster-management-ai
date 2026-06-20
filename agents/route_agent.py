import pandas as pd
from math import radians, cos, sin, sqrt, atan2


class RouteAgent:

    def __init__(self):

        self.infrastructure = pd.read_csv(
            "datasets/clean_infrastructure_dataset.csv"
        )

    def calculate_distance(self, lat1, lon1, lat2, lon2):

        R = 6371  # Earth radius

        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)

        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        return R * c

    def find_nearest_safe_location(self, disaster_lat, disaster_lon):

        nearest = None
        min_distance = float("inf")

        for _, row in self.infrastructure.iterrows():

            dist = self.calculate_distance(
                disaster_lat,
                disaster_lon,
                row["latitude"],
                row["longitude"]
            )

            if dist < min_distance:
                min_distance = dist
                nearest = row

        return {
            "name": nearest["name"],
            "type": nearest["infrastructure_type"],
            "latitude": nearest["latitude"],
            "longitude": nearest["longitude"],
            "distance_km": round(min_distance, 2)
        }
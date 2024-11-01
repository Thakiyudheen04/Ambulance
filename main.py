import random
import time
import logging
from math import radians, sin, cos, sqrt, atan2

# Set up logging to record alerts
logging.basicConfig(filename='v2x_alerts.log', level=logging.INFO, format='%(asctime)s - %(message)s')


# Define the Ambulance class
class Ambulance:
    def __init__(self, id, lat, lon, radius=1):
        self.id = id
        self.lat = lat
        self.lon = lon
        self.radius = radius  # Range within which vehicles will be alerted

    def get_location(self):
        # Simulate location change (for movement)
        self.lat += random.uniform(-0.0001, 0.0001)
        self.lon += random.uniform(-0.0001, 0.0001)
        return self.lat, self.lon

    def broadcast_location(self, vehicles):
        # Broadcast location to all vehicles within a certain range
        ambulance_location = self.get_location()
        print(f"Ambulance {self.id} broadcasting location: {ambulance_location}")
        for vehicle in vehicles:
            vehicle.receive_broadcast(self.id, ambulance_location, self.radius)


# Define the Vehicle class
class Vehicle:
    def __init__(self, id, lat, lon):
        self.id = id
        self.lat = lat
        self.lon = lon

    def get_location(self):
        return self.lat, self.lon

    def receive_broadcast(self, ambulance_id, ambulance_location, radius):
        # Calculate distance between vehicle and ambulance
        vehicle_location = self.get_location()
        distance = calculate_distance(ambulance_location[0], ambulance_location[1], vehicle_location[0],
                                      vehicle_location[1])

        # Alert if within range, otherwise no alert
        if distance <= radius:
            alert_message = f"ALERT: Vehicle {self.id} is {distance:.2f} km from Ambulance {ambulance_id}. Please clear the way!"
            print(alert_message)
            logging.info(alert_message)
        else:
            no_alert_message = f"Vehicle {self.id} is {distance:.2f} km from Ambulance {ambulance_id}. No action needed."
            print(no_alert_message)
            logging.info(no_alert_message)


# Calculate distance using the Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth's radius in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


# Simulate real-time V2X communication
ambulance = Ambulance(id=1, lat=12.9716, lon=77.5946)
vehicles = [
    Vehicle(id=1, lat=12.9711, lon=77.5945),
    Vehicle(id=2, lat=12.9721, lon=77.5956),
    Vehicle(id=3, lat=12.9736, lon=77.5978)
]

# Simulate the ambulance broadcasting its location every 2 seconds
for _ in range(10):
    ambulance.broadcast_location(vehicles)
    time.sleep(2)

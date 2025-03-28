import requests
import random
import time

# Generate mock vital signs
def generate_mock_vitals():
    return {
        "heart_rate": random.randint(60, 150),
        "blood_pressure": random.choice([120/80, 130/85, 140/90, 150/95]),
    }

# Send data to Flask API every 5 seconds
api_url = "http://127.0.0.1:5000/api/vitals"

while True:
    vitals = generate_mock_vitals()
    response = requests.post(api_url, json=vitals)
    print(f"Sent data: {vitals}, Response: {response.json()}")
    time.sleep(5)

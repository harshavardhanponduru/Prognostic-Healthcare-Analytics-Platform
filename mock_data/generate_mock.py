# /Users/harsha/Predictive-Healing-Pavilion/mock_data/generate_mock.py
import requests
import random
import time

api_url = "http://127.0.0.1:5000/api/vitals"

# Simulate mock vitals
def generate_mock_vitals():
    return {
        "heart_rate": random.randint(60, 150),  # Random heart rate between 60 and 150 bpm
        "blood_pressure": random.choice([120, 130, 140, 150, 160])  # Random systolic BP
    }

while True:
    try:
        vitals = generate_mock_vitals()

        # Simulate some extreme values for testing
        if random.random() > 0.8:  # Random chance to send abnormal vitals
            vitals["heart_rate"] = random.randint(150, 180)  # Simulate high heart rate
            vitals["blood_pressure"] = random.choice([160, 170, 180])  # Simulate high BP

        response = requests.post(api_url, json=vitals)
        print(f"Sent data: {vitals}, Response: {response.json()}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    time.sleep(5)  # Send every 5 seconds

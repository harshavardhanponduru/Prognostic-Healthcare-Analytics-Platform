import random
import time
import requests

# --- API Endpoint ---
API_URL = "http://127.0.0.1:5000/api/vitals"

# --- Generate Random Vitals ---
def generate_mock_vitals():
    heart_rate = random.randint(60, 140)  # Seeker speed (heart rate)
    blood_pressure = random.randint(80, 160)  # Bludger impacts (blood pressure)
    return {"heart_rate": heart_rate, "blood_pressure": blood_pressure}

# --- Send Mock Vitals to API ---
def send_mock_data():
    while True:
        data = generate_mock_vitals()
        try:
            response = requests.post(API_URL, json=data)
            if response.status_code == 200:
                print(f"✅ Vitals Sent: {data}")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Failed to send vitals: {e}")

        # Wait for 5 seconds before sending the next data
        time.sleep(5)

# --- Start Sending Mock Data ---
if __name__ == "__main__":
    send_mock_data()

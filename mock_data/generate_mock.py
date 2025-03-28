import requests
import random
import time

# --- Generate mock vital signs ---
def generate_mock_vitals():
    systolic_bp = random.choice([120, 130, 140, 150])  # Systolic BP
    diastolic_bp = random.choice([80, 85, 90, 95])  # Diastolic BP

    return {
        "heart_rate": random.randint(60, 150),  # Random heart rate between 60 and 150 bpm
        "systolic_bp": systolic_bp,
        "diastolic_bp": diastolic_bp,
    }


# --- Flask API endpoint ---
API_URL = "http://127.0.0.1:5000/api/vitals"

# --- Send mock data to Flask API every 5 seconds ---
while True:
    try:
        vitals = generate_mock_vitals()

        # Send POST request to Flask API
        response = requests.post(API_URL, json=vitals)

        # Check response status
        if response.status_code == 200:
            print(f"✅ Sent data: {vitals}, Response: {response.json()}")
        else:
            print(f"❗ Error: Received status code {response.status_code}, Response: {response.text}")

    except requests.ConnectionError:
        print("❌ Connection error: Unable to reach the API.")
    except requests.Timeout:
        print("⏳ Timeout error: The request took too long to get a response.")
    except requests.RequestException as e:
        print(f"❌ API error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    # Wait 5 seconds before sending the next set of vitals
    time.sleep(5)

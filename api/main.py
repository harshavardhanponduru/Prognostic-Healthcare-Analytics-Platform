from flask import Flask, request, jsonify
import random
from datetime import datetime

app = Flask(__name__)

# Mock API route to receive IoT data
@app.route('/api/vitals', methods=['POST'])
def receive_vitals():
    data = request.json
    heart_rate = data.get('heart_rate')
    blood_pressure = data.get('blood_pressure')

    # Analyze vitals using basic rules
    alert = check_vitals(heart_rate, blood_pressure)

    # Prepare response
    response = {
        "status": "Data received",
        "heart_rate": heart_rate,
        "blood_pressure": blood_pressure,
        "alert": alert
    }
    return jsonify(response), 200

# Basic rule-based check for vitals
def check_vitals(hr, bp):
    alert = "All Good"
    if hr > 120:
        alert = "High Seeker Speed! Possible stress."
    if bp > 140/90:
        alert = "Bludger Hit! Hypertension risk."
    return alert

if __name__ == '__main__':
    app.run(debug=True, port=5000)

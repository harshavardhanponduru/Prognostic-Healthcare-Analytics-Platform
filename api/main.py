import sqlite3

import joblib
import numpy as np
from flask import Flask, request, jsonify, render_template
from vitals.database import init_db, save_vitals, get_latest_vitals, DB_PATH
from flask_cors import CORS

app = Flask(__name__, template_folder='../api/templates')

# --- Load trained model at startup ---
try:
    model_path = "/Users/harsha/Predictive-Healing-Pavilion/api/risk_model.pkl"
    model = joblib.load(model_path)
    print("✅ Model loaded successfully!")
except FileNotFoundError:
    print(f"❌ Error: {model_path} not found. Please train and save the model first.")
    model = None

CORS(app)  # Allow all origins (for testing)

# --- Basic rule-based check for vitals ---
def check_vitals(hr, bp):
    alert = "All Good"
    if hr > 120:
        alert = "High Seeker Speed! Possible stress."
    if bp > 140:
        alert = "Bludger Hit! Hypertension risk."
    elif bp < 90:
        alert = "Low Blood Pressure! Risk of fainting."
    return alert

# --- Mock API route to receive IoT data ---
@app.route('/api/vitals', methods=['POST'])
def receive_vitals():
    try:
        data = request.json
        heart_rate = data.get('heart_rate')
        blood_pressure = data.get('blood_pressure')

        if heart_rate is None or blood_pressure is None:
            return jsonify({"error": "Missing heart_rate or blood_pressure"}), 400

        # Analyze vitals using basic rules
        alert = check_vitals(heart_rate, blood_pressure)

        # Save data to database
        save_vitals(heart_rate, blood_pressure, alert)

        # Prepare response
        response = {
            "status": "Data received",
            "heart_rate": heart_rate,
            "blood_pressure": blood_pressure,
            "alert": alert
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- API route to predict health risk ---
@app.route('/api/predict', methods=['POST'])
def predict_risk():
    if model is None:
        return jsonify({"error": "Model not loaded. Check the path or train the model."}), 500

    try:
        data = request.json
        heart_rate = data.get('heart_rate')
        blood_pressure = data.get('blood_pressure')

        # Validate input values
        if heart_rate is None or blood_pressure is None:
            return jsonify({"error": "Missing heart_rate or blood_pressure"}), 400

        # Prepare data for prediction
        input_data = np.array([[heart_rate, blood_pressure]])
        prediction = model.predict(input_data)[0]

        # Map prediction to Quidditch-like status
        if prediction == 1:
            risk_status = "Bludger Danger! Monitor closely."
        else:
            risk_status = "Seeker Speed Normal. No immediate risk."

        response = {
            "heart_rate": heart_rate,
            "blood_pressure": blood_pressure,
            "prediction": int(prediction),
            "status": risk_status
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- API route to get the latest vitals ---
@app.route('/api/vitals/latest', methods=['GET'])
def latest_vitals():
    try:
        vitals = get_latest_vitals()
        return jsonify(vitals), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- API route to get historical vitals data ---
@app.route('/api/vitals/history', methods=['GET'])
def vitals_history():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT heart_rate, blood_pressure, alert, timestamp
            FROM vitals
            ORDER BY timestamp DESC
            LIMIT 20
        ''')
        data = cursor.fetchall()
        conn.close()

        vitals_history = []
        for row in data:
            vitals_history.append({
                "heart_rate": row[0],
                "blood_pressure": row[1],
                "alert": row[2],
                "timestamp": row[3]
            })

        return jsonify(vitals_history), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Route to render the dashboard ---
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Initialize the database
init_db()

# --- Run Flask server ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)

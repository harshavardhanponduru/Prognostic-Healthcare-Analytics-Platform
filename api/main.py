from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from api.vitals.database import init_db, save_vitals, get_latest_vitals
import sqlite3
from vitals.database import DB_PATH
import numpy as np
import joblib
import os

app = Flask(__name__, template_folder="templates")
CORS(app)

# --- Load trained model if available ---
model_path = os.path.join(os.path.dirname(__file__), "models/risk_model.pkl")
model = None
if os.path.exists(model_path):
    try:
        model = joblib.load(model_path)
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")


# --- Health rule-based check ---
def check_vitals(hr, bp):
    if hr > 120:
        return "High Seeker Speed! Possible stress."
    if bp > 140:
        return "Bludger Hit! Hypertension risk."
    if bp < 90:
        return "Low Blood Pressure! Risk of fainting."
    return "All Good"


# --- API to receive vitals data ---
@app.route('/api/vitals', methods=['POST'])
def receive_vitals():
    data = request.json
    heart_rate = data.get('heart_rate')
    blood_pressure = data.get('blood_pressure')

    if heart_rate is None or blood_pressure is None:
        return jsonify({"error": "Missing heart_rate or blood_pressure"}), 400

    alert = check_vitals(heart_rate, blood_pressure)
    save_vitals(heart_rate, blood_pressure, alert)

    return jsonify({
        "status": "Data received",
        "heart_rate": heart_rate,
        "blood_pressure": blood_pressure,
        "alert": alert
    }), 200


# --- API to get latest vitals ---
@app.route('/api/vitals/latest', methods=['GET'])
def latest_vitals():
    vitals = get_latest_vitals()
    return jsonify(vitals), 200


# --- API to predict health risk ---
@app.route('/api/predict', methods=['POST'])
def predict_risk():
    if model is None:
        return jsonify({"error": "Model not loaded."}), 500

    data = request.json
    heart_rate = data.get('heart_rate')
    blood_pressure = data.get('blood_pressure')

    if heart_rate is None or blood_pressure is None:
        return jsonify({"error": "Missing heart_rate or blood_pressure"}), 400

    input_data = np.array([[heart_rate, blood_pressure]])
    prediction = model.predict(input_data)[0]
    risk_status = "Bludger Danger! Monitor closely." if prediction == 1 else "Seeker Speed Normal. No immediate risk."

    return jsonify({
        "heart_rate": heart_rate,
        "blood_pressure": blood_pressure,
        "prediction": int(prediction),
        "status": risk_status
    }), 200

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


# --- Route to render dashboard ---
@app.route('/')
def dashboard():
    return render_template('dashboard.html')


# --- Initialize the database ---
init_db()

# --- Run Flask server ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)

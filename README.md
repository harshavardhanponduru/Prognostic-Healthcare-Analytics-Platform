# Prognostic Healthcare Analytics Platform

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey?logo=flask)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.x-orange?logo=scikitlearn)
![SQLite](https://img.shields.io/badge/SQLite-3-lightblue?logo=sqlite)
![Twilio](https://img.shields.io/badge/Twilio-API-red?logo=twilio)
![License](https://img.shields.io/badge/License-MIT-green)
---

## 📌 Overview

The **Prognostic Healthcare Analytics Platform** is a healthcare solution that enhances patient care through **predictive analytics**. By integrating **real-time vital signs** from wearable IoT devices, the system generates **data-driven insights, alerts, and personalized recommendations**.  

The platform empowers healthcare professionals to **identify risks before they escalate**, enabling **proactive care** and better patient outcomes.

---

## 📑 Table of Contents

- [Key Features](#-key-features)  
- [Technologies](#-technologies)  
- [Getting Started](#-getting-started)  
- [Configuration](#-configuration)  
- [Project Structure](#-project-structure)  
- [API Documentation](#-api-documentation)  
- [Contributors](#-contributors)  
- [License](#-license)  

---

## 🚀 Key Features

- **Real-time Monitoring** – Securely collects and stores patient vitals in SQLite.  
- **AI-Powered Predictions** – Uses **Scikit-learn ML models** for risk assessment.  
- **Automated Alerts** – Sends **SMS alerts** via **Twilio API**.  
- **RESTful API** – Integration-ready for **EHRs** and clinical systems.  
- **AI Clinical Tools** – Integrates with **Gemini API** for:  
  - Automated clinical note generation  
  - Clinical Q&A assistant  

---

## 🛠️ Technologies

- Python  
- Flask  
- Scikit-learn  
- SQLite  
- Twilio API  
- Gemini API  
- HTML, CSS, JavaScript  
- Git  

---

## ⚙️ Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/harshavardhanponduru/Predictive-Healing-Pavilion-main.git
cd Predictive-Healing-Pavilion-main
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
flask run
```

---

## ⚙️ Configuration

Before running the application, configure the required environment variables.  

### 1. Create a `.env` file in the project root:
```ini
# Flask
FLASK_APP=app.py
FLASK_ENV=development

# SQLite Database
DATABASE_URL=sqlite:///vitals.db

# Twilio API (for SMS alerts)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# Gemini API (for AI-driven clinical tools)
GEMINI_API_KEY=your_gemini_api_key
```

### 2. Load environment variables:
```bash
export $(cat .env | xargs)
```

> ⚠️ **Important:** Never commit your `.env` file or real credentials to GitHub. Use `.gitignore` to keep it secure.

---

## 📂 Project Structure

```
.
├── .idea/              # IDE configuration files
├── api/                # Source code for RESTful API
├── mock/               # Mock data and testing resources
├── requirements.txt    # Python dependencies
└── vitals.db           # SQLite database file
```

---

## 📄 API Documentation

**Base URL:**  
```
http://127.0.0.1:5000/api/v1
```

### 1. Get All Patient Vitals
- **Endpoint:** `GET /vitals`  
- **Description:** Fetches the latest vitals for all patients.  

**Example Request:**
```bash
curl -X GET http://127.0.0.1:5000/api/v1/vitals
```

---

### 2. Get Vitals for a Specific Patient
- **Endpoint:** `GET /vitals/<patient_id>`  
- **Description:** Fetches vitals for a given patient ID.  

**Example Request:**
```bash
curl -X GET http://127.0.0.1:5000/api/v1/vitals/P12345
```

---

### 3. Submit New Vitals
- **Endpoint:** `POST /vitals`  
- **Description:** Adds vitals for a patient (IoT or mock data).  

**Example Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/v1/vitals   -H "Content-Type: application/json"   -d '{"patient_id": "P12345", "heart_rate": 82, "blood_pressure": "118/79", "oxygen_saturation": 98}'
```

---

### 4. Trigger an Alert
- **Endpoint:** `POST /alerts`  
- **Description:** Sends a critical SMS alert to providers.  

**Example Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/v1/alerts   -H "Content-Type: application/json"   -d '{"patient_id": "P12345", "condition": "High Blood Pressure", "severity": "critical"}'
```

---

### 5. Health Check
- **Endpoint:** `GET /health`  
- **Description:** Verifies if API server is running.  

**Example Request:**
```bash
curl -X GET http://127.0.0.1:5000/api/v1/health
```

---

## 👥 Contributors

- Harshavardhan Ponduru  
- Aditya Kumar Satapathy  
- Debansha Rout  
- Sushobhan Ghosh  

---

## 📜 License

This project is licensed under the **MIT License** – see the [LICENSE](./LICENSE) file for details.

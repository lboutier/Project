from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import pickle
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load trained ML model at startup
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
except Exception as e:
    model = None
    print("⚠️ Error loading model.pkl:", e)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("patients.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS admissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        surname TEXT,
        age INTEGER,
        date TEXT,
        specialty TEXT,
        urgency INTEGER,
        recommendation TEXT,
        hospital TEXT
    )''')
    conn.commit()
    conn.close()

# Homepage test
@app.route("/")
def home():
    return "✔️ Flask API is running!"

# Get all hospitals
@app.route("/get_hospitals", methods=["GET"])
def get_hospitals():
    hospitals = [
        {
            "name": "Rotthalmünster",
            "specialties": ["Stroke", "Anesthesia", "Cardiology"],
            "latitude": 48.354987,
            "longitude": 13.201969,
            "available_beds": 12,
            "capacity": 100
        },
        {
            "name": "Vilshofen",
            "specialties": ["Geriatrics", "Cardiology", "Pediatrics"],
            "latitude": 48.627808,
            "longitude": 13.19838,
            "available_beds": 5,
            "capacity": 150
        },
        {
            "name": "Wegscheid",
            "specialties": ["Gynecology", "Radiology", "Orthopedics"],
            "latitude": 48.6012951,
            "longitude": 13.7930649,
            "available_beds": 20,
            "capacity": 120
        }
    ]

    for h in hospitals:
        h["occupancy_rate"] = round(((h["capacity"] - h["available_beds"]) / h["capacity"]) * 100, 2)

    return jsonify(hospitals)

# Save a new patient to database
@app.route("/add_patient", methods=["POST"])
def add_patient():
    data = request.get_json()
    conn = sqlite3.connect("patients.db")
    c = conn.cursor()
    c.execute('''INSERT INTO admissions (name, surname, age, date, specialty, urgency, recommendation, hospital)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (data["name"], data["surname"], data["age"], data["date"],
               data["specialty"], data["urgency"], data["recommendation"], data.get("hospital")))
    conn.commit()
    conn.close()
    return jsonify({"message": "Patient saved"}), 201

# Retrieve all patients
@app.route("/get_admissions", methods=["GET"])
def get_admissions():
    conn = sqlite3.connect("patients.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM admissions")
    rows = c.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# AI model prediction endpoint
@app.route("/predict", methods=["POST"])
def predict():
    if not model:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json()

    try:
        input_df = pd.DataFrame([{
            "Urgency": data["urgency"],
            "Distance": data["distance"],
            "Specialty": data["specialty"],
            "Availability": data["availability"]
        }])
        prediction = model.predict(input_df)
        return jsonify({"recommended_hospital": prediction[0]})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Launch app
if __name__ == "__main__":
    init_db()
    app.run(debug=True)

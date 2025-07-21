from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Initialize database
def init_db():
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_name TEXT,
            first_name TEXT,
            age INTEGER,
            date TEXT,
            specialty TEXT,
            urgency INTEGER,
            recommendation TEXT,
            hospital TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Call init_db immediately so it's ready on Render
init_db()

# Root route
@app.route("/")
def home():
    return "✔️ Hospital API is running!"

# Add a new patient
@app.route("/add_patient", methods=["POST"])
def add_patient():
    data = request.get_json()
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO admissions (last_name, first_name, age, date, specialty, urgency, recommendation, hospital)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data["last_name"],
        data["first_name"],
        data["age"],
        data["date"],
        data["specialty"],
        data["urgency"],
        data["recommendation"],
        data.get("hospital")
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Patient saved successfully"}), 201

# Get all admissions
@app.route("/get_admissions", methods=["GET"])
def get_admissions():
    conn = sqlite3.connect("patients.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admissions")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# Get hospital list
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

    # Add occupancy rate
    for h in hospitals:
        h["occupancy_rate"] = round(((h["capacity"] - h["available_beds"]) / h["capacity"]) * 100, 2)

    return jsonify(hospitals)

# Only run if executed directly
if __name__ == "__main__":
    app.run(debug=True)

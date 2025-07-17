from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("patients.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS admissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        prenom TEXT,
        age INTEGER,
        date TEXT,
        specialite TEXT,
        urgence INTEGER,
        recommandation TEXT,
        hopital TEXT
    )''')
    conn.commit()
    conn.close()

@app.route("/add_patient", methods=["POST"])
def add_patient():
    data = request.get_json()
    conn = sqlite3.connect("patients.db")
    c = conn.cursor()
    c.execute('''INSERT INTO admissions (nom, prenom, age, date, specialite, urgence, recommandation, hopital)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (data["Nom"], data["Prénom"], data["Age"], data["Date"],
               data["Specialite"], data["Urgence"], data["Recommandation"], data.get("Hopital")))
    conn.commit()
    conn.close()
    return jsonify({"message": "Patient saved"}), 201

@app.route("/get_admissions", methods=["GET"])
def get_admissions():
    conn = sqlite3.connect("patients.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM admissions")
    rows = c.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])
    
@app.route("/")
def home():
    return "✔️ Flask API is running!"
@app.route("/get_hospitals", methods=["GET"])
def get_hospitals():
    hospitals_data = [
        {
            "Nom": "Rotthalmünster",
            "Specialites": ["Stroke", "Anesthesia", "Cardiology"],
            "Latitude": 48.354987,
            "Longitude": 13.201969,
            "Lits_disponibles": 12,
            "Capacite": 100
        },
        {
            "Nom": "Vilshofen",
            "Specialites": ["Geriatrics", "Cardiology", "Pediatrics"],
            "Latitude": 48.627808,
            "Longitude": 13.19838,
            "Lits_disponibles": 5,
            "Capacite": 150
        },
        {
            "Nom": "Wegscheid",
            "Specialites": ["Gynecology", "Radiology", "Orthopedics"],
            "Latitude": 48.6012951,
            "Longitude": 13.7930649,
            "Lits_disponibles": 20,
            "Capacite": 120
        }
    ]

    # Calculer le taux d’occupation pour chaque hôpital
    for h in hospitals_data:
        h["Taux_occupation"] = round(((h["Capacite"] - h["Lits_disponibles"]) / h["Capacite"]) * 100, 2)

    return jsonify(hospitals_data)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

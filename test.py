from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

# Initialisiere Flask-App
app = Flask(__name__)

# Initialisiere oder erstelle die Datenbank
DB_NAME = 'esp32_data.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            humidity REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Route, um Daten vom ESP32 zu empfangen
@app.route('/api/data', methods=['POST'])
def receive_data():
    try:
        # Empfange JSON-Daten
        data = request.get_json()
        temperature = data.get('temperature')
        humidity = data.get('humidity')

        # Prüfe, ob die Werte korrekt sind
        if temperature is None or humidity is None:
            return jsonify({'error': 'Invalid data'}), 400

        # Daten in die Datenbank einfügen
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sensor_data (temperature, humidity) 
            VALUES (?, ?)
        ''', (temperature, humidity))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Data received successfully!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route, um Daten aus der Datenbank abzurufen (optional)
@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sensor_data ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        conn.close()

        # Daten formatieren
        data = [
            {'id': row[0], 'temperature': row[1], 'humidity': row[2], 'timestamp': row[3]}
            for row in rows
        ]

        return jsonify(data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Main-Funktion
if __name__ == '__main__':
    init_db()
    app.run(port=5001)
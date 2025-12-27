import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy
import threading
import time

# ---------------- GPIO SETUP ----------------
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

BUZZER = 18
GPIO.setup(BUZZER, GPIO.OUT)

def beep():
    GPIO.output(BUZZER, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(BUZZER, GPIO.LOW)

# ---------------- RFID ----------------
reader = SimpleMFRC522()

# ---------------- FLASK ----------------
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ---------------- DATABASE ----------------
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.String(50))
    action = db.Column(db.String(20))

with app.app_context():
    db.create_all()

# ---------------- RFID LOOP ----------------
def rfid_loop():
    while True:
        try:
            card_id, text = reader.read()
            print("RFID Scanned:", card_id)

            with app.app_context():
                entry = Log(card_id=str(card_id), action="Scanned")
                db.session.add(entry)
                db.session.commit()

            beep()
            time.sleep(2)

        except Exception as e:
            print("RFID Error:", e)

# ---------------- WEB UI ----------------
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Smart Library</title>
    <style>
        body { font-family: Arial; background:#0f0f0f; color:#fff; }
        table { width:100%; border-collapse: collapse; }
        th, td { padding:10px; border-bottom:1px solid #444; }
    </style>
</head>
<body>
    <h2>📚 Smart Library – Live Logs</h2>
    <table>
        <tr>
            <th>ID</th>
            <th>Card UID</th>
            <th>Action</th>
        </tr>
        {% for log in logs %}
        <tr>
            <td>{{ log.id }}</td>
            <td>{{ log.card_id }}</td>
            <td>{{ log.action }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route("/")
def index():
    logs = Log.query.order_by(Log.id.desc()).all()
    return render_template_string(HTML, logs=logs)

# ---------------- START EVERYTHING ----------------
if __name__ == "__main__":
    threading.Thread(target=rfid_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)

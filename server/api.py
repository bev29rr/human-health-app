from flask import Blueprint, request, jsonify, session, g
import sqlite3, json

DATABASE = "database.db"

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

api = Blueprint('api', __name__, url_prefix='/api')

try:
    with open("config.json", "r") as file:
        json_data = json.load(file)
except Exception as e:
    print("Error loading config.json:", e)
    json_data = {}

@api.route('/login', methods=['POST'])
def handle_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"response": False, "error": "Missing credentials"}), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    sql_data = cursor.fetchone()

    if sql_data and sql_data[1] == password:  #TODO: use password hashing
        session["username"] = username
        return jsonify({"response": True})
    else:
        return jsonify({"response": False})

@api.route("/status", methods=["GET"])
def status():
    current_user = get_user()
    if current_user:
        return jsonify({"response": current_user})
    else:
        return jsonify({"response": False}), 401

def get_user():
    return session.get("username", False)

@api.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)
    return jsonify({"response": "Logged out successfully"})

@api.route('/heartRate')
def serve_heartrate():
    try:
        with open('static/txt/heartrate.txt', 'r') as file:
            bpm = file.read().strip()
        return jsonify({"bpm": bpm})
    except Exception as e:
        return jsonify({"bpm": 100, "error": str(e)})

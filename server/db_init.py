import sqlite3
import json

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

with open("config.json", "r") as file:
    json_data = json.load(file)

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
""")

for user in json_data.get("users", []):
    cursor.execute("""
        INSERT INTO users (username, password) 
        VALUES (?, ?)""", 
        (user.get("username"), user.get("password"))
    )

conn.commit()
conn.close()
print("Databases initialised")
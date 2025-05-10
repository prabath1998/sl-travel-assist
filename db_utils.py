import sqlite3
from datetime import datetime

DB_NAME = "messages.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_text TEXT,
                    timestamp TEXT,
                    is_trained BOOLEAN DEFAULT 0
                )''')
    conn.commit()
    conn.close()

def insert_message(msg):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO messages (message_text, timestamp, is_trained) VALUES (?, ?, ?)",
              (msg, datetime.utcnow().isoformat(), False))
    conn.commit()
    conn.close()

init_db()
import sqlite3
from datetime import datetime

DB_NAME = "feedback.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_message TEXT,
                    bot_reply TEXT,
                    helpful BOOLEAN,
                    intent_tag TEXT,
                    is_trained BOOLEAN DEFAULT 0,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    conn.close()

def insert_feedback(user_message, bot_reply, helpful, intent_tag=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO feedback (user_message, bot_reply, helpful, intent_tag) VALUES (?, ?, ?, ?)",
              (user_message, bot_reply, helpful, intent_tag))
    conn.commit()
    conn.close()

init_db()
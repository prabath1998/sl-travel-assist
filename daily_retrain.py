import sqlite3
import json
from nltk_utils import tokenize

DB_NAME = "messages.db"

with open("intents.json", "r") as f:
    intents = json.load(f)

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
cursor.execute("SELECT id, message_text FROM messages WHERE is_trained = 0")
new_messages = cursor.fetchall()

if not new_messages:
    print("No new messages to train.")
else:
    print(f"Adding {len(new_messages)} new messages to intents...")
    default_tag = "unknown"
    exists = any(i['tag'] == default_tag for i in intents['intents'])
    if not exists:
        intents['intents'].append({"tag": default_tag, "patterns": [], "responses": ["I do not understand yet."]})

    for msg_id, msg in new_messages:
        for intent in intents['intents']:
            if intent['tag'] == default_tag:
                intent['patterns'].append(msg)
        cursor.execute("UPDATE messages SET is_trained = 1 WHERE id = ?", (msg_id,))

    with open("intents.json", "w") as f:
        json.dump(intents, f, indent=2)

    conn.commit()
    conn.close()

    import subprocess
    print("Retraining model...")
    subprocess.run(["python", "train.py"])
    print("Retrain complete.")
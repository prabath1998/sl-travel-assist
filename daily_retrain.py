import sqlite3
import json

DB_NAME = "feedback.db"

with open("intents.json", "r") as f:
    intents = json.load(f)

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
cursor.execute("SELECT id, user_message, intent_tag FROM feedback WHERE helpful = 1 AND is_trained = 0")
new_feedback = cursor.fetchall()

if not new_feedback:
    print("No new feedback to train.")
else:
    print(f"Adding {len(new_feedback)} feedback messages to intents...")
    for feedback_id, msg, tag in new_feedback:
        if tag and tag != "unknown":
            for intent in intents['intents']:
                if intent['tag'] == tag:
                    intent['patterns'].append(msg)
                    break
            else:
                intents['intents'].append({"tag": tag, "patterns": [msg], "responses": ["I do not understand yet."]})
        else:
            for intent in intents['intents']:
                if intent['tag'] == "unknown":
                    intent['patterns'].append(msg)
                    break
            else:
                intents['intents'].append({"tag": "unknown", "patterns": [msg], "responses": ["I do not understand yet."]})

        cursor.execute("UPDATE feedback SET is_trained = 1 WHERE id = ?", (feedback_id,))

    with open("intents.json", "w") as f:
        json.dump(intents, f, indent=2)

    conn.commit()
    conn.close()

    import subprocess
    print("Retraining model...")
    subprocess.run(["python", "train.py"])
    print("Retrain complete.")
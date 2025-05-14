from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from feedback_utils import insert_feedback

app = Flask(__name__)
CORS(app)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.6:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses']), tag
    return "I do not understand...", "unknown"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    response, tag = get_response(user_input)
    return jsonify({'bot': response, 'tag': tag})

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    user_message = data.get("user_message", "")
    bot_reply = data.get("bot_reply", "")
    helpful = data.get("helpful", False)
    intent_tag = data.get("intent_tag", None)

    if user_message and bot_reply:
        insert_feedback(user_message, bot_reply, helpful, intent_tag)

    return jsonify({'status': 'Feedback received'})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
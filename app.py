from flask import Flask, request, jsonify
from flask_cors import CORS
import random

from dotenv import load_dotenv
import os

load_dotenv()


# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for Flutter

# Sample responses for the chatbot
responses = {
    "hello": ["Hi there!", "Hello!", "Hey! How can I assist you?"],
    "how are you": ["I'm just a bot, but I'm doing great! How about you?"],
    "bye": ["Goodbye!", "See you later!", "Take care!"],
    "thank": ["You're welcome!", "No problem!", "Glad to help!", "See you later!"],
    "default": ["I'm not sure I understand. Can you rephrase that?"],
}

def chatbot_response(user_input):
    user_input = user_input.lower()
    tokens = user_input.split()  # Tokenizing user input (without nltk)

    # Check for keywords in the tokenized input
    for key in responses.keys():
        if any(word in tokens for word in key.split()):  # Match words
            return random.choice(responses[key])

    return random.choice(responses["default"])

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please enter a message."})

    bot_reply = chatbot_response(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    # app.run(debug=True, port=5000)
    app.run(
        host=os.getenv('FLASK_RUN_HOST', '127.0.0.1'),
        port=int(os.getenv('FLASK_RUN_PORT', 5000)),
        debug=True
    )
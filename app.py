from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')

    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "contents": [{
            "parts": [{"text": user_input}]
        }]
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        try:
            reply = response.json()['candidates'][0]['content']['parts'][0]['text']
            return jsonify({'response': reply})
        except Exception:
            return jsonify({'response': 'Error parsing response from Gemini.'})
    else:
        return jsonify({'response': 'Failed to connect to Gemini API.'})

if __name__ == '__main__':
    app.run(debug=True)

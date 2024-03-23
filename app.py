from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://68.146.5.150"}})

LLAMA_API_URL = "https://llama2.ai/api"

@app.route('/api', methods=['POST'])
def handle_api_request():
    message = request.json.get('message', '')

    # Create payload for llama2.ai API
    payload = {
        "prompt": "<s>[INST] <<SYS>>\nYou are a helpful assistant.All of your messages will use perfect grammer, without errors, and will not be misleading.  Who will solely help with brainstorming, and coming up with ideas, you will never generate a full assignment which can be directly submitted, you will refuse to answer any requests that are of this matter.\n<</SYS>>\n\n{Message} [/INST]\n",
        "model": "meta/llama-2-70b-chat",
        "systemPrompt": "You are a helpful assistant.",
        "temperature": 0.75,
        "topP": 0.9,
        "maxTokens": 800,
        "image": None,
        "audio": None
    }

    # Set the message in the payload
    payload['prompt'] = payload['prompt'].replace("{Message}", message)

    # Send request to llama2.ai API
    headers = {'Content-Type': 'application/json'}
    response = requests.post(LLAMA_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        return jsonify({"error": "Failed to process request"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

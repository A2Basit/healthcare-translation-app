from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS
# Clear any existing value from the environment
if "GROQ_API_KEY" in os.environ:
    print(f"Found existing GROQ_API_KEY in environment: {os.environ['GROQ_API_KEY']}")
    del os.environ["GROQ_API_KEY"]
    print("Deleted existing GROQ_API_KEY from environment")

# Load the .env.local file
print("Loading .env.local file...")
load_dotenv("D:/healthcare-translation-app/.env.local")

app = Flask(__name__)
CORS(app)

# Get the API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print(f"GROQ_API_KEY: {GROQ_API_KEY}")  # Debugging line
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


@app.route("/translate", methods=["POST"])
def translate_text():
    try:
        data = request.json
        text = data.get("text", "")
        source_lang = data.get("source_lang", "en")
        target_lang = data.get("target_lang", "es")
        
        if not text:
            return jsonify({"error": "No text provided"}), 400

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "system", "content": "You are a helpful translator."},
                {"role": "user", "content": f"Please translate the following text into {target_lang} and output ONLY the translated text:\n{text}.\nDo NOT include any notes, suggestions or anything else. Just output the translated text ONLY"}
            ],
            "temperature": 0.3
        }

        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        print(f"Response: {response.text}")  # Debugging line
        print(f"Status Code: {response.status_code}")  # Debugging line

        if response.status_code == 200:
            response_data = response.json()
            translated_text = response_data['choices'][0]['message']['content']
            return jsonify({"translated_text": translated_text})
        else:
            return jsonify({"error": "Translation API failed", "details": response.text}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

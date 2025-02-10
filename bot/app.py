from flask import Flask, render_template, jsonify, request
import os
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini
api_key = "AIzaSyBNBgchXs6MmOx-lBQSnovzCoyOuC18MY0"  # Hardcoded API key for testing only
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="Your dyslexia support instructions here..."
)

history = [{"role": "user", "parts": ["hi"]}, {"role": "model", "parts": ["Hello! How can I assist you today?"]}]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    chat_session = model.start_chat(history=history)
    response = chat_session.send_message(user_message)
    
    model_response = response.text
    history.append({"role": "user", "parts": [user_message]})
    history.append({"role": "model", "parts": [model_response]})
    
    return jsonify({"reply": model_response})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify({
        "message": "DoseSafe AI API",
        "status": "operational"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    try:
        from groq import Groq
        
        data = request.json
        message = data.get('message', '')
        
        groq_api_key = os.getenv('GROQ_API_KEY')
        if not groq_api_key:
            return jsonify({"error": "AI service not configured"}), 503
        
        client = Groq(api_key=groq_api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant."},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return jsonify({
            "response": response.choices[0].message.content,
            "success": True
        })
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500

# Vercel serverless function handler
def handler(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()

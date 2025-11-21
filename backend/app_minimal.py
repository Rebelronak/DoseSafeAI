from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from groq import Groq

# Load environment variables
load_dotenv()

app = Flask(__name__)

# CORS configuration
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize Groq client
groq_client = None
try:
    groq_api_key = os.getenv('GROQ_API_KEY')
    if groq_api_key:
        groq_client = Groq(api_key=groq_api_key)
        print("✅ Groq AI client initialized")
    else:
        print("⚠️  GROQ_API_KEY not set")
except Exception as e:
    print(f"⚠️ Groq init failed: {e}")

@app.route('/')
def index():
    return jsonify({
        "message": "DoseSafe AI Backend",
        "status": "operational",
        "version": "1.0-minimal"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/ai-capabilities')
def ai_capabilities():
    return jsonify({
        "groq_available": groq_client is not None,
        "features": ["chatbot"]
    })

@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        data = request.json
        message = data.get('message', '')
        
        if not groq_client:
            return jsonify({"error": "AI service not configured"}), 503
        
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant for DoseSafe AI. Provide helpful information about medications and health."},
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

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

# 🤖 Setting Up AI Chatbot with Groq (Llama)

## Quick Setup Instructions

### 1. Get Groq API Key (Free)
1. Visit [Groq Console](https://console.groq.com/keys)
2. Sign up for a free account
3. Create a new API key
4. Copy the key (starts with `gsk_...`)

### 2. Configure Environment
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Groq API key:
   ```bash
   GROQ_API_KEY=gsk_your_actual_api_key_here
   ```

### 3. Install Requirements
Make sure you have the Groq library installed:
```bash
pip install groq
```

### 4. Test the Setup
Start your backend server and the chatbot should now provide real-time AI responses!

## Features
- ✅ **Real-time responses** using Llama 3.3-70B model
- ✅ **Medical knowledge** specialized for medication questions
- ✅ **Conversation context** maintains chat history
- ✅ **Safety reminders** automatically included
- ✅ **Fallback responses** when API is unavailable

## Groq Benefits
- 🚀 **Fast**: Ultra-low latency responses
- 💰 **Free**: Generous free tier
- 🧠 **Smart**: Llama 3.3-70B model
- 🔒 **Reliable**: High uptime and stability

## Supported Questions
The AI can answer questions about:
- Drug interactions
- Side effects
- Medication storage
- Dosage guidance
- Safety warnings
- General health topics

## Troubleshooting
- **No responses**: Check if GROQ_API_KEY is set correctly
- **Fallback responses**: API might be down, it will retry automatically
- **Error messages**: Check backend logs for detailed error information

The chatbot will automatically fall back to predefined responses if the AI service is unavailable.

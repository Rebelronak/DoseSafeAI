#!/usr/bin/env python3
"""
Test script for Groq AI Chatbot integration
Run this to verify your Groq API setup is working correctly
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_groq_setup():
    """Test Groq API configuration and connectivity"""
    
    print("🧪 Testing DoseSafe AI Chatbot Setup...")
    print("=" * 50)
    
    # Check if API key exists
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("❌ GROQ_API_KEY not found in environment")
        print("📋 Please follow GROQ_SETUP.md instructions")
        return False
    
    if api_key == 'your_groq_api_key_here':
        print("❌ GROQ_API_KEY is still set to placeholder value")
        print("📋 Please replace with your actual API key from https://console.groq.com/keys")
        return False
    
    print(f"✅ GROQ_API_KEY found: {api_key[:10]}...")
    
    # Test Groq library import
    try:
        from groq import Groq
        print("✅ Groq library imported successfully")
    except ImportError:
        print("❌ Groq library not installed")
        print("💡 Run: pip install groq")
        return False
    
    # Test API connectivity
    try:
        client = Groq(api_key=api_key)
        print("✅ Groq client initialized")
        
        # Test a simple API call
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful medical AI assistant."
                },
                {
                    "role": "user", 
                    "content": "What are drug interactions?"
                }
            ],
            model="llama-3.3-70b-versatile",
            max_tokens=100,
            temperature=0.7
        )
        
        response = chat_completion.choices[0].message.content
        print("✅ API call successful")
        print(f"📝 Sample response: {response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {str(e)}")
        print("💡 Check your API key and internet connection")
        return False

def main():
    """Main test function"""
    success = test_groq_setup()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 SUCCESS! Your Groq AI chatbot is ready to use!")
        print("🚀 Start your backend server and try the chatbot")
    else:
        print("😞 Setup incomplete. Please check the issues above.")
        print("📖 See GROQ_SETUP.md for detailed instructions")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())

#!/bin/bash
# DoseSafe-AI Production Deployment Script
# Run this script to deploy the complete system

echo "🏥 DoseSafe-AI Production Deployment"
echo "======================================"

# Check Python version
echo "📋 Checking Python version..."
python --version
if [ $? -ne 0 ]; then
    echo "❌ Python not found. Please install Python 3.13+"
    exit 1
fi

# Check Node.js version
echo "📋 Checking Node.js version..."
node --version
if [ $? -ne 0 ]; then
    echo "❌ Node.js not found. Please install Node.js 16+"
    exit 1
fi

# Create virtual environment
echo "🔧 Creating Python virtual environment..."
python -m venv dosesafe_env

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source dosesafe_env/bin/activate  # Linux/Mac
# dosesafe_env\Scripts\activate  # Windows

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd frontend
npm install
cd ..

# Build frontend for production
echo "🏗️ Building frontend for production..."
cd frontend
npm run build
cd ..

# Set up environment variables
echo "🔐 Setting up environment variables..."
if [ ! -f .env ]; then
    echo "GROQ_API_KEY=your_groq_api_key_here" > .env
    echo "FLASK_ENV=production" >> .env
    echo "DEBUG=False" >> .env
    echo "⚠️ Please update .env with your actual API keys"
fi

# Check ML models
echo "🤖 Checking ML models..."
if [ -d "ml_models/models" ]; then
    echo "✅ ML models found"
else
    echo "⚠️ Training ML models..."
    cd ml_models
    python comprehensive_trainer_fixed.py
    cd ..
fi

# Check Tesseract installation
echo "👁️ Checking Tesseract OCR..."
tesseract --version
if [ $? -ne 0 ]; then
    echo "⚠️ Tesseract not found. Please install Tesseract OCR"
    echo "   Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki"
    echo "   Linux: sudo apt-get install tesseract-ocr"
    echo "   Mac: brew install tesseract"
fi

echo "🎉 Deployment setup complete!"
echo "📋 Next steps:"
echo "   1. Update .env with your API keys"
echo "   2. Run: python start_production.py"
echo "   3. Open: http://localhost:5000"

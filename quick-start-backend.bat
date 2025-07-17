@echo off
echo 🚀 DoseSafe AI - Quick Setup Script
echo =====================================

cd /d "E:\DoseSafe-AI\backend"

echo.
echo 🔍 Checking Python installation...
python --version
if %ERRORLEVEL% neq 0 (
    echo ❌ Python not found! Please install Python from python.org
    echo 📥 Download: https://python.org/downloads/
    pause
    exit /b 1
)

echo.
echo 📦 Installing dependencies globally (quick setup)...
echo ⚠️  Note: This installs packages globally. For production, use virtual environment.

pip install --upgrade pip
pip install Flask==2.3.3 flask-cors==4.0.0 python-dotenv==1.0.0 requests==2.31.0
pip install Pillow==10.0.1 pytesseract==0.3.10
pip install pandas==2.0.3 numpy==1.24.3

echo.
echo 🎯 Skipping heavy ML packages for quick testing...
echo 💡 You can install them later: easyocr, opencv-python, torch, spacy

echo.
echo 🔧 Creating .env file...
if not exist ".env" (
    echo # Quick Setup Environment > .env
    echo FLASK_APP=app.py >> .env
    echo FLASK_ENV=development >> .env
    echo FLASK_DEBUG=True >> .env
    echo CORS_ORIGINS=http://localhost:5173,http://localhost:3000 >> .env
    echo Created basic .env file
)

echo.
echo 📁 Creating required directories...
if not exist "uploads" mkdir uploads

echo.
echo ✅ Quick setup complete!
echo.
echo 🚀 Starting Flask server...
echo 🌐 Backend will be available at: http://localhost:5000
echo 🔗 Test endpoint: http://localhost:5000/health
echo.

python app.py

pause

@echo off
REM DoseSafe-AI Windows Production Deployment Script

echo 🏥 DoseSafe-AI Production Deployment
echo ======================================

REM Check Python version
echo 📋 Checking Python version...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.13+
    pause
    exit /b 1
)

REM Check Node.js version
echo 📋 Checking Node.js version...
node --version
if %errorlevel% neq 0 (
    echo ❌ Node.js not found. Please install Node.js 16+
    pause
    exit /b 1
)

REM Create virtual environment
echo 🔧 Creating Python virtual environment...
python -m venv dosesafe_env

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call dosesafe_env\Scripts\activate

REM Install Python dependencies
echo 📦 Installing Python dependencies...
cd backend
pip install -r requirements.txt
cd ..

REM Install Node.js dependencies
echo 📦 Installing Node.js dependencies...
cd frontend
npm install
cd ..

REM Build frontend for production
echo 🏗️ Building frontend for production...
cd frontend
npm run build
cd ..

REM Set up environment variables
echo 🔐 Setting up environment variables...
if not exist .env (
    echo GROQ_API_KEY=your_groq_api_key_here > .env
    echo FLASK_ENV=production >> .env
    echo DEBUG=False >> .env
    echo ⚠️ Please update .env with your actual API keys
)

REM Check ML models
echo 🤖 Checking ML models...
if exist "ml_models\models" (
    echo ✅ ML models found
) else (
    echo ⚠️ Training ML models...
    cd ml_models
    python comprehensive_trainer_fixed.py
    cd ..
)

REM Check Tesseract installation
echo 👁️ Checking Tesseract OCR...
tesseract --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Tesseract not found. Please install Tesseract OCR
    echo    Download from: https://github.com/UB-Mannheim/tesseract/wiki
)

echo 🎉 Deployment setup complete!
echo 📋 Next steps:
echo    1. Update .env with your API keys
echo    2. Run: python start_production.py
echo    3. Open: http://localhost:5000

pause

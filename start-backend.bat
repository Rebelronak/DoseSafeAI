@echo off
echo Starting DoseSafe AI Backend...
cd /d "e:\DoseSafe-AI\backend"

echo Checking if virtual environment exists...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing/updating dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Installing spaCy model...
python -m spacy download en_core_web_sm

echo Creating .env file if it doesn't exist...
if not exist ".env" (
    copy ".env.example" ".env"
    echo Created .env file from example. Please update it with your API keys.
)

echo.
echo ========================================
echo Starting Flask server...
echo ========================================
echo Backend will be available at: http://localhost:5000
echo Test endpoint: http://localhost:5000/test/scan
echo.

python app.py

pause

@echo off
echo ========================================
echo    DoseSafe AI - Backend Quick Setup
echo ========================================
echo.

:: Check if we're in the right directory
if not exist "backend\app.py" (
    echo ERROR: Please run this script from the DoseSafe-AI root directory
    echo Current directory: %CD%
    echo Expected file: backend\app.py
    pause
    exit /b 1
)

:: Navigate to backend directory
cd backend

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from https://python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

:: Show Python location to verify it's not Windows Store
echo Python found at:
where python

:: Check if it's Windows Store Python (problematic)
where python | findstr "WindowsApps" >nul
if not errorlevel 1 (
    echo.
    echo WARNING: You're using Windows Store Python which has limitations
    echo For best results, install Python from https://python.org/downloads/
    echo.
    echo Continuing anyway...
    timeout /t 3
)

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing minimal requirements globally...
echo (Virtual environment creation is skipped due to Windows Store Python issues)
python -m pip install -r requirements-minimal.txt

if errorlevel 1 (
    echo.
    echo Installation failed. Trying alternative approach...
    echo Installing each package individually...
    
    python -m pip install flask
    python -m pip install flask-cors
    python -m pip install pillow
    python -m pip install pytesseract
    python -m pip install opencv-python
    python -m pip install pandas
    python -m pip install scikit-learn
    python -m pip install numpy
)

echo.
echo ========================================
echo Starting DoseSafe AI Backend Server...
echo ========================================
echo Server will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

:: Start the Flask application
python app.py

pause

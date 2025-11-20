@echo off
echo =====================================
echo  DoseSafe AI - Windows Python Fix
echo =====================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found in PATH
    echo Please install Python from python.org (NOT Windows Store)
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo Checking if this is Windows Store Python...
python -c "import sys; print('Windows Store Python detected' if 'WindowsApps' in sys.executable else 'Regular Python installation')"

echo.
echo Attempting to upgrade pip...
python -m pip install --upgrade pip

echo.
echo Installing Flask and essential packages globally...
python -m pip install flask flask-cors requests python-dotenv

echo.
echo Testing Flask installation...
python -c "import flask; print('Flask version:', flask.__version__)"
if %errorlevel% neq 0 (
    echo ERROR: Flask installation failed
    pause
    exit /b 1
)

echo.
echo =====================================
echo  Flask installed successfully!
echo =====================================
echo.
echo You can now run the backend with:
echo   cd backend
echo   python app.py
echo.
pause

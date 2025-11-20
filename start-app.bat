@echo off
echo Starting Complete DoseSafe AI Application...

echo.
echo ========================================
echo Starting Backend Server...
echo ========================================
start "DoseSafe Backend" cmd /k "cd /d e:\DoseSafe-AI && start-backend.bat"

echo Waiting 10 seconds for backend to initialize...
timeout /t 10 /nobreak

echo.
echo ========================================
echo Starting Frontend Server...
echo ========================================
start "DoseSafe Frontend" cmd /k "cd /d e:\DoseSafe-AI && start-frontend.bat"

echo.
echo ========================================
echo DoseSafe AI is starting up!
echo ========================================
echo Backend: http://localhost:5000
echo Frontend: http://localhost:5173
echo.
echo Both servers are starting in separate windows.
echo Wait for both servers to fully load before using the application.
echo.

pause

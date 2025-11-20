@echo off
echo ========================================
echo    DoseSafe AI - Frontend Hot Refresh
echo ========================================
echo.

echo Clearing npm cache...
cd E:\DoseSafe-AI\frontend
npm cache clean --force

echo.
echo Removing node_modules cache...
if exist node_modules (
    rmdir /s /q node_modules
)

echo.
echo Reinstalling dependencies...
npm install

echo.
echo Starting development server with fresh cache...
npm run dev

pause

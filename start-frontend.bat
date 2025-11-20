@echo off
echo Starting DoseSafe AI Frontend...
cd /d "e:\DoseSafe-AI\frontend"

echo Installing/updating dependencies...
npm install

echo Starting Vite development server...
npm run dev

pause

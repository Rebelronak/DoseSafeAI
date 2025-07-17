# 🏥 DoseSafe AI - Quick Start Guide

DoseSafe AI is an intelligent medication safety platform that uses AI to analyze prescriptions and detect drug interactions.

## 🚀 Quick Start (Easiest Method)

### Option 1: One-Click Start
1. Double-click `start-app.bat` in the root directory
2. Wait for both servers to start (backend: port 5000, frontend: port 5173)
3. Open http://localhost:5173 in your browser

### Option 2: Manual Start

#### Backend (Terminal 1)
```powershell
cd "e:\DoseSafe-AI\backend"
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python app.py
```

#### Frontend (Terminal 2)
```powershell
cd "e:\DoseSafe-AI\frontend"
npm install
npm run dev
```

## 🛠️ Development Setup

### Prerequisites
- **Node.js 18+**: https://nodejs.org/
- **Python 3.8+**: https://python.org/
- **Git** (optional): https://git-scm.com/

### Environment Setup
1. Copy `backend/.env.example` to `backend/.env`
2. Add your API keys (optional for basic functionality)

### Project Structure
```
DoseSafe-AI/
├── backend/           # Flask API server
│   ├── app.py        # Main Flask application
│   ├── routes/       # API endpoints
│   ├── services/     # Business logic
│   └── requirements.txt
├── frontend/          # React + Vite application
│   ├── src/
│   │   ├── pages/    # React pages
│   │   ├── components/ # Reusable components
│   │   └── services/ # API calls
│   └── package.json
└── ml_models/         # AI/ML models and training
```

## 🌐 Access Points
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **API Docs**: http://localhost:5000/api/docs (when implemented)

## 🔧 Troubleshooting

### Common Issues
1. **Port 5173 already in use**: Frontend will use next available port
2. **Port 5000 already in use**: Change port in `backend/app.py`
3. **Module not found**: Ensure virtual environment is activated
4. **CORS errors**: Check backend/.env CORS_ORIGINS setting

### Dependencies Issues
```powershell
# Backend dependency issues
cd backend
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# Frontend dependency issues
cd frontend
npm ci
# or
rm -rf node_modules package-lock.json
npm install
```

## 📱 Application Features
- 📸 **Prescription Scanning**: Upload images or PDFs
- ✍️ **Manual Entry**: Enter medications manually
- 🔍 **Drug Interaction Detection**: AI-powered analysis
- 💬 **AI Chatbot**: Ask medication questions
- 📊 **Results Dashboard**: Comprehensive safety reports
- 📚 **Previous Scans**: History and tracking

## 🛡️ Safety Notice
This application is for educational purposes. Always consult healthcare professionals for medical advice.

## 📞 Support
For issues or questions, check the troubleshooting section above or create an issue in the repository.

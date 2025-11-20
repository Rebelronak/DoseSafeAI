"""
DoseSafe-AI Production Startup Script
Combines frontend and backend in production mode
"""

import os
import sys
import subprocess
import threading
import time
from pathlib import Path

def start_backend():
    """Start the Flask backend server"""
    print("🔄 Starting DoseSafe-AI Backend...")
    
    # Change to backend directory
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    
    # Set production environment
    os.environ["FLASK_ENV"] = "production"
    os.environ["DEBUG"] = "False"
    
    # Start Flask server
    subprocess.run([sys.executable, "app.py"], check=True)

def start_frontend():
    """Start the React frontend server"""
    print("🔄 Starting DoseSafe-AI Frontend...")
    
    # Change to frontend directory
    frontend_dir = Path(__file__).parent / "frontend"
    os.chdir(frontend_dir)
    
    # Start React development server or serve build
    try:
        # Try to serve production build
        subprocess.run(["npx", "serve", "-s", "build", "-l", "3000"], check=True)
    except subprocess.CalledProcessError:
        # Fallback to development server
        print("⚠️ Production build not found, starting development server...")
        subprocess.run(["npm", "start"], check=True)

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("📋 Checking dependencies...")
    
    # Check Python packages
    try:
        import flask
        import pandas
        import sklearn
        import pytesseract
        import groq
        print("✅ Python dependencies OK")
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        print("💡 Run: pip install -r backend/requirements.txt")
        return False
    
    # Check Tesseract
    try:
        subprocess.run(["tesseract", "--version"], capture_output=True, check=True)
        print("✅ Tesseract OCR OK")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Tesseract OCR not found")
        print("💡 Install from: https://github.com/UB-Mannheim/tesseract/wiki")
        return False
    
    # Check environment variables
    if not os.getenv("GROQ_API_KEY"):
        print("⚠️ GROQ_API_KEY not set in environment")
        print("💡 Add your API key to .env file")
    
    return True

def main():
    """Main startup function"""
    print("🏥 DoseSafe-AI Production Startup")
    print("=" * 50)
    
    # Check dependencies first
    if not check_dependencies():
        print("❌ Dependency check failed. Please fix issues above.")
        return
    
    # Check if ML models exist
    models_dir = Path(__file__).parent / "ml_models" / "models"
    if not models_dir.exists():
        print("⚠️ ML models not found. Training models...")
        ml_dir = Path(__file__).parent / "ml_models"
        os.chdir(ml_dir)
        subprocess.run([sys.executable, "comprehensive_trainer_fixed.py"])
        os.chdir(Path(__file__).parent)
    
    print("🚀 Starting DoseSafe-AI...")
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait for backend to start
    time.sleep(3)
    
    print("🌐 System ready!")
    print("📍 Backend: http://localhost:5000")
    print("📍 Frontend: http://localhost:3000")
    print("📖 API Docs: http://localhost:5000/ai-capabilities")
    print("\n💡 Upload a prescription image to test the system!")
    print("🛑 Press Ctrl+C to stop")
    
    try:
        # Start frontend (this will block)
        start_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down DoseSafe-AI...")

if __name__ == "__main__":
    main()

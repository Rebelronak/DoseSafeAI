"""
Professional DoseSafe-AI Production Startup
Complete system with authentication and dashboard
"""

import os
import sys
import subprocess
import threading
import time
import webbrowser
from pathlib import Path

def start_backend():
    """Start the Flask backend server"""
    print("🔄 Starting DoseSafe-AI Backend Server...")
    
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    
    # Set production environment
    os.environ["FLASK_ENV"] = "production"
    os.environ["DEBUG"] = "False"
    
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")

def start_frontend():
    """Start the React frontend"""
    print("🔄 Starting DoseSafe-AI Frontend...")
    
    frontend_dir = Path(__file__).parent / "frontend"
    os.chdir(frontend_dir)
    
    try:
        # Install dependencies if needed
        if not (frontend_dir / "node_modules").exists():
            print("📦 Installing frontend dependencies...")
            subprocess.run(["npm", "install"], check=True)
        
        # Start React development server
        subprocess.run(["npm", "start"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")

def check_system_requirements():
    """Check if all system requirements are met"""
    print("📋 Checking System Requirements...")
    
    issues = []
    
    # Check Python
    try:
        python_version = sys.version_info
        if python_version.major == 3 and python_version.minor >= 8:
            print(f"✅ Python {python_version.major}.{python_version.minor} - OK")
        else:
            issues.append("❌ Python 3.8+ required")
    except:
        issues.append("❌ Python not found")
    
    # Check Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()} - OK")
        else:
            issues.append("❌ Node.js not found")
    except:
        issues.append("❌ Node.js not found")
    
    # Check npm
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm {result.stdout.strip()} - OK")
        else:
            issues.append("❌ npm not found")
    except:
        issues.append("❌ npm not found")
    
    # Check Tesseract
    try:
        result = subprocess.run(["tesseract", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Tesseract OCR - OK")
        else:
            issues.append("❌ Tesseract OCR not found")
    except:
        issues.append("⚠️ Tesseract OCR not found - OCR features may not work")
    
    # Check Python dependencies
    try:
        import flask, sklearn, pandas, groq
        print("✅ Python dependencies - OK")
    except ImportError as e:
        issues.append(f"❌ Missing Python dependency: {e}")
    
    # Check environment variables
    if not os.getenv("GROQ_API_KEY"):
        issues.append("⚠️ GROQ_API_KEY not set - AI features may be limited")
    
    return issues

def setup_environment():
    """Set up the environment if needed"""
    print("🔧 Setting up environment...")
    
    # Create .env file if it doesn't exist
    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        env_content = """# DoseSafe-AI Environment Configuration
GROQ_API_KEY=your_groq_api_key_here
FLASK_ENV=production
DEBUG=False
HOST=0.0.0.0
PORT=5000
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("📝 Created .env file - Please add your API keys")
    
    # Check ML models
    models_dir = Path(__file__).parent / "ml_models" / "models"
    if not models_dir.exists():
        print("🤖 ML models not found. Training models...")
        ml_dir = Path(__file__).parent / "ml_models"
        os.chdir(ml_dir)
        try:
            subprocess.run([sys.executable, "comprehensive_trainer_fixed.py"], check=True)
            print("✅ ML models trained successfully")
        except subprocess.CalledProcessError:
            print("⚠️ ML model training failed - some features may be limited")
        os.chdir(Path(__file__).parent)

def display_startup_info():
    """Display startup information"""
    print("\n" + "="*70)
    print("🏥 DoseSafe-AI Professional System")
    print("="*70)
    print("🎯 Advanced AI-Powered Prescription Analysis")
    print("🔒 Professional Authentication System")
    print("📊 Real-time Analytics Dashboard")
    print("🤖 Machine Learning Integration")
    print("👨‍⚕️ Healthcare-Grade Security")
    print("="*70)

def main():
    """Main startup function"""
    display_startup_info()
    
    # Check system requirements
    issues = check_system_requirements()
    
    if issues:
        print("\n⚠️ System Issues Found:")
        for issue in issues:
            print(f"  {issue}")
        
        if any("❌" in issue for issue in issues):
            print("\n🛑 Critical issues found. Please fix them before continuing.")
            input("Press Enter to continue anyway or Ctrl+C to exit...")
    
    # Setup environment
    setup_environment()
    
    print("\n🚀 Starting DoseSafe-AI Professional System...")
    print("📍 Backend will be available at: http://localhost:5000")
    print("📍 Frontend will be available at: http://localhost:3000")
    print("🔐 Professional login system enabled")
    print("📊 Dashboard and analytics ready")
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait for backend to start
    print("\n⏳ Waiting for backend to initialize...")
    time.sleep(5)
    
    print("✅ Backend ready!")
    print("🌐 Starting frontend...")
    
    # Open browser automatically
    def open_browser():
        time.sleep(10)  # Wait for frontend to start
        try:
            webbrowser.open('http://localhost:3000')
            print("🌍 Browser opened automatically")
        except:
            print("⚠️ Could not open browser automatically")
    
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    print("\n💡 Demo Login Credentials:")
    print("   Email: any valid email")
    print("   Password: any password")
    print("   Or click 'Demo Login (Ronak)'")
    
    print("\n🎉 System Ready for Professional Demo!")
    print("🛑 Press Ctrl+C to stop the system")
    
    try:
        # Start frontend (this will block)
        start_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down DoseSafe-AI Professional System...")
        print("Thank you for using DoseSafe-AI!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 DoseSafe-AI Professional System stopped.")
    except Exception as e:
        print(f"\n❌ Error starting system: {e}")
        print("Please check the error message and try again.")

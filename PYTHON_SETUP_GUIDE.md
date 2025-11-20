# 🐍 Python Setup Guide for Windows

## The Problem
You're encountering the **Windows Store Python issue** which prevents creating virtual environments properly. This is a very common problem on Windows systems.

## 🚀 Quick Fix - Use Our Automated Scripts

We've created scripts that automatically handle the Python issues:

### Option 1: Batch Script (Recommended)
```cmd
cd E:\DoseSafe-AI
.\fix-python-and-start.bat
```

### Option 2: PowerShell Script (More Detailed)
```powershell
cd E:\DoseSafe-AI
.\fix-python-and-start.ps1
```

## ✅ Manual Solution: Install Python from python.org

### Step 1: Download Python from python.org
1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or 3.12 (recommended for stability)
3. **IMPORTANT**: During installation, check "Add Python to PATH"
4. Choose "Install for all users" if possible
5. **CRITICAL**: Uninstall Windows Store Python first if present

### Step 2: Verify Installation
Open a NEW PowerShell window and run:
```powershell
python --version
where python
```
You should see something like:
```
Python 3.11.x
C:\Program Files\Python311\python.exe  # NOT WindowsApps path
```

### Step 3: Install Backend Dependencies (Global Method)
Since venv isn't working with Windows Store Python, install globally:
```powershell
cd E:\DoseSafe-AI\backend
python -m pip install --upgrade pip
python -m pip install -r requirements-minimal.txt
```

### Step 4: Start the Backend
```powershell
python app.py
```

## 🐋 Docker Alternative (If Above Doesn't Work)
If Python installation is still problematic:
```powershell
# Install Docker Desktop from docker.com
# Then run:
docker-compose up
```

## 🔧 Troubleshooting

### If you still see WindowsApps Python:
1. Remove Python from Windows Store (optional)
2. Add the new Python to PATH manually:
   - Open System Properties → Environment Variables
   - Add `C:\Program Files\Python311` to PATH
   - Add `C:\Program Files\Python311\Scripts` to PATH

### If pip install fails:
```powershell
python -m pip install --upgrade pip setuptools wheel
python -m pip install Flask flask-cors python-dotenv requests Pillow
```

### Check what Python you're using:
```powershell
python -c "import sys; print(sys.executable)"
```

## 📞 Need Help?
If you're still having issues, try the Docker method or let us know the output of:
```powershell
python --version
where python
python -c "import sys; print(sys.executable)"
```

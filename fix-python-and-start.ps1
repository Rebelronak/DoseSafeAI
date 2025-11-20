# DoseSafe AI - Python Environment Fixer and Backend Starter
# This script diagnoses Python issues and starts the backend

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    DoseSafe AI - Python Environment Fixer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "backend\app.py")) {
    Write-Host "ERROR: Please run this script from the DoseSafe-AI root directory" -ForegroundColor Red
    Write-Host "Current directory: $PWD" -ForegroundColor Yellow
    Write-Host "Expected file: backend\app.py" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Function to check Python installation
function Test-PythonInstallation {
    Write-Host "Checking Python installation..." -ForegroundColor Yellow
    
    try {
        $pythonVersion = python --version 2>&1
        $pythonPath = (Get-Command python -ErrorAction Stop).Source
        
        Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
        Write-Host "✓ Python location: $pythonPath" -ForegroundColor Green
        
        # Check if it's Windows Store Python
        if ($pythonPath -like "*WindowsApps*") {
            Write-Host "⚠ WARNING: You're using Windows Store Python" -ForegroundColor Yellow
            Write-Host "  This version has limitations with virtual environments" -ForegroundColor Yellow
            Write-Host "  Recommendation: Install Python from https://python.org/downloads/" -ForegroundColor Yellow
            Write-Host ""
            return $false
        }
        
        return $true
    }
    catch {
        Write-Host "✗ Python not found or not in PATH" -ForegroundColor Red
        Write-Host "  Please install Python from https://python.org/downloads/" -ForegroundColor Yellow
        Write-Host "  Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
        return $false
    }
}

# Function to install packages
function Install-PythonPackages {
    Write-Host "Installing Python packages..." -ForegroundColor Yellow
    
    # Navigate to backend
    Set-Location backend
    
    # Upgrade pip first
    Write-Host "Upgrading pip..." -ForegroundColor Cyan
    python -m pip install --upgrade pip
    
    # Try to install from requirements
    Write-Host "Installing from requirements-minimal.txt..." -ForegroundColor Cyan
    $installResult = python -m pip install -r requirements-minimal.txt
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Requirements installation failed. Installing packages individually..." -ForegroundColor Yellow
        
        $packages = @(
            "flask",
            "flask-cors", 
            "pillow",
            "pytesseract",
            "opencv-python",
            "pandas",
            "scikit-learn",
            "numpy"
        )
        
        foreach ($package in $packages) {
            Write-Host "Installing $package..." -ForegroundColor Cyan
            python -m pip install $package
        }
    }
    
    Write-Host "✓ Package installation completed" -ForegroundColor Green
}

# Function to start the backend
function Start-Backend {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "    Starting DoseSafe AI Backend Server" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Server will be available at: http://localhost:5000" -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
    Write-Host ""
    
    # Start Flask application
    python app.py
}

# Main execution
try {
    $pythonOk = Test-PythonInstallation
    
    if (-not $pythonOk) {
        Write-Host ""
        Write-Host "Would you like to continue anyway? (Y/N)" -ForegroundColor Yellow
        $continue = Read-Host
        if ($continue -ne "Y" -and $continue -ne "y") {
            exit 1
        }
    }
    
    Install-PythonPackages
    Start-Backend
}
catch {
    Write-Host "An error occurred: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}
finally {
    # Return to original directory
    Set-Location $PSScriptRoot
}

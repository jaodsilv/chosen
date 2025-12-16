# Setup script for CHOSEN v2
# This script sets up the development environment on Windows

$ErrorActionPreference = "Stop"

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "CHOSEN v2 - Setup Script" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found $pythonVersion" -ForegroundColor Green

    $versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
    if ($versionMatch) {
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 11)) {
            Write-Host "Error: Python 3.11+ is required" -ForegroundColor Red
            exit 1
        }
    }
} catch {
    Write-Host "Error: Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Navigate to project root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir
Set-Location $projectRoot

# 1. Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists. Skipping creation." -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "Virtual environment created." -ForegroundColor Green
}

# Activate virtual environment
& .\venv\Scripts\Activate.ps1

# 2. Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
pip install --upgrade pip

# 3. Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r backend\requirements.txt
pip install -r backend\requirements-dev.txt
Write-Host "Dependencies installed." -ForegroundColor Green

# 4. Setup pre-commit hooks
Write-Host ""
Write-Host "Setting up pre-commit hooks..." -ForegroundColor Yellow
pre-commit install
Write-Host "Pre-commit hooks installed." -ForegroundColor Green

# 5. Create data directories
Write-Host ""
Write-Host "Creating data directories..." -ForegroundColor Yellow
$dirs = @("data\conversations", "data\settings", "data\cache", "data\metadata", "logs")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}
Write-Host "Data directories created." -ForegroundColor Green

# 6. Copy environment file
Write-Host ""
Write-Host "Setting up environment..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env file from .env.example" -ForegroundColor Green
    Write-Host "IMPORTANT: Please edit .env with your Anthropic API key" -ForegroundColor Yellow
} else {
    Write-Host ".env file already exists. Skipping." -ForegroundColor Yellow
}

# 7. Check git-crypt
Write-Host ""
Write-Host "Checking git-crypt..." -ForegroundColor Yellow
try {
    $gitCryptVersion = git-crypt --version 2>&1
    Write-Host "git-crypt is installed." -ForegroundColor Green
    if (-not (Test-Path ".git-crypt")) {
        Write-Host "git-crypt not initialized. Run 'git-crypt init' to initialize encryption." -ForegroundColor Yellow
    } else {
        Write-Host "git-crypt is already initialized." -ForegroundColor Green
    }
} catch {
    Write-Host "git-crypt not found. Install it for data encryption:" -ForegroundColor Yellow
    Write-Host "  scoop install git-crypt" -ForegroundColor White
}

Write-Host ""
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Edit .env file with your Anthropic API key"
Write-Host "2. Activate virtual environment: .\venv\Scripts\Activate.ps1"
Write-Host "3. Start the server: cd backend; uvicorn app.main:app --reload"
Write-Host "4. Visit http://localhost:8000/api/docs for API documentation"
Write-Host ""

# PowerShell script to set up iFarm development environment
# Usage: .\setup.ps1
# Run with: Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup.ps1

param(
    [string]$DbUrl = "",
    [string]$SecretKey = ""
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "iFarm Development Environment Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check Python is installed
Write-Host "`nChecking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if (-not $?) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}
Write-Host "Found: $pythonVersion" -ForegroundColor Green

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($?) {
        Write-Host "Virtual environment created successfully" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "`nVirtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "`nUpgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install requirements
Write-Host "`nInstalling dependencies from requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($?) {
    Write-Host "Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Create .env file if it doesn't exist
if (-not (Test-Path "config\.env")) {
    Write-Host "`nCreating config/.env from .env.example..." -ForegroundColor Yellow
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" "config\.env"
        Write-Host "Created config/.env" -ForegroundColor Green
        Write-Host "UPDATE config/.env with your actual database and secret key!" -ForegroundColor Magenta
    } else {
        Write-Host "WARNING: .env.example not found" -ForegroundColor Yellow
    }
} else {
    Write-Host "`nconfig/.env already exists" -ForegroundColor Green
}

# Optional: Set environment variables if provided as arguments
if ($DbUrl) {
    Write-Host "`nUpdating DATABASE_URL in config/.env..." -ForegroundColor Yellow
    # (Simple replacement - for production use a config management tool)
    $content = Get-Content "config\.env"
    $content = $content -replace 'DATABASE_URL=.*', "DATABASE_URL=$DbUrl"
    Set-Content "config\.env" $content
    Write-Host "DATABASE_URL updated" -ForegroundColor Green
}

if ($SecretKey) {
    Write-Host "`nUpdating SECRET_KEY in config/.env..." -ForegroundColor Yellow
    $content = Get-Content "config\.env"
    $content = $content -replace 'SECRET_KEY=.*', "SECRET_KEY=$SecretKey"
    Set-Content "config\.env" $content
    Write-Host "SECRET_KEY updated" -ForegroundColor Green
}

# Display next steps
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Edit config/.env with your database credentials" -ForegroundColor White
Write-Host "2. Run migrations: flask db upgrade" -ForegroundColor White
Write-Host "3. Start the server: python run.py" -ForegroundColor White
Write-Host "`nVirtual environment is already activated!" -ForegroundColor Green
Write-Host "`nTo deactivate later, run: deactivate" -ForegroundColor Gray

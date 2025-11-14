#!/bin/bash

# Bash script to set up iFarm development environment (macOS/Linux)
# Usage: bash setup.sh
# Or: chmod +x setup.sh && ./setup.sh

set -e  # Exit on error

echo "========================================"
echo "iFarm Development Environment Setup"
echo "========================================"

# Check Python is installed
echo -e "\nChecking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "Found: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "\nCreating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created successfully"
else
    echo -e "\nVirtual environment already exists"
fi

# Activate virtual environment
echo -e "\nActivating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo -e "\nUpgrading pip..."
python -m pip install --upgrade pip > /dev/null

# Install requirements
echo -e "\nInstalling dependencies from requirements.txt..."
pip install -r requirements.txt
echo "Dependencies installed successfully"

# Create .env file if it doesn't exist
if [ ! -f "config/.env" ]; then
    echo -e "\nCreating config/.env from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example config/.env
        echo "Created config/.env"
        echo "UPDATE config/.env with your actual database and secret key!"
    else
        echo "WARNING: .env.example not found"
    fi
else
    echo -e "\nconfig/.env already exists"
fi

# Display next steps
echo -e "\n========================================"
echo "Setup Complete!"
echo "========================================"
echo -e "\nNext steps:"
echo "1. Edit config/.env with your database credentials"
echo "2. Run migrations: flask db upgrade"
echo "3. Start the server: python run.py"
echo -e "\nVirtual environment is already activated!"
echo "To deactivate later, run: deactivate"

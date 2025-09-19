# Quick virtual environment setup for Windows
# Usage: .\quickstart.ps1

# Check if venv exists, create if not
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..."
& .\venv\Scripts\Activate.ps1

Write-Host "Virtual environment activated."
Write-Host "Run 'deactivate' to exit."
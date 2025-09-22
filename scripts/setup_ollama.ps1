# Setup Ollama model from .env configuration
# Reads MODEL_NAME from .env file

Write-Host "==============================" -ForegroundColor Cyan
Write-Host "  Ollama Model Setup" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "Error: .env file not found." -ForegroundColor Red
    Write-Host "Please create a .env file with MODEL_NAME=your_model"
    exit 1
}

# Read MODEL_NAME from .env file
$envContent = Get-Content ".env"
$modelLine = $envContent | Where-Object { $_ -match "^MODEL_NAME=" }

if (-not $modelLine) {
    Write-Host "Error: MODEL_NAME not found in .env file." -ForegroundColor Red
    Write-Host "Please add MODEL_NAME=your_model to .env file"
    exit 1
}

$MODEL_NAME = $modelLine -replace "MODEL_NAME=", "" -replace '"', '' -replace ' ', ''

if ([string]::IsNullOrWhiteSpace($MODEL_NAME)) {
    Write-Host "Error: MODEL_NAME is empty in .env file." -ForegroundColor Red
    exit 1
}

Write-Host "Model configured: $MODEL_NAME" -ForegroundColor Green

# Check if Ollama is installed
$ollamaCommand = Get-Command ollama -ErrorAction SilentlyContinue

if (-not $ollamaCommand) {
    Write-Host "Error: Ollama is not installed." -ForegroundColor Red
    Write-Host "Please install Ollama first:"
    Write-Host "  Download from: https://ollama.ai/download"
    exit 1
}

# Check if model already exists
$modelList = ollama list 2>$null
$modelExists = $modelList | Select-String -Pattern "^$MODEL_NAME"

ollama pull $MODEL_NAME
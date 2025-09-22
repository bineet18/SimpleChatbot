: ===========================
:: scripts\setup_ollama.bat
:: ===========================
@echo off
:: Setup Ollama model from .env configuration
:: Reads MODEL_NAME from .env file

echo ==============================
echo   Ollama Model Setup
echo ==============================

:: Check if .env file exists
if not exist ".env" (
    echo Error: .env file not found.
    echo Please create a .env file with MODEL_NAME=your_model
    exit /b 1
)

:: Read MODEL_NAME from .env file
set "MODEL_NAME="
for /f "tokens=1,* delims==" %%a in ('findstr /b "MODEL_NAME=" .env') do (
    set "MODEL_NAME=%%b"
)

:: Remove quotes and spaces from MODEL_NAME
set MODEL_NAME=%MODEL_NAME:"=%
set MODEL_NAME=%MODEL_NAME: =%

if "%MODEL_NAME%"=="" (
    echo Error: MODEL_NAME not found in .env file.
    echo Please add MODEL_NAME=your_model to .env file
    exit /b 1
)

echo Model configured: %MODEL_NAME%

:: Check if Ollama is installed
where ollama >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Ollama is not installed.
    echo Please install Ollama first:
    echo   Download from: https://ollama.ai/download
    exit /b 1
)

:: Check if model already exists
for /f "delims=" %%i in ('ollama list 2^>nul ^| findstr /b "%MODEL_NAME%"') do set "modelExists=%%i"

ollama pull %MODEL_NAME%
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

ollama pull %MODEL_NAME%
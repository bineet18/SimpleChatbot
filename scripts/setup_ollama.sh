#!/bin/bash

# Setup Ollama model from .env configuration
# Reads MODEL_NAME from .env file

echo "=============================="
echo "  Ollama Model Setup"
echo "=============================="

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Error: .env file not found."
    echo "Please create a .env file with MODEL_NAME=your_model"
    exit 1
fi

# Read MODEL_NAME from .env file
MODEL_NAME=$(grep "^MODEL_NAME=" .env | cut -d'=' -f2 | tr -d '"' | tr -d ' ')

if [ -z "$MODEL_NAME" ]; then
    echo "Error: MODEL_NAME not found in .env file."
    echo "Please add MODEL_NAME=your_model to .env file"
    exit 1
fi

echo "Model configured: $MODEL_NAME"

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Error: Ollama is not installed."
    echo "Please install Ollama first:"
    echo "  macOS: brew install ollama"
    echo "  Linux: curl -fsSL https://ollama.ai/install.sh | sh"
    exit 1
fi

# Check if model already exists
if ollama list | grep -q "^$MODEL_NAME"; then
    echo "✓ Model '$MODEL_NAME' is already available."
    echo "Setup complete!"
else
    echo "Model '$MODEL_NAME' not found locally."
    echo "Pulling model '$MODEL_NAME'..."
    ollama pull "$MODEL_NAME"
    
    if [ $? -eq 0 ]; then
        echo "✓ Successfully pulled '$MODEL_NAME'"
        echo "Setup complete!"
    else
        echo "Error: Failed to pull model '$MODEL_NAME'"
        echo "Please check the model name and try again."
        exit 1
    fi
fi
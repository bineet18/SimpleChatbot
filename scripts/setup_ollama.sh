#!/bin/bash

# Setup Ollama for the vulnerable chatbot demo

echo "================================"
echo "  Ollama Setup for Demo"
echo "================================"

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Ollama is not installed."
    echo ""
    echo "Please install Ollama first:"
    echo "  macOS: brew install ollama"
    echo "  Linux: curl -fsSL https://ollama.ai/install.sh | sh"
    echo ""
    exit 1
fi

echo "✓ Ollama is installed"

# Check if Ollama is running
if ! ollama list &> /dev/null; then
    echo "Starting Ollama service..."
    ollama serve &
    sleep 3
fi

echo "✓ Ollama service is running"

# Function to pull a model
pull_model() {
    local model=$1
    echo ""
    echo "Checking for model: $model"
    
    if ollama list | grep -q "$model"; then
        echo "✓ Model $model is already available"
    else
        echo "Pulling model $model..."
        ollama pull $model
        if [ $? -eq 0 ]; then
            echo "✓ Successfully pulled $model"
        else
            echo "✗ Failed to pull $model"
            return 1
        fi
    fi
}

# Pull required models
echo ""
echo "Setting up models..."
pull_model "Model is available"

# Optional: Pull alternative models
echo ""
echo "Would you like to install alternative models? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "Installing alternative models..."
    pull_model "mistral"
    pull_model "llama3"
fi

# Test the model
echo ""
echo "Testing model..."
echo "Running test prompt..."

test_response=$(ollama run llama2 "Say 'Hello, SuperCarz!' and nothing else" --verbose=false 2>/dev/null)

if [[ $test_response == *"SuperCarz"* ]]; then
    echo "✓ Model test successful"
else
    echo "⚠ Model test returned unexpected response"
fi

echo ""
echo "================================"
echo "  Setup Complete!"
echo "================================"
echo ""
echo "Models ready for use:"
ollama list

echo ""
echo "You can now run the FastAPI server:"
echo "  cd .. && python backend/main.py"
echo ""
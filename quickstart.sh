#!/bin/bash

# Quick setup and activation helper for macOS
# Usage: source quickstart.sh

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Function to setup and activate
setup_and_activate() {
    local VENV_DIR="venv"
    
    # Check if we're already in a virtual environment
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        echo -e "${YELLOW}Already in a virtual environment: $VIRTUAL_ENV${NC}"
        echo -e "${YELLOW}Deactivating current environment...${NC}"
        deactivate
    fi
    
    # Create venv if it doesn't exist
    if [ ! -d "$VENV_DIR" ]; then
        echo -e "${YELLOW}Creating virtual environment...${NC}"
        python3 -m venv $VENV_DIR
        
        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to create virtual environment${NC}"
            return 1
        fi
        echo -e "${GREEN}✓ Virtual environment created${NC}"
    fi
    
    # Activate the virtual environment
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source $VENV_DIR/bin/activate
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Virtual environment activated${NC}"
        echo -e "${GREEN}Python: $(which python)${NC}"
        echo -e "${GREEN}Pip: $(which pip)${NC}"
        
        # Check if requirements.txt exists and offer to install
        if [ -f "requirements.txt" ]; then
            echo -e "\n${YELLOW}requirements.txt found${NC}"
            read -p "Install dependencies now? (y/n): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                echo -e "${YELLOW}Installing dependencies...${NC}"
                pip install --upgrade pip
                pip install -r requirements.txt
                echo -e "${GREEN}✓ Dependencies installed${NC}"
            fi
        fi
        
        echo -e "\n${GREEN}========================================${NC}"
        echo -e "${GREEN}  Environment Ready!${NC}"
        echo -e "${GREEN}========================================${NC}"
        echo -e "${YELLOW}You are now in the virtual environment${NC}"
        echo -e "${YELLOW}Run 'deactivate' to exit${NC}"
    else
        echo -e "${RED}Failed to activate virtual environment${NC}"
        return 1
    fi
}

# Execute the function
setup_and_activate
#!/bin/bash

# Setup script for PE Editor 7.3

# ANSI color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting setup for PE Editor 7.3...${NC}"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 could not be found.${NC}"
    echo "Please install Python 3 to run this application."
    exit 1
fi

echo -e "${GREEN}Python 3 found.${NC}"

# Define virtual environment directory
VENV_DIR="venv"

# Tell Dropbox not to sync a folder (it stays on this computer only)
mark_dropbox_ignored() {
    if command -v setfattr &> /dev/null; then
        setfattr -n user.com.dropbox.ignored -v 1 "$1" 2>/dev/null
    elif command -v xattr &> /dev/null; then
        xattr -w com.dropbox.ignored 1 "$1" 2>/dev/null
    fi
}

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating one...${NC}"
    # Create the folder and mark it ignored first, so Dropbox never uploads it
    mkdir -p "$VENV_DIR"
    mark_dropbox_ignored "$VENV_DIR"
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to create virtual environment.${NC}"
        exit 1
    fi
    echo -e "${GREEN}Virtual environment created.${NC}"
else
    echo -e "${GREEN}Virtual environment already exists.${NC}"
fi

# Make sure an existing venv is also excluded from Dropbox
mark_dropbox_ignored "$VENV_DIR"

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo -e "${YELLOW}Installing dependencies from requirements.txt...${NC}"
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to install dependencies.${NC}"
        deactivate
        exit 1
    fi
    echo -e "${GREEN}Dependencies installed successfully.${NC}"
else
    echo -e "${RED}requirements.txt not found. Cannot install dependencies.${NC}"
    deactivate
    exit 1
fi

echo -e "${GREEN}Setup complete! You can now run the application.${NC}"
deactivate
exit 0

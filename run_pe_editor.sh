#!/bin/bash

# Run script for PE Editor RF 7.3

# ANSI color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR" || exit 1
VENV_DIR="$SCRIPT_DIR/venv"
MAIN_SCRIPT="$SCRIPT_DIR/pe_editor.py"

run_app() {
    echo -e "${GREEN}Launching PE Editor...${NC}"
    "$VENV_DIR/bin/python" "$MAIN_SCRIPT" "$@"
    return $?
}

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Virtual environment not found. Running setup...${NC}"
    ./setup_env.sh
    if [ $? -ne 0 ]; then
        echo -e "${RED}Setup failed. Aborting.${NC}"
        exit 1
    fi
fi

# Try to run the application
run_app "$@"
EXIT_CODE=$?

# If application failed, try to repair environment and run again
if [ $EXIT_CODE -ne 0 ]; then
    echo -e "${RED}Application crashed or failed to start (Exit code: $EXIT_CODE).${NC}"
    echo -e "${YELLOW}Attempting to repair environment...${NC}"
    
    # Run setup script to ensure environment is correct
    ./setup_env.sh
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Environment repair complete. Retrying application launch...${NC}"
        run_app "$@"
        EXIT_CODE=$?
    else
        echo -e "${RED}Environment repair failed.${NC}"
        exit 1
    fi
fi

exit $EXIT_CODE

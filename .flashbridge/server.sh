#!/bin/bash

# Get the directory path of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
VENV_NAME="svenv"
REQUIREMENTS_NAME="srequirements.txt"

# Function to delete the virtual environment
delete_venv() {
    echo "Cleaning up virtual environment..."
    rm -rf "$SCRIPT_DIR/$VENV_NAME"
    echo "Virtual environment deleted."
    exit 1
}

# Check if the virtual environment is configured
if [ ! -d "$SCRIPT_DIR/$VENV_NAME" ]; then
    echo "Setting up virtual environment..."
    python3 -m venv "$SCRIPT_DIR/$VENV_NAME"
    source "$SCRIPT_DIR/$VENV_NAME/bin/activate" || delete_venv
    pip install -r "$SCRIPT_DIR/$REQUIREMENTS_NAME" || delete_venv
    echo "Virtual environment setup complete."
else
    source "$SCRIPT_DIR/$VENV_NAME/bin/activate"
fi

# Run the server script
python "$SCRIPT_DIR/server.py"


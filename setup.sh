#!/usr/bin/env bash

# colors
RESET_COLOR="\033[0m"
GREEN="\033[0;32m"
RED="\033[0;31m"

# Create and activate python's virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Setup intial .env file
cp .env.example .env

# Install python dependencies
pip3 install -r requirements.txt

echo "\n${GREEN}[Setup completed successfully! Your environment is ready.]${RESET_COLOR}"
echo "\n${GREEN}Remember to change .env variables to customize your settings.]${RESET_COLOR}"
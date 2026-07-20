#!/usr/bin/env bash

# colors
RESET_COLOR="\033[0m"
GREEN="\033[0;32m"
RED="\033[0;31m"

echo "${GREEN}INFO: ${RESET_COLOR}Creating python virtual environment..."
python3 -m venv .venv
echo "${GREEN}INFO: ${RESET_COLOR}Python virtual environment created successfully!"


echo "${GREEN}INFO: ${RESET_COLOR}Activating python virtual environment..."
source .venv/bin/activate
echo "${GREEN}INFO: ${RESET_COLOR}Python virtual environment activated successfully!"

echo "${GREEN}INFO: ${RESET_COLOR}Setting up intial .env file..."
cp .env.example .env

echo "${GREEN}INFO: ${RESET_COLOR}Installing python dependencies..."
pip3 install -r requirements.txt
echo "${GREEN}INFO: ${RESET_COLOR}Python dependencies installed successfully!"


echo "${GREEN}INFO: ${RESET_COLOR}Setup completed successfully! Your environment is ready."
echo "\n${GREEN}INFO: ${RESET_COLOR}Remember to change .env variables to customize your settings."
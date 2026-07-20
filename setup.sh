#!/usr/bin/env bash

# colors
RESET_COLOR="\033[0m"
GREEN="\033[0;32m"
RED="\033[0;31m"

echo "${GREEN}Create and activate python virtual environment${RESET_COLOR}"
python3 -m venv .venv
source .venv/bin/activate

echo "${GREEN}Setup intial .env file${RESET_COLOR}"
cp .env.example .env

echo "${GREEN}Install python dependencies${RESET_COLOR}"
pip3 install -r requirements.txt

echo "${GREEN}Setup completed successfully! Your environment is ready.${RESET_COLOR}"
echo "\n${GREEN}Remember to change .env variables to customize your settings.${RESET_COLOR}"
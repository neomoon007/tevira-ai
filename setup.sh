#!/usr/bin/env bash

# Create and activate python's virtual environment
python3 -m venv venv
source venv/bin/activate

# Setup intial .env file
echo "Remember to change .env variables to customize your settings"
cp .env.example .env

# Install python dependencies
pip3 install -r requirements.txt
#!/usr/bin/env bash

# Colors
RESET_COLOR="\033[0m"
# RED="\033[0;31m"
GREEN="\033[0;32m"
# YELLOW="\033[0;33m"

# Log functions
log_info() { echo -e "${GREEN}INFO:${RESET_COLOR} $*"; }
# log_warn() { echo -e "${YELLOW}WARN:${RESET_COLOR}  $*"; }
# log_error() { echo -e "${RED}ERROR:${RESET_COLOR} $*"; }

log_info "Creating python virtual environment..."
python3 -m venv .venv
log_info "Python virtual environment created successfully!"


log_info "Activating python virtual environment..."
source .venv/bin/activate
log_info "Python virtual environment activated successfully!"

log_info "Setting up intial .env file..."
cp .env.example .env

log_info "Installing python dependencies..."
pip3 install -r requirements.txt
log_info "Python dependencies installed successfully!"


log_info "Setup completed successfully! Your environment is ready."
log_info "Remember to change .env variables to customize your settings."
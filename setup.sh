#!/usr/bin/env bash

# Colors
RESET_COLOR="\033[0m"
# RED="\033[0;31m"
GREEN="\033[0;32m"
# YELLOW="\033[0;33m"

# Log functions
log_info() { echo -e "${GREEN}INFO${RESET_COLOR}:     $*"; }
# log_warn() { echo -e "${YELLOW}WARN${RESET_COLOR}:     $*"; }
# log_error() { echo -e "${RED}ERROR${RESET_COLOR}:     $*"; }

log_info "Setting up intial .env files..."
cp .env.example .env
cp .envrc.example .envrc

log_info "Installing dependencies..."
poetry install
direnv allow

log_info "Setup completed successfully! Your environment is ready."
log_info "Remember to change .env variables to customize your settings."
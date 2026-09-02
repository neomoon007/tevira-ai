#!/usr/bin/env bash

# Stop script if error
set -e

# Colors
RESET_COLOR="\033[0m"
# RED="\033[0;31m"
GREEN="\033[0;32m"
# YELLOW="\033[0;33m"


# Log functions
log_info() { echo -e "${GREEN}INFO${RESET_COLOR}:     $*"; }
# log_warn() { echo -e "${YELLOW}WARN${RESET_COLOR}:     $*"; }
# log_error() { echo -e "${RED}ERROR${RESET_COLOR}:     $*"; }


log_info "Running alembic migrations..."
alembic upgrade head
log_info "Database is up to date."

log_info "Running test suite..."
pytest

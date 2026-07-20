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

log_info "Loading .env variables..."
set -a
source .env
set +a

log_info "Initializing docker containers..."
docker compose up -d

log_info "Waiting for PostgreSQL..."

# until docker exec tevira-postgres

log_info "Running alembic migrations..."
alembic upgrade head

log_info "Initializing uvicorn server..."
uvicorn src.app.main:app --reload


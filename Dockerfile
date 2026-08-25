# ---------------------------------------
# STAGE 1: The Builder
# ---------------------------------------
FROM python:3.14.7-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install poetry via pip (cleaner and smaller than apt-get curl)
RUN pip install --no-cache-dir poetry==2.4.1

COPY pyproject.toml poetry.lock ./

# Create a virtual environment and install strictly production dependencies
RUN python -m venv /opt/venv \
    && . /opt/venv/bin/activate \
    && poetry install --only main --no-interaction --no-ansi --no-root

# ---------------------------------------
# STAGE 2: The Production Runtime
# ---------------------------------------
FROM python:3.14.7-slim

# Force the OS to prioritize the virtual environment's binaries
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Copy ONLY the isolated virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the application source code
COPY . .

CMD ["uvicorn", "src.tevira_ai.main:app", "--host", "0.0.0.0", "--port", "8000"]
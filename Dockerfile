# ---------------------------------------
# STAGE 1: The Builder
# ---------------------------------------
FROM python:3.14.7-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Install poetry via pip (cleaner and smaller than apt-get curl)
RUN pip install --no-cache-dir poetry==2.4.1

COPY pyproject.toml poetry.lock ./

# Create a virtual environment and install strictly production dependencies
RUN python -m venv /opt/venv \
    && . /opt/venv/bin/activate \
    && poetry install --only main --no-interaction --no-ansi --no-root

# ---------------------------------------
# STAGE 2.1: The Test Builder
# ---------------------------------------
FROM builder AS test-builder

RUN poetry install --only test --no-interaction --no-ansi --no-root

# ---------------------------------------
# STAGE 2.2: The Test Target
# ---------------------------------------
FROM python:3.14.7-slim AS test

# Force the OS to prioritize the virtual environment's binaries
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Copy ONLY the isolated virtual environment from the builder stage
COPY --from=test-builder /opt/venv /opt/venv

# Copy the application source code
COPY /tests /app/tests/
COPY /src /app/src/
COPY /alembic /app/alembic/
COPY alembic.ini pytest.ini /scripts/run.test.sh /app/

CMD ["./run.test.sh"]


# ---------------------------------------
# STAGE 3: The Production Runtime
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
COPY /src /app/src/
COPY /alembic /app/alembic/
COPY alembic.ini /scripts/run.sh /app/

CMD ["./run.sh"]
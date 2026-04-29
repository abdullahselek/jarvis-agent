FROM python:3.11-slim

# Install curl, git, xz-utils, jq (for hermes hooks), and ca-certificates, then clean up
RUN apt-get update && apt-get install -y --no-install-recommends curl git ca-certificates xz-utils jq && \
    rm -rf /var/lib/apt/lists/*

# Install hermes-agent
RUN curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copy deps first for layer caching
COPY pyproject.toml .python-version README.md ./
RUN uv sync

# Copy app source
COPY main.py ./
COPY tests/ ./
COPY src/ /app/src/
ENV PYTHONPATH=/app/src

# Configure hermes-agent hooks for file_guard
COPY src/safety/hooks/ /usr/local/bin/hermes-hooks/
RUN chmod +x /usr/local/bin/hermes-hooks/*

COPY src/safety/setup_hooks.py /usr/local/bin/setup_hooks.py
RUN python3 /usr/local/bin/setup_hooks.py

COPY config/ /app/config/

CMD ["/app/.venv/bin/python", "/app/main.py"]

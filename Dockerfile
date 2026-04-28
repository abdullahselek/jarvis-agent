FROM python:3.11-slim

# Ollama runs on the host; containers can reach it via host.docker.internal
ENV OLLAMA_HOST=host.docker.internal

# Install curl, git, xz-utils (for tar compression), and ca-certificates, then clean up
RUN apt-get update && apt-get install -y --no-install-recommends curl git ca-certificates xz-utils && \
    rm -rf /var/lib/apt/lists/*

# Install hermes-agent
RUN curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

WORKDIR /app

COPY main.py pyproject.toml ./
COPY .python-version .python-version

CMD ["hermes"]

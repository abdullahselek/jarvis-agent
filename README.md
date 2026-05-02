# jarvis-agent

A local-first, multi-agent AI system that uses [hermes-agent](https://github.com/NousResearch/hermes-agent) as its foundation and [Ollama](https://ollama.com/) for LLM hosting.

## Architecture

```
User
  └─► Supervisor Agent (gemma4:31b)
       ├─► /coder       (qwen3.6)      — engineering tasks
       ├─► /analyst     (gemma4:e4b)    — data analysis & summarization
       └─► /general     (gemma4:31b)    — default chat & coordination
```

All agents connect to a single Ollama instance at `http://localhost:11434/v1`.

## Safety

Two layers protect every action:

- **Action Consent** — hermes-agent Command Approval: every tool call prompts for explicit user confirmation.
- **File Access Guard** — a whitelist-based path validator (`src/safety/file_guard.py`) blocks filesystem tools from accessing directories outside the permitted list.

Permitted paths (default): `~/Repositories`

## Quick Start

1. Start Ollama on the host with external access enabled:
   ```bash
   sudo systemctl edit ollama
   ```
   Add:
   ```ini
   [Service]
   ExecStart=
   Environment="OLLAMA_HOST=0.0.0.0"
   ```
   Then:
   ```bash
   sudo systemctl daemon-reload && sudo systemctl restart ollama
   ```

2. Pull required models:
   ```bash
   ollama pull gemma4:31b
   ollama pull qwen3.6
   ollama pull gemma4:e4b
   ```

3. Run the agent:
   ```bash
   docker compose up jarvis-agent
   ```

4. Run tests:
   ```bash
   docker compose --profile test up test
   docker exec jarvis-agent python3 /app/test_file_guard.py   # file guard
   ```

## Project Structure

```
.
├── config/
│   └── profiles.yaml            # Agent profile definitions (model, persona)
├── src/
│   ├── safety/
│   │   ├── file_guard.py        # Whitelist-based path validator
│   │   ├── hooks/
│   │   │   └── block_file_access.sh  # hermes-agent pre_tool_call hook
│   │   ├── setup_hooks.py       # Configures the hermes hook
│   │   └── __init__.py
│   └── orchestrator/
│       └── router.py            # Intent-to-profile routing (Phase 3)
├── tests/
│   ├── test_connectivity.py     # Ollama API + model verification
│   ├── test_file_guard.py       # Path validator unit tests
│   ├── test_routing.py          # Intent classifier unit tests
│   └── test_integration.py      # Consent, security, routing
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── main.py
```

## Router Keywords

| Profile | Keywords |
|---------|----------|
| **coder** | `code`, `coding`, `develop`, `implement`, `fix`, `debug`, `refactor`, `api`, `bug`, `test`, `deploy` |
| **analyst** | `analyze`, `summarize`, `compare`, `report`, `research`, `data`, `statistics`, `extract`, `find` |
| **general** | Default — all other inputs |

## Run the Agent

```bash
docker compose up jarvis-agent
docker compose run -it jarvis-agent
```

## Run All Tests

```bash
docker compose --profile test up test                           # Integration tests
docker exec jarvis-agent /app/.venv/bin/python /app/test_file_guard.py    # File guard
docker exec jarvis-agent /app/.venv/bin/python /app/test_routing.py        # Router
docker exec jarvis-agent /app/.venv/bin/python /app/test_integration.py    # Consent, security, routing
```

"""Verify hermes-agent can reach the Ollama API."""

import os
import urllib.request
import json

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")

# Required models from the plan
REQUIRED_MODELS = {"gemma4", "qwen3.6"}


def test_api_reachable():
    req = urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=5)
    assert req.status == 200, f"Ollama API unreachable at {OLLAMA_URL}"


def test_required_models():
    req = urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=5)
    data = json.loads(req.read())
    pulled = {m["name"].split(":")[0] for m in data.get("models", [])}
    missing = REQUIRED_MODELS - pulled
    assert not missing, f"Missing models: {missing}"


if __name__ == "__main__":
    test_api_reachable()
    test_required_models()
    print("All connectivity checks passed")

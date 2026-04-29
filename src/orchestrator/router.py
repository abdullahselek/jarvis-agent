"""Intent-based router that maps user messages to agent profiles."""

import yaml
from pathlib import Path


_CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config" / "profiles.yaml"


def _load_profiles() -> dict:
    with open(_CONFIG_PATH) as f:
        data = yaml.safe_load(f)
    return data.get("profiles", {})


# Routing rules: (keywords_or_pattern, profile_name)
_ROUTE_RULES = [
    (
        {"code", "coding", "develop", "implement", "write a function",
         "fix", "debug", "refactor", "edit", "build", "create a class",
         "api", "endpoint", "feature", "bug", "test", "unit test",
         "class", "method", "implement", "architecture", "database",
         "deploy", "run the application", "the application",
         "source code", "src"},
        "coder",
    ),
    (
        {"analyze", "extract", "summarize", "compare", "report",
         "research", "data", "statistics", "metric", "trend",
         "information", "summary", "list", "overview", "review",
         "find", "look up", "search", "information about",
         "what is", "who is", "tell me about"},
        "analyst",
    ),
]


_DEFAULT_PROFILE = "general"


def _classify(message: str) -> str:
    """Classify user intent and return the target profile name."""
    lower = message.lower()
    for keywords, profile in _ROUTE_RULES:
        if any(kw in lower for kw in keywords):
            return profile
    return _DEFAULT_PROFILE


def get_profile(message: str) -> dict:
    """Return the profile dict for the given user message."""
    profile_name = _classify(message)
    profiles = _load_profiles()
    return profiles[profile_name]


def route(message: str) -> str:
    """Return the profile name for the given user message."""
    return _classify(message)

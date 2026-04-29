"""Unit tests for intent-based router."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from orchestrator import route, get_profile


def test_rout_to_coder():
    assert route("fix the bug in main.py") == "coder"
    assert route("write a function to calculate fibonacci") == "coder"
    assert route("implement a new API endpoint") == "coder"
    assert route("refactor the codebase") == "coder"
    assert route("debug this error") == "coder"


def test_rout_to_analyst():
    assert route("analyze this data") == "analyst"
    assert route("summarize the report") == "analyst"
    assert route("research the trends") == "analyst"
    assert route("compare these options") == "analyst"
    assert route("extract information about the project") == "analyst"


def test_default_general():
    assert route("hello") == "general"
    assert route("what can you do") == "general"
    assert route("help me with something") == "general"


def test_get_profile_returns_dict():
    profile = get_profile("fix the bug")
    assert isinstance(profile, dict)
    assert "model" in profile
    assert "persona" in profile
    assert profile["model"] == "qwen3.6"


def test_get_profile_analyst():
    profile = get_profile("analyze this")
    assert profile["model"] == "gemma4:e4b"


def test_get_profile_general():
    profile = get_profile("hello world")
    assert profile["model"] == "gemma4:31b"


if __name__ == "__main__":
    test_rout_to_coder()
    test_rout_to_analyst()
    test_default_general()
    test_get_profile_returns_dict()
    test_get_profile_analyst()
    test_get_profile_general()
    print("All routing tests passed")

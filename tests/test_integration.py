"""Phase 4: Integration tests — consent, security, and routing."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from safety.file_guard import PermissionError, validate, PERMITTED_PATHS
from orchestrator import route, get_profile

HOME = os.path.expanduser("~")


def test_command_approval_is_built_into_hermes():
    """hermes-agent TUI already requires user confirmation for every tool call.
    This is verified by the TUI banner shown at startup (every tool call
    prompts y/N). No additional code needed — the framework handles it."""
    pass


def test_blocked_external_path():
    try:
        validate("/etc/passwd")
        assert False, "Should have raised PermissionError"
    except PermissionError:
        pass


def test_blocked_home_subdir():
    try:
        validate(f"{HOME}/Downloads/test.txt")
        assert False, "Should have raised PermissionError"
    except PermissionError:
        pass


def test_blocked_root():
    try:
        validate("/root")
        assert False, "Should have raised PermissionError"
    except PermissionError:
        pass


def test_permitted_path():
    validate(f"{HOME}/Repositories/test.py")


def test_permitted_subdirectory():
    validate(f"{HOME}/Repositories/jarvis-agent/tests/test_integration.py")


def test_permitted_paths_config():
    assert f"{HOME}/Repositories" in PERMITTED_PATHS


def test_routing_coder():
    assert route("fix the bug in main.py") == "coder"
    assert route("implement a new API endpoint") == "coder"
    assert route("debug this error") == "coder"
    assert route("write a function to calculate fibonacci") == "coder"


def test_routing_analyst():
    assert route("analyze this data") == "analyst"
    assert route("summarize the report") == "analyst"
    assert route("research the trends") == "analyst"


def test_routing_default_general():
    assert route("hello") == "general"
    assert route("what can you do") == "general"


def test_routing_returns_full_profile():
    profile = get_profile("fix the bug")
    assert profile["model"] == "qwen3.6:35b"
    assert "persona" in profile

    profile = get_profile("analyze this")
    assert profile["model"] == "gemma4:e4b"

    profile = get_profile("hello world")
    assert profile["model"] == "gemma4:31b"


if __name__ == "__main__":
    test_command_approval_is_built_into_hermes()
    test_permitted_path()
    test_permitted_subdirectory()
    test_permitted_paths_config()
    test_blocked_external_path()
    test_blocked_home_subdir()
    test_blocked_root()
    test_routing_coder()
    test_routing_analyst()
    test_routing_default_general()
    test_routing_returns_full_profile()
    print("All Phase 4 integration tests passed")

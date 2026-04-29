"""Unit tests for file_guard path validation."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from safety.file_guard import PermissionError, validate

HOME = os.path.expanduser("~")


def test_permitted_path():
    validate(f"{HOME}/Repositories/test.py")


def test_permitted_subdirectory():
    validate(f"{HOME}/Repositories/jarvis-agent/src/safety/file_guard.py")


def test_blocked_path():
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


if __name__ == "__main__":
    test_permitted_path()
    test_permitted_subdirectory()
    test_blocked_path()
    test_blocked_home_subdir()
    print("All file_guard tests passed")

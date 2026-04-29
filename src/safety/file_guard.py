"""Whitelist-based file system path validator for jarvis-agent."""

import os
from pathlib import Path


# Paths the agent is allowed to read/write/list
PERMITTED_PATHS: list[str] = [
    os.path.expanduser("~/Repositories"),
]


class PermissionError(Exception):
    """Access denied to the requested path."""


def _normalize(path: Path) -> str:
    """Return the resolved absolute string path."""
    return os.path.normpath(path.resolve().as_posix())


def _is_permitted(path_str: str) -> bool:
    """Check if *path_str* starts with any permitted directory."""
    normed = _normalize(Path(path_str))
    for permitted in (_normalize(Path(p)) for p in PERMITTED_PATHS):
        if normed == permitted or normed.startswith(permitted + "/"):
            return True
    return False


def validate(path_str: str) -> Path:
    """Validate that *path_str* is in the whitelist.

    Returns the resolved Path on success, raises PermissionError otherwise.
    """
    if not _is_permitted(path_str):
        raise PermissionError(
            f"Access denied: {path_str} is outside permitted paths {PERMITTED_PATHS}"
        )
    return Path(path_str)


def wrap_tool(func, tool_name: str, *args, **kwargs):
    """Wrap a filesystem tool (read/write/list) to run *validate* before execution.

    Raises PermissionError if the path is not whitelisted.
    """
    permitted_arg_indices = {
        1,
        2,
    }  # most tools take the path as the second positional arg
    for idx in permitted_arg_indices:
        if len(args) > idx and isinstance(args[idx], (str, Path)):
            validate(args[idx])
            return func(*args, **kwargs)

    for key in ("path", "filepath", "filename", "directory"):
        if key in kwargs and isinstance(kwargs[key], (str, Path)):
            validate(kwargs[key])
            return func(*args, **kwargs)

    return func(*args, **kwargs)

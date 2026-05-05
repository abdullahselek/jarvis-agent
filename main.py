"""jarvis-agent: Supervisor that routes user input to the correct agent profile, then delegates to hermes-agent."""

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from orchestrator import get_profile


_SKIPPED = frozenset((
    "__pycache__", "node_modules", ".git", ".cache", ".npm", ".cargo",
    "virtualenv", ".venv", ".conda", ".local", "snap", ".config",
))


_ROOT = os.environ.get("GITHUB_ROOT", "/repos/github")


def _search_local_paths(message: str, max_results: int = 100, max_depth: int = 5) -> str:
    root = Path(_ROOT)
    if not root.exists():
        return ""
    found: set[str] = set()
    for kw in _extract_keywords(message):
        for dirpath, dirnames, filenames in os.walk(root, topdown=True):
            dirnames[:] = [
                d for d in dirnames
                if d not in _SKIPPED
                and len(Path(dirpath).relative_to(root).parts) < max_depth
            ]
            for name in [*dirnames, *filenames]:
                if kw in name.lower():
                    rel = Path(dirpath, name).relative_to(root)
                    if len(rel.parts) <= max_depth:
                        found.add(str(rel))
                    if len(found) >= max_results:
                        break
            if len(found) >= max_results:
                break
        if len(found) >= max_results:
            break
    return "\n".join(sorted(found)) if found else ""


_KEYWORD_FILTER = frozenset((
    "a", "the", "is", "to", "of", "in", "on", "at", "for",
    "and", "or", "it", "me", "my", "this", "that", "can",
    "do", "i",
))


def _extract_keywords(message: str) -> list[str]:
    words = message.lower().split()
    return [w.rstrip(".,!?;:") for w in words if len(w) >= 3 and w.lower().rstrip(".,!?;:") not in _KEYWORD_FILTER]


def main():
    """Detect intent, then invoke hermes-agent with the target profile's model."""
    print("jarvis-agent v0.1.0 — Enter your request:\n")
    message = input("[You]: ").strip()
    if not message:
        print("Nothing entered.")
        sys.exit(0)

    # Inject local file system paths so all profiles can reference them.
    paths = _search_local_paths(message)
    if paths:
        message += f"\n\nAvailable paths on this system:\n{paths}"

    profile = get_profile(message)
    profile_name = profile["model"].split(":")[0]
    print(f"\n[Jarvis]: Routing to profile: {profile_name} "
          f"(model: {profile['model']})\n")

    # Run hermes-agent with the target model.
    # Pipe the user's message to hermes' stdin so it doesn't hang waiting for input.
    env = os.environ.copy()
    env["HERMES_ACCEPT_HOOKS"] = "1"
    result = subprocess.run(
        ["hermes", "chat", "-m", f"ollama/{profile['model']}", "--yolo"],
        input=message,
        text=True,
        env=env,
        cwd=os.getcwd(),
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()

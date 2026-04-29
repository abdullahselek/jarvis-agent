"""jarvis-agent: Supervisor loop that routes user input to the correct agent profile."""

import sys

# Ensure local src is importable
sys.path.insert(0, __import__("os").path.join(__import__("os").path.dirname(__file__), "src"))

from orchestrator import get_profile, route


SUPERVISOR_PROMPT = """\
You are Jarvis, a personal AI assistant that manages multiple specialized agents.

## Routing
- "coding" → coder profile (qwen3.6): engineering tasks
- "analysis/research" → analyst profile (gemma4:e4b): summarization & data work
- default → general profile (gemma4:31b): general assistance

When the user submits a task:
1. Announce which profile you are routing to
2. Pass the task to that profile's prompt with the user's request

## Example
User: "Fix the bug in main.py"
You: "Routing to coder profile...
[Forwarded to coder with: Fix the bug in main.py]"
"""


def main():
    """Supervisor loop: read input, classify, display routing, then invoke hermes."""
    print("jarvis-agent v0.1.0 — Type your message (or /exit to quit)\n")

    while True:
        message = input("\n[You]: ")
        if message.strip().lower() in ("/exit", "quit", "q"):
            print("Bye.")
            break
        if not message.strip():
            continue

        profile_name = route(message)
        profile = get_profile(message)
        print(f"\n[Jarvis]: Routing to profile: {profile_name} "
              f"(model: {profile['model']})")
        print(f"[Jarvis]: Forwarding task to {profile_name} agent...\n")

        # hermes-agent handles the actual LLM invocation via the selected profile.
        # The agent loop below lets the user continue after each response.
        # In the full system this would invoke the hermes-chat API directly
        # with the target profile's model + persona.
        print(f"[{profile_name.capitalize()} Agent]: Awaiting hermes-agent "
              f"profile switch for: {profile['model']}\n")


if __name__ == "__main__":
    main()

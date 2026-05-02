"""jarvis-agent: Supervisor that routes user input to the correct agent profile, then delegates to hermes-agent."""

import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from orchestrator import get_profile


def main():
    """Detect intent, then invoke hermes-agent with the target profile's model."""
    print("jarvis-agent v0.1.0 — Enter your request:\n")
    message = input("[You]: ").strip()
    if not message:
        print("Nothing entered.")
        sys.exit(0)

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
        env=env,
        cwd=os.getcwd(),
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()

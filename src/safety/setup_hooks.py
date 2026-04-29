"""Configure hermes-agent hooks for file_guard integration."""

import os
import re


CONFIG_PATH = os.path.expanduser("~/.hermes/config.yaml")


def configure_hooks():
    """Uncomment and update the hooks section in hermes config."""
    with open(CONFIG_PATH, "r") as f:
        content = f.read()

    # Uncomment the hooks section (lines starting with "# hooks:", "#   pre_tool_call:", etc.)
    content = re.sub(
        r"^(# )hooks:", r"hooks:", content, flags=re.MULTILINE
    )
    content = re.sub(
        r"^(# )  pre_tool_call:", r"  pre_tool_call:", content, flags=re.MULTILINE
    )
    content = re.sub(
        r"^(# )    - matcher:", r"    - matcher:", content, flags=re.MULTILINE
    )
    content = re.sub(
        r"^(# )      command:", r"      command:", content, flags=re.MULTILINE
    )
    content = re.sub(
        r"^(# )      timeout:", r"      timeout:", content, flags=re.MULTILINE
    )
    content = re.sub(
        r"^(# )  post_tool_call:", r"  post_tool_call:", content, flags=re.MULTILINE
    )
    content = re.sub(
        r"^(# )  pre_llm_call:", r"  pre_llm_call:", content, flags=re.MULTILINE
    )
    content = re.sub(
        r"^(# )  subagent_stop:", r"  subagent_stop:", content, flags=re.MULTILINE
    )
    content = re.sub(
        r"^(# )hooks_auto_accept", r"hooks_auto_accept", content, flags=re.MULTILINE
    )

    # Update the pre_tool_call matcher to cover all filesystem tools
    content = content.replace(
        '    - matcher: "terminal"',
        '    - matcher: "write_file|read_file|patch|search|list_directory|move_file|copy_file|delete_file|terminal"',
    )

    # Replace the hook command path
    content = content.replace(
        "~/.hermes/agent-hooks/block-rm-rf.sh",
        "/usr/local/bin/hermes-hooks/block_file_access.sh",
    )

    with open(CONFIG_PATH, "w") as f:
        f.write(content)

    print("Hermes hooks configured successfully")


if __name__ == "__main__":
    configure_hooks()

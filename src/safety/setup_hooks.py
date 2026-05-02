"""Configure hermes-agent hooks for file_guard integration."""

import os
import re


CONFIG_PATH = os.path.expanduser("~/.hermes/config.yaml")


def configure_hooks():
    """Uncomment hooks and configure ollama as the inference backend."""
    with open(CONFIG_PATH, "r") as f:
        content = f.read()

    # ── Hooks section ──────────────────────────────────────────────────

    # Uncomment the hooks section keys (only uncomment actual YAML keys)
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
        r"^(# )hooks_auto_accept:", r"hooks_auto_accept:", content, flags=re.MULTILINE
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

    # Fix a broken comment line in the sampling section
    content = content.replace(
        "      timeout: 30             # LLM call timeout (seconds)",
        "# timeout: 30             # LLM call timeout (seconds)",
    )

    # ── Ollama backend ─────────────────────────────────────────────────
    # Change the default model and provider to use local Ollama
    content = content.replace(
        '  default: "anthropic/claude-opus-4.6"',
        '  default: "ollama/gemma4:31b"',
    )
    content = content.replace(
        '  provider: "auto"',
        '  provider: "custom"',
    )
    content = content.replace(
        '  base_url: "https://openrouter.ai/api/v1"',
        '  base_url: "http://localhost:11434/v1"',
    )

    with open(CONFIG_PATH, "w") as f:
        f.write(content)

    print("Hermes hooks and ollama configured successfully")


if __name__ == "__main__":
    configure_hooks()

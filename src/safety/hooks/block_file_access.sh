#!/usr/bin/env bash
# pre_tool_call hook: blocks filesystem tools that access non-whitelisted paths.
# Reads JSON payload on stdin, validates the path, writes JSON to stdout.
# If the path is outside the whitelist, blocks the tool call.

set -euo pipefail

# Read the hook payload (JSON on stdin)
PAYLOAD="$(cat)"

# Extract the tool name
TOOL_NAME=$(echo "$PAYLOAD" | jq -r '.tool_name')

# Only validate filesystem tools
if ! echo "$TOOL_NAME" | grep -qE '^(write_file|read_file|patch|search|list_directory|move_file|copy_file|delete_file)$'; then
  # Pass through for non-filesystem tools
  echo "$PAYLOAD"
  exit 0
fi

# Extract the path argument
PATH_ARG=$(echo "$PAYLOAD" | jq -r '.tool_input | to_entries[] | select(.key == "path" or .key == "filepath" or .key == "filename") | .value')

if [ -z "$PATH_ARG" ] || [ "$PATH_ARG" = "null" ]; then
  echo "$PAYLOAD"
  exit 0
fi

# Check against permitted paths
PERMITTED_PATHS=("${HOME}/Repositories")

# Check prefix match (no need for dir to exist)
for permitted in "${PERMITTED_PATHS[@]}"; do
  if [[ "$PATH_ARG" == "$permitted"* ]] || [[ "$PATH_ARG" == "$permitted" ]]; then
    echo "$PAYLOAD"
    exit 0
  fi
done

# Block the tool call
cat <<'HOOK_OUTPUT'
{"blocked": true, "reason": "File path is outside permitted directories. Use a path within ~/Repositories, ~/Documents, or ~/Downloads."}
HOOK_OUTPUT

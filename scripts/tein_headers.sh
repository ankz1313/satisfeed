#!/bin/sh
# Prints the Tein auth header for Claude Code's MCP connection (.mcp.json headersHelper).
# Mac apps opened from the Dock don't read ~/.zshrc, so if TEIN_API_KEY isn't already
# set, ask a login shell for it. The key is never written to any file.
key="$TEIN_API_KEY"
if [ -z "$key" ]; then
  key=$(zsh -ilc 'printf "\n%s" "$TEIN_API_KEY"' 2>/dev/null </dev/null | tail -n 1)
fi
if [ -z "$key" ]; then
  echo "TEIN_API_KEY is not set. Add: export TEIN_API_KEY=... to ~/.zshrc" >&2
  exit 1
fi
printf '{"Authorization": "Bearer %s"}\n' "$key"

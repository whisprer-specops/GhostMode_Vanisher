#!/bin/bash

SCRIPT_PATH="/usr/local/bin/ghost_fix_identities.py"

if ! command -v zenity >/dev/null; then
  echo "❌ zenity not installed. Install with: sudo apt install zenity"
  exit 1
fi

if [[ ! -f "$SCRIPT_PATH" ]]; then
  zenity --error --text="❌ Cannot find identity fixer script at $SCRIPT_PATH"
  exit 1
fi

(
  python3 "$SCRIPT_PATH"
) | zenity --progress \
  --title="Ghost Identity Fixer" \
  --text="Scanning & repairing identity folders..." \
  --pulsate --auto-close --no-cancel

zenity --info --title="Ghost Identity Fixer" --text="✅ All identity folders are now complete!"

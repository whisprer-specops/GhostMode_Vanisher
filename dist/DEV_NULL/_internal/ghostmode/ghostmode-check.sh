#!/bin/bash
set -e

echo "[🔍] Running GhostMode Preflight Check..."

MISSING=()

check_command() {
  if ! command -v "$1" &> /dev/null; then
    echo "❌ Missing: $1"
    MISSING+=("$1")
  else
    echo "✅ Found: $1"
  fi
}

# Required CLI tools
for cmd in zenity lsof lsblk gpg monero-wallet-cli python3; do
  check_command "$cmd"
done

# Check USB availability
USB=$(lsblk -o MOUNTPOINT -nr | grep -E '^/media|^/mnt' | head -n1)
if [[ -z "$USB" ]]; then
  echo "⚠️  No USB drive currently mounted."
else
  echo "✅ USB detected at $USB"
fi

# Final summary
if [[ ${#MISSING[@]} -gt 0 ]]; then
  echo -e "\n❌ Missing required tools: ${MISSING[*]}"
  echo "Run: sudo apt install ${MISSING[*]}"
  exit 1
else
  echo -e "\n✅ All checks passed. You're good to ghost 🫥"
  exit 0
fi

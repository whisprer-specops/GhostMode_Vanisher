#!/bin/bash
set -euo pipefail

CONFIG="$HOME/.config/ghostmode/ghostmode.conf"
UNINSTALL="/usr/local/bin/ghostmode-uninstall.sh"

# Read config
if [[ -f "$CONFIG" ]]; then
    ENABLE=$(grep -i '^enable_timeout' "$CONFIG" | cut -d'=' -f2 | tr -d '[:space:]')
    HOURS=$(grep -i '^timeout_hours' "$CONFIG" | cut -d'=' -f2 | tr -d '[:space:]')
else
    echo "No ghostmode.conf found. Exiting."
    exit 0
fi

if [[ "$ENABLE" != "true" ]]; then
    echo "Timeout-based wipe disabled. Exiting."
    exit 0
fi

THRESHOLD=$((HOURS * 3600))
echo "🕰️ Watching uptime... (Threshold: ${HOURS}h)"

while true; do
    UPTIME=$(cut -d. -f1 /proc/uptime)
    if (( UPTIME >= THRESHOLD )); then
        echo "💣 Uptime threshold reached. Executing uninstall!"
        bash "$UNINSTALL"
        break
    fi
    sleep 10
done

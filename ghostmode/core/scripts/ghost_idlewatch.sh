#!/bin/bash

# Duration before auto-wipe (minutes)
TIMEOUT_MINUTES=$1
TIMEOUT_MS=$(( TIMEOUT_MINUTES * 60 * 1000 ))

echo "⏳ GhostIdleWatch enabled – timeout after $TIMEOUT_MINUTES minutes"

while true; do
    IDLE_TIME=$(xprintidle)
    if [ "$IDLE_TIME" -gt "$TIMEOUT_MS" ]; then
        echo "💀 Inactivity threshold reached. Triggering GhostExit..."
        bash ~/GhostMode/ghost_exit.sh
        break
    fi
    sleep 30
done
#!/bin/bash

INTERVAL_MINUTES=15  # 💡 Change as needed
IDENTITY_DIR="$HOME/.ghost_identities"
CURRENT_ID=""

echo "⏱️ GHOSTMODE™ Identity Timer — rotating every $INTERVAL_MINUTES minutes."

while true; do
    # Pick random identity
    IDENTITY=$(ls "$IDENTITY_DIR" | shuf -n1)

    if [[ "$IDENTITY" == "$CURRENT_ID" ]]; then
        echo "🔁 Same identity, skipping..."
        continue
    fi

    CURRENT_ID="$IDENTITY"
    PROFILE_PATH="$IDENTITY_DIR/$IDENTITY"

    echo "🎭 Loading new identity: $CURRENT_ID"

    # Kill previous Firefox
    pkill firefox 2>/dev/null || true
    sleep 1

    # Launch browser with identity profile
    firefox --no-remote -profile "$PROFILE_PATH/firefox-profile" &

    # Import GPG key
    if [[ -f "$PROFILE_PATH/gpg-key.asc" ]]; then
        gpg --import "$PROFILE_PATH/gpg-key.asc"
    fi

    # Set Monero wallet context (shell-wide var)
    export MONERO_WALLET_DIR="$PROFILE_PATH/monero-wallet"

    # Show metadata
    echo "🔍 Identity Info:"
    jq . "$PROFILE_PATH/metadata.json"

    # Display avatar
    if command -v feh >/dev/null && [[ -f "$PROFILE_PATH/avatar.png" ]]; then
        feh --title "$CURRENT_ID" "$PROFILE_PATH/avatar.png" &
    fi

    echo "⏳ Sleeping for $INTERVAL_MINUTES minutes..."
    sleep $((INTERVAL_MINUTES * 60))
done

IFACE="wlan0"
sudo ifconfig $IFACE down
sudo macchanger -r $IFACE
sudo ifconfig $IFACE up
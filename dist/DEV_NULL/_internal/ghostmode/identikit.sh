#!/bin/bash

set -e

IDENTITY_DIR="$HOME/.ghost_identities"

echo "🎭 IDENTITY ROTATOR"

# Step 1: Select identity
IDENTITY=$(zenity --list --title="Choose an Identity" --column="Identities" $(ls "$IDENTITY_DIR"))

if [ -z "$IDENTITY" ]; then
    zenity --error --text="No identity selected!"
    exit 1
fi

PROFILE_PATH="$IDENTITY_DIR/$IDENTITY"

# Step 2: Load browser profile
echo "🧠 Loading browser profile for: $IDENTITY"
firefox --no-remote -profile "$PROFILE_PATH/firefox-profile" &

# Step 3: Import GPG key
if [[ -f "$PROFILE_PATH/gpg-key.asc" ]]; then
    echo "🔐 Importing GPG key..."
    gpg --import "$PROFILE_PATH/gpg-key.asc"
fi

# Step 4: Prepare Monero wallet path
if [[ -d "$PROFILE_PATH/monero-wallet" ]]; then
    echo "💰 Setting up Monero wallet path..."
    export MONERO_WALLET_DIR="$PROFILE_PATH/monero-wallet"
fi

# Step 5: Show metadata (alias, handle, burner email)
if [[ -f "$PROFILE_PATH/metadata.json" ]]; then
    zenity --text-info --title="Identity Metadata" --filename="$PROFILE_PATH/metadata.json"
else
    zenity --info --text="✅ $IDENTITY loaded. No metadata file found."
fi

# Step 6: Display avatar (if available)
if [[ -f "$PROFILE_PATH/avatar.png" ]]; then
    feh --title "👤 $IDENTITY" "$PROFILE_PATH/avatar.png" &
fi

echo "✅ Identity '$IDENTITY' fully loaded."
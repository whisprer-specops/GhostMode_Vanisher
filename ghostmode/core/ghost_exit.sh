#!/bin/bash

set -e
echo "💀 Initiating SmoothFade Exit Protocol..."

IDENTITY_DIR="$HOME/.ghost_identities"
CURRENT_ID=$(pgrep -a firefox | grep -oP '(?<=--profile )[^\s]+')

# Kill browser + GUI leaks
echo "🧯 Closing browsers..."
pkill firefox
pkill feh

# MAC reset
IFACE="wlan0"
sudo ifconfig $IFACE down
sudo macchanger -p $IFACE
sudo ifconfig $IFACE up
echo "🔁 MAC address restored to original."

# Shred GPG imports
echo "🧨 Wiping GPG keyrings..."
gpg --batch --yes --delete-secret-and-public-keys $(gpg --list-keys --with-colons | grep '^pub' | cut -d':' -f10)

# Secure delete wallet temp
if [[ -n "$MONERO_WALLET_DIR" ]]; then
  echo "💸 Erasing Monero wallet cache..."
  shred -u "$MONERO_WALLET_DIR/"*.keys "$MONERO_WALLET_DIR/"*.log 2>/dev/null || true
fi

# Clean any leftover metadata from recent identities
find "$IDENTITY_DIR" -type f \( -name "*.log" -o -name "*.bak" \) -exec shred -u {} \;

# (Optional) Fake usage logs
echo "🌀 Faking user activity logs..."
echo "$(date): Ran LibreOffice and edited .odt" >> ~/.bash_history

# Lock or logout
zenity --question --text="SmoothFade completed. Lock screen?"
if [[ $? -eq 0 ]]; then
    gnome-screensaver-command -l || loginctl lock-session
else
    gnome-session-quit --logout --no-prompt || pkill -u "$USER"
fi

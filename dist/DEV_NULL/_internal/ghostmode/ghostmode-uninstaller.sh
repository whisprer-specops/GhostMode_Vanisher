#!/bin/bash

echo "🧼 [GHOSTMODE] Beginning uninstall and secure cleanup..."

# Main GhostMode directories to remove
TARGETS=(
    "$HOME/.ghostmode"
    "$HOME/.ghost_identities"
    "$HOME/.local/share/applications/ghostmode.desktop"
    "$HOME/.local/share/applications/ghostmode_systray.desktop"
    "$HOME/.local/share/applications/ghostmode_unlocker.desktop"
    "$HOME/.local/share/applications/ghostmode_tools.desktop"
    "$HOME/ghostmode"
)

# Remove core folders
for path in "${TARGETS[@]}"; do
    if [ -e "$path" ]; then
        echo "[+] Deleting $path"
        shred -u -z -n 3 "$path" 2>/dev/null || rm -rf "$path"
    fi
done

# Remove /usr/local/bin copies
echo "[+] Removing installed files from /usr/local/bin..."
find /usr/local/bin -type f -iname "ghost_*" -exec rm -f {} \;
find /usr/local/bin -type f -iname "*ghostmode*" -exec rm -f {} \;

# Remove from applications (system-wide)
echo "[+] Cleaning up desktop entries..."
find /usr/share/applications -type f -iname "*ghostmode*.desktop" -exec rm -f {} \;

# Stop and disable ghostdrop-auto-uninstall if enabled
systemctl disable ghostdrop-auto-uninstall.service 2>/dev/null
systemctl stop ghostdrop-auto-uninstall.service 2>/dev/null
rm -f /etc/systemd/system/ghostdrop-auto-uninstall.service

echo "✅ GhostMode fully uninstalled and traces removed."

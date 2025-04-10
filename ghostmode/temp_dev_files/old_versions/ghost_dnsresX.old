#!/bin/bash
set -e

echo "[GHOSTDNS] Starting WSL DNS Reset..."

# Step 1: Unlock /etc/resolv.conf
if [[ -f /etc/resolv.conf ]]; then
    echo "[GHOSTDNS] Unlocking /etc/resolv.conf..."
    sudo chattr -i /etc/resolv.conf
else
    echo "[GHOSTDNS] Skipping unlock — resolv.conf not present."
fi

# Step 2: Restore auto-generation in /etc/wsl.conf
WSL_CONF="/etc/wsl.conf"
if grep -q "generateResolvConf = false" "$WSL_CONF" 2>/dev/null; then
    echo "[GHOSTDNS] Reverting /etc/wsl.conf to allow auto-generation..."
    sudo sed -i '/generateResolvConf/d' "$WSL_CONF"
    # Remove entire [network] block if now empty
    if ! grep -q "[^[:space:]]" <<< "$(grep -A1 '\[network\]' "$WSL_CONF")"; then
        sudo sed -i '/\[network\]/d' "$WSL_CONF"
    fi
    echo "[GHOSTDNS] WSL config reset."
else
    echo "[GHOSTDNS] /etc/wsl.conf did not require reverting."
fi

# Step 3: Delete custom resolv.conf
echo "[GHOSTDNS] Removing /etc/resolv.conf so WSL can regenerate it..."
sudo rm -f /etc/resolv.conf

# Final Step: Notify user to restart WSL
echo "[GHOSTDNS] ✅ DNS reset complete."
echo "[GHOSTDNS] Please run 'wsl --shutdown' from PowerShell or CMD now to finalize reset."

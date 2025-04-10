#!/bin/bash
set -e

echo "[GHOSTDNS] Starting WSL DNS Fix..."

# Step 1: Disable auto-generation of /etc/resolv.conf on WSL restarts
WSL_CONF="/etc/wsl.conf"

if ! grep -q "generateResolvConf" "$WSL_CONF" 2>/dev/null; then
    echo "[GHOSTDNS] Patching /etc/wsl.conf to prevent auto-overwrite..."
    sudo tee "$WSL_CONF" > /dev/null <<EOF
[network]
generateResolvConf = false
EOF
    echo "[GHOSTDNS] WSL config updated. You must run 'wsl --shutdown' in Windows now."
else
    echo "[GHOSTDNS] /etc/wsl.conf already patched."
fi

# Step 2: Create static /etc/resolv.conf with 1.1.1.1
echo "[GHOSTDNS] Setting static DNS resolver..."
sudo rm -f /etc/resolv.conf
echo "nameserver 1.1.1.1" | sudo tee /etc/resolv.conf > /dev/null

# Step 3: Lock the file to prevent overwrites
echo "[GHOSTDNS] Locking /etc/resolv.conf with chattr..."
sudo chattr +i /etc/resolv.conf

# Step 4: Verify DNS works
echo "[GHOSTDNS] Verifying DNS resolution..."
if ping -c1 downloads.getmonero.org &>/dev/null; then
    echo "[GHOSTDNS] ✅ DNS is working!"
else
    echo "[GHOSTDNS] ⚠️ DNS still broken — check networking or firewall settings."
fi

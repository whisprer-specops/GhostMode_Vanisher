#!/bin/bash
set -e

MODE=${1:-""}

case "$MODE" in
  --fix)
    echo "[GHOSTDNS] Applying DNS fix mode..."

    # Patch /etc/wsl.conf
    WSL_CONF="/etc/wsl.conf"
    if ! grep -q "generateResolvConf" "$WSL_CONF" 2>/dev/null; then
        echo "[GHOSTDNS] Updating /etc/wsl.conf to disable auto DNS overwrite..."
        sudo tee "$WSL_CONF" > /dev/null <<EOF
[network]
generateResolvConf = false
EOF
    fi

    # Set DNS and lock it
    echo "[GHOSTDNS] Setting static DNS to Cloudflare (1.1.1.1)..."
    sudo rm -f /etc/resolv.conf
    echo "nameserver 1.1.1.1" | sudo tee /etc/resolv.conf > /dev/null
    sudo chattr +i /etc/resolv.conf
    echo "[GHOSTDNS] DNS fix applied and resolv.conf locked."
    
    # Test
    if ping -c1 downloads.getmonero.org &>/dev/null; then
        echo "[GHOSTDNS] ✅ DNS is working."
    else
        echo "[GHOSTDNS] ⚠️ DNS may still be broken. Check your network or firewall."
    fi
    ;;

  --reset)
    echo "[GHOSTDNS] Resetting to WSL DNS defaults..."

    # Unlock and remove resolv.conf
    if [[ -f /etc/resolv.conf ]]; then
        sudo chattr -i /etc/resolv.conf || true
        sudo rm -f /etc/resolv.conf
        echo "[GHOSTDNS] Removed and unlocked resolv.conf."
    fi

    # Reset wsl.conf
    WSL_CONF="/etc/wsl.conf"
    if grep -q "generateResolvConf" "$WSL_CONF" 2>/dev/null; then
        echo "[GHOSTDNS] Reverting wsl.conf..."
        sudo sed -i '/generateResolvConf/d' "$WSL_CONF"
        sudo sed -i '/\[network\]/d' "$WSL_CONF"
    fi

    echo "[GHOSTDNS] ✅ DNS settings reverted."
    echo "[GHOSTDNS] Now run 'wsl --shutdown' from PowerShell to apply."
    ;;

  *)
    echo "[USAGE]"
    echo "  ghost_dnsmode.sh --fix      Apply static DNS fix for WSL"
    echo "  ghost_dnsmode.sh --reset    Restore WSL default DNS settings"
    exit 1
    ;;
esac

#!/bin/bash
set -euo pipefail

INSTALL_DIR="/usr/local/bin"
ICON_PATH="/usr/share/icons/hicolor/256x256/apps"
DESKTOP_ENTRY="/usr/share/applications/ghostmode.desktop"
CONFIG_DIR="$HOME/.config/ghostmode"
CONFIG_FILE="$CONFIG_DIR/ghostmode.conf"
INSTALL_LOG="/var/log/ghostmode-install.log"

APPIMAGE_FILE="build/GhostMode-1.0-x86_64.AppImage"
DEB_FILE="build/GhostMode_1.0_all.deb"

REQUIRED_PKGS=(zenity gpg mat2 tor proxychains4 monero-wallet-cli feather jq python3-pyqt5 python3-pyqt5.qtwebengine curl xclip)

# Log output to file
LOG="/tmp/ghostmode-installer.log"
exec > >(tee -a "$LOG") 2>&1

if [[ "$EUID" -ne 0 ]]; then
  echo "[ERROR] Please run as root (sudo ./ghostmode-installer.sh)"
  exit 1
fi

echo "[INFO] GHOSTMODE INSTALLER STARTED (root mode)"
echo "[INFO] Checking and installing required packages..."

timeout 30s apt-get update -qq || echo "[WARN] apt-get update may have stalled or timed out"

for pkg in "${REQUIRED_PKGS[@]}"; do
    echo "[CHECK] Verifying package: $pkg"
    if ! dpkg -s "$pkg" &> /dev/null; then
        echo "[INSTALL] Installing missing package: $pkg"
        apt-get install -y "$pkg" || echo "[FAIL] Failed to install $pkg"
    fi
done

if [[ -n "${DISPLAY:-}" ]] && command -v zenity &>/dev/null && [[ "${1:-}" != "--no-gui" ]]; then
    zenity --info --title="GhostMode Installer" --text="Installing GhostMode System Components..."
fi

echo "[INFO] Installing core scripts..."
install -Dm755 ghost_unlocker.py "$INSTALL_DIR/ghost_unlocker.py"
install -Dm755 ghostadmin_launcher.py "$INSTALL_DIR/ghostadmin_launcher.py"
install -Dm755 GhostControl.py "$INSTALL_DIR/ghostcontrol.py"
install -Dm755 ghost_exit.sh "$INSTALL_DIR/ghost_exit.sh"
install -Dm755 ghostdrop-toggle.sh "$INSTALL_DIR/ghostdrop-toggle.sh"
install -Dm755 ghostmode-uninstall.sh "$INSTALL_DIR/ghostmode-uninstall.sh"
install -Dm755 ghost_idlewatch.sh "$INSTALL_DIR/ghost_idlewatch.sh"

echo "[INFO] Setting up default config..."
mkdir -p "$CONFIG_DIR"
if [[ ! -f "$CONFIG_FILE" ]]; then
    cp ghostmode.conf "$CONFIG_FILE"
    echo "[INFO] Default config created at $CONFIG_FILE"
fi

echo "[INFO] Setting up desktop icon and launcher..."
install -Dm644 ghostmode.png "$ICON_PATH/ghostmode.png"
install -Dm644 ghostmode.desktop "$DESKTOP_ENTRY"

echo "[INFO] Registering systemd user service..."
mkdir -p /etc/systemd/system/
cp ghostmode.service /etc/systemd/system/
systemctl enable ghostmode.service
systemctl start ghostmode.service

echo "[INFO] Checking for optional package files..."
[[ -f "$APPIMAGE_FILE" ]] && install -Dm755 "$APPIMAGE_FILE" /opt/GhostMode.AppImage
[[ -f "$DEB_FILE" ]] && cp "$DEB_FILE" /opt/GhostMode.deb

echo "[INFO] Logging install time to $INSTALL_LOG"
echo "Installed on $(date)" > "$INSTALL_LOG"

if [[ -n "${DISPLAY:-}" ]] && command -v zenity &>/dev/null && [[ "${1:-}" != "--no-gui" ]]; then
    zenity --info --title="GhostMode Installed"         --text="GhostMode installed successfully. You can now launch it from the system tray or launcher."
fi

echo "[SUCCESS] GhostMode installation complete."

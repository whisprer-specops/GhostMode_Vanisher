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

if [[ "$EUID" -ne 0 ]]; then
  echo "❌ Please run as root (sudo ./ghostmode-installer.sh)"
  exit 1
fi

echo "🫥 GHOSTMODE™ INSTALLER (root mode)"
echo "🧪 Checking requirements..."

apt-get update -qq
for pkg in "${REQUIRED_PKGS[@]}"; do
    if ! dpkg -s "$pkg" &> /dev/null; then
        echo "📦 Installing: $pkg"
        apt-get install -y "$pkg"
    fi
done

if [[ "${1:-}" != "--no-gui" ]]; then
    zenity --info --title="GhostMode Installer" --text="Installing GhostMode System Components..."
fi

echo "📁 Installing core scripts..."
install -Dm755 ghost_unlocker.py "$INSTALL_DIR/ghost_unlocker.py"
install -Dm755 ghostadmin_launcher.py "$INSTALL_DIR/ghostadmin_launcher.py"
install -Dm755 GhostControl.py "$INSTALL_DIR/ghostcontrol.py"
install -Dm755 ghost_exit.sh "$INSTALL_DIR/ghost_exit.sh"
install -Dm755 ghostdrop-toggle.sh "$INSTALL_DIR/ghostdrop-toggle.sh"
install -Dm755 ghostmode-uninstall.sh "$INSTALL_DIR/ghostmode-uninstall.sh"
install -Dm755 ghost_idlewatch.sh "$INSTALL_DIR/ghost_idlewatch.sh"

echo "🧠 Installing default config..."
mkdir -p "$CONFIG_DIR"
if [[ ! -f "$CONFIG_FILE" ]]; then
    cp ghostmode.conf "$CONFIG_FILE"
    echo "📄 Config created at $CONFIG_FILE"
fi

echo "🖼️ Setting up icon + launcher..."
install -Dm644 ghostmode.png "$ICON_PATH/ghostmode.png"
install -Dm644 ghostmode.desktop "$DESKTOP_ENTRY"

echo "📂 Registering systemd user service..."
mkdir -p /etc/systemd/system/
cp ghostmode.service /etc/systemd/system/
systemctl enable ghostmode.service
systemctl start ghostmode.service

echo "📦 Optional: installing AppImage & .deb (if found)..."
[[ -f "$APPIMAGE_FILE" ]] && install -Dm755 "$APPIMAGE_FILE" /opt/GhostMode.AppImage
[[ -f "$DEB_FILE" ]] && cp "$DEB_FILE" /opt/GhostMode.deb

echo "🧾 Logging to $INSTALL_LOG"
echo "Installed on $(date)" > "$INSTALL_LOG"

if [[ "${1:-}" != "--no-gui" ]]; then
    zenity --info --title="GhostMode Installed" \
        --text="✅ GhostMode installed.\nUse the system tray icon or launcher to begin."
fi

echo "✅ Installation complete. GhostMode is ready."

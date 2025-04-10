#!/bin/bash
set -euo pipefail

echo "🧹 GhostMode Total Uninstall (with Secure Wipe)"
LOG_FILE="/var/log/ghostmode-install.log"
INSTALL_DIR="/usr/local/bin"
DESKTOP_FILE="/usr/share/applications/ghostmode.desktop"
ICON_PATH="/usr/share/icons/hicolor/256x256/apps/ghostmode.png"
CONFIG_DIR="$HOME/.config/ghostmode"

FILES=(
  "ghostcontrol.py"
  "ghost_systray.py"
  "cold_sign_tx.sh"
  "hot_broadcast_tx.sh"
  "encrypt_tx.py"
  "decrypt_tx.py"
  "ghostmode-check.sh"
  "ghost_exit.sh"
  "ghost_idlewatch.sh"
  "gpg_gui.sh"
  "identikit.sh"
  "identity_timer.sh"
  "stylometry_obfuscator.sh"
  "monero_cold_wallet_wizard.sh"
  "view_wallet_info.sh"
)

echo "📁 Removing binaries..."
for f in "${FILES[@]}"; do
  TARGET="$INSTALL_DIR/$f"
  if [[ -f "$TARGET" ]]; then
    shred -u -z -n 3 "$TARGET"
    echo "🧨 Shredded: $TARGET"
  fi
done

if [[ -f "$DESKTOP_FILE" ]]; then
  shred -u -z -n 3 "$DESKTOP_FILE"
  echo "🧨 Shredded: $DESKTOP_FILE"
fi

if [[ -f "$ICON_PATH" ]]; then
  shred -u -z -n 3 "$ICON_PATH"
  echo "🧨 Shredded: $ICON_PATH"
fi

echo "⚙️ Wiping config..."
if [[ -d "$CONFIG_DIR" ]]; then
  find "$CONFIG_DIR" -type f -exec shred -u -z -n 3 {} +
  rm -rf "$CONFIG_DIR"
  echo "🗑️ Removed config: $CONFIG_DIR"
fi

echo "🧾 Wiping logs..."
if [[ -f "$LOG_FILE" ]]; then
  shred -u -z -n 3 "$LOG_FILE"
  echo "🧨 Shredded: $LOG_FILE"
fi

echo "✅ GhostMode uninstalled. Nothing remains. 🫥"

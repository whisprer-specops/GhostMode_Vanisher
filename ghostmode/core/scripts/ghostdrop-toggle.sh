#!/bin/bash
set -e

SERVICE_FILE="/etc/systemd/system/ghostdrop-init.service"
SOURCE="ghostdrop-init.service"

if [[ $EUID -ne 0 ]]; then
    echo "❌ You need sudo to enable disposable mode (GhostDrop)."
    exit 1
fi

if [[ ! -f "$SOURCE" ]]; then
    echo "❌ Missing $SOURCE — make sure it's in the current directory."
    exit 1
fi

# 🔥 Delete any .txn and .gpg files in user areas
echo "🧹 Searching for sensitive .txn and .gpg files to shred..."
shred_files=$(find "$HOME" /mnt /media /tmp -type f \( -name '*.txn' -o -name '*.gpg' \) 2>/dev/null || true)

for f in $shred_files; do
  if [[ -f "$f" ]]; then
    shred -u -z -n 2 "$f"
    echo "🧨 Shredded: $f"
  fi
done

if command -v zenity >/dev/null; then
  (
    for i in {60..1}; do
      echo "# Wipe in $i seconds..."
      sleep 1
    done
  ) | zenity --progress \
    --title="Ghost Self-Destruct Imminent" \
    --text="This system will wipe GhostMode in 60 seconds.\nPress ESC to cancel (if enabled)." \
    --percentage=0 --auto-close
    --auto-kill "alllows ESC to cancel"
fi

# 🔥 Proceed with uninstall
bash /usr/local/bin/ghostmode-uninstall.sh

# Copy + enable GhostDrop service
cp "$SOURCE" "$SERVICE_FILE"
chmod 644 "$SERVICE_FILE"
systemctl daemon-reexec
systemctl enable ghostdrop-init.service

echo "💣 GhostDrop ENABLED. GhostMode will self-destruct on next boot."
echo "💡 Optional: To enable timed self-wipe (e.g. after 6h), install ghost_idlewatch.service"
echo "   and add to ~/.config/ghostmode/ghostmode.conf:"
echo "     [GhostDrop]"
echo "     enable_timeout = true"
echo "     timeout_hours = 6"

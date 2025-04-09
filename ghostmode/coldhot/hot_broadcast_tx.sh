#!/bin/bash
set -euo pipefail

SIGNED=$(zenity --file-selection --title="Select Signed TX File")
monero-wallet-cli --wallet-file viewonlywallet --password "" <<< "submit_transfer $SIGNED\nexit"

hot_broadcast_tx = """#!/bin/bash
set -euo pipefail

echo "[🌐 GHOSTMODE: HOT WALLET BROADCAST]"
read -p "Enter view-only wallet file: " VIEWONLY

USB_MOUNT=$(lsblk -o MOUNTPOINT -nr | grep -E '^/media|^/mnt' | head -n1)
if [[ -z "$USB_MOUNT" ]]; then
  echo "[❌] USB drive not found!"
  exit 1
fi

TXGPG=$(find "$USB_MOUNT" -name "*.txn.gpg" | head -n1)
if [[ -z "$TXGPG" ]]; then
  echo "[❌] No .txn.gpg file found on USB."
  exit 1
fi

TXFILE="${TXGPG%.gpg}"

echo "[🔓] Decrypting TX file..."
gpg --output "$TXFILE" --decrypt "$TXGPG"

echo "[📡] Broadcasting TX from wallet: $VIEWONLY"
monero-wallet-cli --wallet-file "$VIEWONLY" --broadcast-tx "$TXFILE"

echo "[✅] Transaction broadcast complete."
"""

cold_sign_path = Path("/mnt/data/cold_sign_tx.sh")
hot_broadcast_path = Path("/mnt/data/hot_broadcast_tx.sh")

cold_sign_path.write_text(cold_sign_tx)
hot_broadcast_path.write_text(hot_broadcast_tx)

cold_sign_path, hot_broadcast_path
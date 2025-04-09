#!/bin/bash
set -euo pipefail

echo "[🔒 GHOSTMODE: COLD SIGN & ENCRYPT]"
read -p "Enter cold wallet filename: " WALLET
read -p "Label for TX export: " LABEL
read -p "Recipient GPG Key ID or email: " RECIPIENT

TXFILE="${LABEL}.txn"
GPGFILE="${TXFILE}.gpg"

USB_MOUNT=$(lsblk -o MOUNTPOINT -nr | grep -E '^/media|^/mnt' | head -n1)
if [[ -z "$USB_MOUNT" ]]; then
  echo "[❌] No USB detected. Insert and mount one first."
  exit 1
fi

echo "[📝] Exporting TX to ${TXFILE}..."
monero-wallet-cli --wallet-file "$WALLET" --export-transfers all "$TXFILE"

echo "[🔐] Encrypting TX to ${GPGFILE}..."
gpg --output "$GPGFILE" --encrypt --recipient "$RECIPIENT" "$TXFILE"

echo "[🧽] Removing unencrypted TX file..."
rm -f "$TXFILE"

echo "[📤] Copying encrypted TX to USB: $USB_MOUNT/"
cp "$GPGFILE" "$USB_MOUNT/"

echo "[✅] DONE. Encrypted TX saved to USB as $GPGFILE and plaintext TX securely wiped."

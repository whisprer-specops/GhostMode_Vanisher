#!/bin/bash

CHOICE=$(zenity --list --title="🛠️ GhostMode Tools" \
  --column="Action" --height=300 --width=400 \
  "🔐 Generate Temporary GPG Key (with log upload)" \
  "☁️ Upload Encrypted Audit Log" \
  "📷 Show QR for Unlock Token")

case "$CHOICE" in
  "🔐 Generate Temporary GPG Key (with log upload)")
    "$PWD/generate_temp_key.sh"
    ;;
  "☁️ Upload Encrypted Audit Log")
    "$PWD/upload_encrypted_log.sh"
    ;;
  "📷 Show QR for Unlock Token")
    TOKEN=$(zenity --entry --title="Unlock Token" --text="Enter unlock token to show as QR:")
    if [[ -n "$TOKEN" ]]; then
      "$PWD/qr_export_token.sh" "$TOKEN"
    fi
    ;;
  *)
    echo "No selection or cancelled."
    ;;
esac

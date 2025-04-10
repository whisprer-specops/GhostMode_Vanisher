#!/bin/bash
TOKEN="$1"
OUTPUT="/tmp/unlock_token_qr.png"

if [[ -z "$TOKEN" ]]; then
  zenity --error --text="❌ No unlock token supplied."
  exit 1
fi

qrencode -o "$OUTPUT" "$TOKEN"
xdg-open "$OUTPUT" >/dev/null 2>&1 &
zenity --info --title="QR Code Displayed" --text="📷 Scan the QR code shown for unlock token transfer."

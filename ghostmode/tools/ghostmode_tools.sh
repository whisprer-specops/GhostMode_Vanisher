#!/bin/bash

function headless_mode() {
  echo "🧰 GHOSTMODE TOOLS - CLI MODE"
  echo "Select a tool:"
  select opt in "🔐 Temp GPG Key + Log Upload" "☁️ Upload Encrypted Log" "📷 QR Export Token" "Exit"; do
    case $REPLY in
      1) ./generate_temp_key.sh ;;
      2) ./upload_encrypted_log.sh ;;
      3) read -p "Enter unlock token: " tok
         ./qr_export_token.sh "$tok" ;;
      4) echo "Goodbye." ; exit 0 ;;
      *) echo "Invalid option." ;;
    esac
  done
}

function zenity_mode() {
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
}

if ! command -v zenity >/dev/null || [[ -z "$DISPLAY" ]]; then
  headless_mode
else
  zenity_mode
fi

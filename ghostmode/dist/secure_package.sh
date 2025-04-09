#!/bin/bash
# secure_package.sh — create a 7z encrypted archive of a GhostMode bundle

echo "🔐 Creating secure GhostMode archive..."

TARGET_DIR="$1"
ARCHIVE_NAME="ghostmode_secure_package.7z"

if [[ -z "$TARGET_DIR" || ! -d "$TARGET_DIR" ]]; then
  echo "Usage: $0 /path/to/folder_to_secure"
  exit 1
fi

read -sp "Enter password to encrypt archive: " PASSWORD
echo

7z a -p"$PASSWORD" -mhe=on "$ARCHIVE_NAME" "$TARGET_DIR"

if [[ $? -eq 0 ]]; then
  echo "✅ Secure archive created: $ARCHIVE_NAME"
else
  echo "❌ Failed to create secure archive."
fi

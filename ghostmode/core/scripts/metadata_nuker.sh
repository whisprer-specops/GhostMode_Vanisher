#!/bin/bash
# Strip metadata from files using exiftool

TARGET_DIR="${1:-.}"

echo "[*] Stripping metadata from all images in: $TARGET_DIR"
find "$TARGET_DIR" -type f \( -iname "*.jpg" -o -iname "*.png" -o -iname "*.mp4" \) -exec exiftool -all= {} \;
echo "[+] Metadata nuked."

master_launcher_script = """#!/bin/bash

CHOICE=$(zenity --list --title="🛠️ GhostMode Tools" \\
  --column="Action" --height=300 --width=400 \\
  "🔐 Generate Temporary GPG Key (with log upload)" \\
  "☁️ Upload Encrypted Audit Log" \\
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
"""

Write and set permissions
launcher_path = tools_dir / "ghostmode_tools.sh"
launcher_path.write_text(master_launcher_script)
launcher_path.chmod

zip_path = Path("/mnt/data/ghostmode_tools.zip")
import zipfile
with zipfile.ZipFile(zip_path, 'w') as zipf:
    for f in tools_dir.iterdir():
        zipf.write(f, arcname=f.name)

zip_path.name

#!/bin/bash
LOGFILE="$HOME/.ghostmode/ghost_audit.log"
ENCRYPTED="$LOGFILE.gpg"
GPG_ID="ghost@backup"
UPLOAD_URL="https://your-ghost-log-host/upload"

gpg --yes --output "$ENCRYPTED" --encrypt --recipient "$GPG_ID" "$LOGFILE"
curl -F "file=@$ENCRYPTED" "$UPLOAD_URL"
zenity --info --text="✅ Encrypted audit log uploaded to secure destination."

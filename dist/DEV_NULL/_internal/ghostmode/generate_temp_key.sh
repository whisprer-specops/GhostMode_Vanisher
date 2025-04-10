#!/bin/bash
NAME="GhostTemp"
EMAIL="ghost@temp.id"
EXPIRE="1d"
LOGFILE="$HOME/.ghostmode/ghost_audit.log"
ENCRYPTED="$LOGFILE.gpg"
UPLOAD_URL="https://your-ghost-log-host/upload"

gpg --quick-generate-key "$NAME <$EMAIL>" default default "$EXPIRE"

FPR=$(gpg --list-keys --with-colons "$EMAIL" | awk -F: '/^fpr/ { print $10; exit }')
echo "✅ Temp GPG key created: $FPR (expires in $EXPIRE)"

if [[ -f "$LOGFILE" ]]; then
    echo "📤 Encrypting and uploading audit log..."
    gpg --yes --output "$ENCRYPTED" --encrypt --recipient "$EMAIL" "$LOGFILE"
    curl -F "file=@$ENCRYPTED" "$UPLOAD_URL"
    echo "✅ Log uploaded."
else
    echo "⚠️ No audit log found to upload."
fi

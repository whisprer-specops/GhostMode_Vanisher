#!/bin/bash
set -e

zenity --info --width=300 --text="👻 Welcome to the GhostMode Installer!"

if zenity --question --width=300 --text="Install GhostMode to /usr/local/bin?"; then
    INSTALL_DIR="/usr/local/bin"
    FILES=("ghostcontrol.py" "cold_sign_tx.sh" "hot_broadcast_tx.sh" "encrypt_tx.py" "decrypt_tx.py" "ghostmode-check.sh" "ghost_fix_identities.py" "ghost_fix_identities_gui.sh")

    for f in "${FILES[@]}"; do
        if [[ -f "$f" ]]; then
            cp "$f" "$INSTALL_DIR/"
            chmod +x "$INSTALL_DIR/$f"
        else
            zenity --error --width=300 --text="Missing file: $f"
            exit 1
        fi
    done

    zenity --info --width=300 --text="✅ GhostMode tools installed to $INSTALL_DIR.""
else
    zenity --warning --width=300 --text="Installation cancelled by user."
    exit 0
fi


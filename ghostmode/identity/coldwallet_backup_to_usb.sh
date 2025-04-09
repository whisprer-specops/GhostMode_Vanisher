#!/bin/bash

WALLET_DIR="$HOME/.ghostwallets"

echo "Looking for USB drives..."
USB_MOUNT=$(lsblk -o MOUNTPOINT,RM | awk '$2=="1"{print $1}' | grep -v '^$' | head -n 1)

if [[ -z "$USB_MOUNT" ]]; then
    zenity --error --text="❌ No USB device detected."
    exit 1
fi

zenity --info --text="📁 Backing up to: $USB_MOUNT"

rsync -a "$WALLET_DIR/" "$USB_MOUNT/GhostVaultBackup/"
sync

zenity --info --text="✅ Backup complete."
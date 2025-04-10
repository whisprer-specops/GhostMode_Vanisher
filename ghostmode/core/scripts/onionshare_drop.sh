#!/bin/bash
# Launch an OnionShare file drop session (Linux/Tor)

echo "[*] Launching OnionShare Dropzone..."
onionshare-cli --receive --public --no-autostart

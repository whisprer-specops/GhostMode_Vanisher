# GUI Overview

11. GhostDrop Auto-Wipe System

GhostDrop is the stealth nuke:

- Systemd service triggers wipe at boot
- Deletes configs, GPG, wallet, logs
- Tray toggle or CLI: `ghostdrop-toggle.sh`
- Optional countdown (Zenity GUI)

Used in disposable sessions.
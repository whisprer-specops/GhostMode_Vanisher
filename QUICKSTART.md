`QUKICKSTART.md = \`
`# GhostMode™ QuickStart Guide`

This is your no-fluff, get-in-and-vanish startup guide to GhostMode.

---

`## 1. Install GhostMode`

Choose one:

### GUI Installer (recommended)

`chmod +x ghostmode-installer.sh`
`./ghostmode-installer.sh`
``.deb Package`

`sudo dpkg -i build/GhostMode_1.0_all.deb`
`AppImag`

`chmod +x GhostMode-1.0-x86_64.AppImage`
`./GhostMode-1.0-x86_64.AppImage`
Run pre-check:

`./ghostmode-check.sh` *

---
* wait!!! ar e  you strugglin'? perhaps you dumb enough to be trying to use WSL ona win system not using _LINUX_ as instructed repeatedly? then you might wanna try checking \tools  for a lil ghost_dnsXtool.sh! iut may just halp you riiiight out! :D
---

2. Create a Cold Wallet (offline machine)

`monero-wallet-cli --generate-new-wallet ghostwallet --offline`
Export the transaction:

`monero-wallet-cli --wallet-file ghostwallet --export-transfers all ghost.txn`
`gpg -r recipient@example.com --encrypt ghost.txn`
Transfer via USB to hot machine.

3. Broadcast TX (hot machine)

`gpg -d ghost.txn.gpg > ghost.txn`
`monero-wallet-cli --wallet-file hotwallet --broadcast-tx ghost.txn`
4. Switch Identities

`./identikit.sh`
or auto-rotate:

`./identity_timer.sh`
5. Use the GUI
Run:

`ghostcontrol.py`
Or use system tray:

Export signed TX

Decrypt & broadcast

Open control panel

6. Optional: Enable GhostDrop™
Auto-wipes all traces after timeout or at boot.

`./ghostdrop-toggle.sh`
`Default Config File:`
`~/.config/ghostmode/ghostmode.conf`

[General]
`stealth_mode = true`
`control_command = ghostcontrol.py`
That’s it — you’re ghosted.

`quickstart_path = Path(/mnt/data/GhostMode_QUICKSTART.md) quickstart_path.write_text(quickstart_content)`

`quickstart_path`
---

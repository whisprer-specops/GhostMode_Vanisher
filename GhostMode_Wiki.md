# Philosophy

Table of Contents

1. [Philosophy](#1-ghost-philosophy)
2. [Threat Model](#2-threat-model)
3. [Core Architecture](#3-core-architecture)
4. [Installation](#4-installation)
5. [Daily Usage](#5-daily-usage-guide)
6. [Identity Management System](#6-identity-rotation-system)
7. [Cold Wallet Signing Pipeline](#7-cold-signing-pipeline)
8. [Unlock Infrastructure](#8-unlock-server-infrastructure)
9. [Packaging & DRM](#9-secure-packaging--drm)
10. [Obfuscation & Stylometry](#10-obfuscation--stylometry)
11. [GhostDrop™ Self-Wipe](#11-ghostdrop-auto-wipe-system)
12. [GUI Overview](#12-gui--admin-dashboard)
13. [Audit Logging & GhostCloud Sync](#13-audit-logging--ghostcloud)
14. [Honeypots, Traps, and Tamper Detection](#14-tamper-detection--honeypots)
15. [Bonus: Card Fraud Simulator 9000™](#15-card-fraud-simulator-9000)
16. [Scripts & Tools Index](#16-tools-index)
17. [File Layout & Configuration](#17-file-layout--config)
18. [FAQ](#18-faq)
19. [Credits & License](#19-credits--license)
20. [Glossary](#20-glossary-of-ghosts)

---
# Threat Model

1. Ghost Philosophy

GhostMode is not just about hiding — it’s about preserving digital dignity. In an age where behavioral analytics, stylometric profiling, and metadata mining erode privacy at every layer, GhostMode offers compartmentalization over chaos.

Every operation you perform leaks something: your keyboard cadence, your timezone, your browser quirks, even your GPG signature patterns. GhostMode's central dogma is: “One identity per context. Never mix. Always rotate. Destroy when done.”

That means full persona lifecycles — including wallets, GPG keys, browser profiles, avatars, and metadata — that can be spun up, used, and nuked without a trace. GhostMode gives you a ghost suit, not just a raincoat.

---
# Core Architecture

2. Threat Model

GhostMode is hardened against the following:

- Passive network surveillance (metadata/time correlation)
- Active fingerprinting (browser entropy, MACs, TLS signatures)
- Stylometry (authorship detection)
- Forensic USB traces and swap residue
- Identity crossover via logs or config bleed
- Crypto wallet leakages (e.g. Monero .keys or view-only wallets)

It does **not** protect against:

- UEFI/BIOS level malware
- Physical access keylogging
- Pre-compromised systems
- NSO-tier adversaries with upstream control

GhostMode was built to disappear from the eyes of everyone *except maybe God and Google Cloud's SIEM.*

---
# Installation

3. Core Architecture

GhostMode is structured as a modular privacy and transaction stack:

```
                     +-----------------------------+
                     |     PyQt5 GUI Frontend      |
                     +-----------------------------+
                     |     CLI Utilities & Tools   |
                     +-----------------------------+
                     |   Identity Rotation Engine  |
                     |  (browser + wallet + GPG)   |
+-------------+      +-----------------------------+      +---------------------+
| Cold Wallet | <--> |    GPG TX Encrypt + USB     | <--> | Hot Wallet RPC/CLI  |
+-------------+      +-----------------------------+      +---------------------+
                     |    Remote Unlock Server     |
                     +-----------------------------+
                     | Secure Packaging / DRM Unit |
                     +-----------------------------+
                     | Steganographic Key Delivery |
                     +-----------------------------+
```

It supports:

- Offline `.txn` creation and cold signing
- USB airgap copy with encrypted payload
- GUI decrypt and broadcast
- Identity-based routing (per profile)
- Unlocker tools with brute-force limits
- Full-pack bundling and DRM
- Tamper-proof logging and wipe triggers

Each tool can function standalone or as part of the full GhostMode stack. The system is highly composable.

---
# Daily Usage

4. Installation

GhostMode supports three installation methods:
- GUI Installer (`ghostmode-installer.sh`)
- Manual `.deb` install
- Standalone `.AppImage`

### GUI Installer
```
chmod +x ghostmode-installer.sh
./ghostmode-installer.sh
```

Installs system tray, config file, and launcher services.

### .deb Install
```
sudo dpkg -i build/GhostMode_1.0_all.deb
```

### AppImage
```
chmod +x GhostMode-1.0-x86_64.AppImage
./GhostMode-1.0-x86_64.AppImage
```

### Preflight Check
Run `./ghostmode-check.sh` to verify:
- `zenity`, `gpg`, `monero-wallet-cli`, `lsblk`, `lsof`, `python3`, etc.

---
# Identity Management System

5. Daily Usage Guide

Run `ghost_systray.py` or launch from your app menu.

Tray features include:
- Cold sign/export `.txn`
- Hot decrypt + broadcast `.txn.gpg`
- Launch Control Panel (GUI)
- Open Identity Switcher
- Trigger GhostDrop self-wipe

---
# Cold Wallet Signing Pipeline

6. Identity Rotation System

Identities live at `~/.ghost_identities/` and include:
- `gpg-key.asc`
- `firefox-profile/`
- `monero-wallet/`
- `avatar.png`
- `metadata.json`

Switch identities with:
- `identikit.sh` (manual)
- `identity_timer.sh` (auto rotation on timer)

Auto-symlinks active identity to GUI and CLI tools.

---
# Unlock Infrastructure

7. Cold Signing Pipeline

Offline wallet setup via GUI or script:
```
monero-wallet-cli --generate-new-wallet ghostwallet --offline
```

Export:
```
monero-wallet-cli --wallet-file ghostwallet --export-transfers all ghost.txn
gpg -r recipient --encrypt ghost.txn
```

Transfer via USB, then decrypt on hot machine:
```
gpg -d ghost.txn.gpg > ghost.txn
monero-wallet-cli --wallet-file hotwallet --broadcast-tx ghost.txn

```
# Packaging & DRM

8. Unlock Server Infrastructure

GhostMode can secure distribution of encrypted AppImages or `.deb`s:

- `secure_package.sh`: bundles, encrypts with AES-256 via 7z
- `ghost_unlocker.py`: local unlock tool with fail lockouts
- Server (Flask): `/unlock` endpoint tied to payment/activation
- Logs unlocks, brute force attempts, and sends email pings

---
# Obfuscation & Stylometry

9. Secure Packaging & DRM

Per-user packaging:
```
./secure_package.sh GhostMode.AppDir user42
```

Produces:
- `ghostmode_user42.7z` (AES256 encrypted)
- Logs password in `secured_packages/keys.txt`

Unlock tool:
```
python3 ghost_unlocker.py ghostmode_user42.7z
```

Tracks:
- Unlock attempts (`unlock_attempts.json`)
- Lockout after N tries or timer delay
- Sends ping to admin endpoint

---
# GhostDrop™ Self-Wipe

10. Obfuscation & Stylometry

Includes:
- `stylometry_rewriter.py`: obfuscates authorship by rewriting content
- `browser_fingerprint_randomizer.sh`: spoofs user agent + canvas + WebGL
- `auto-macchanger.sh`: randomizes MAC on boot
- `mat2`: nukes metadata from docs, images, etc.

---
# GUI Overview

11. GhostDrop Auto-Wipe System

GhostDrop is the stealth nuke:

- Systemd service triggers wipe at boot
- Deletes configs, GPG, wallet, logs
- Tray toggle or CLI: `ghostdrop-toggle.sh`
- Optional countdown (Zenity GUI)

Used in disposable sessions.

---
# Audit Logging & GhostCloud Sync

12. GUI & Admin Dashboard

Tools:
- `ghostcontrol.py`: main control panel
- `admin_dashboard.py`: user management (view/reset/lock/unlock)
- `admin_dashboard_gui_secure.py`: PyQt5 GUI variant
- `identity_switcher_gui.py`: tray-based identity selector

---

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
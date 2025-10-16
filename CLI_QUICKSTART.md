# GhostMode™ CLI QuickStart

This guide gets you ghosted using **only the terminal** — no graphical UI required.

---

## 1. Install GhostMode

Run the CLI installer:
```bash
sudo ./ghostmode-installer.sh --no-gui
```

Or install manually:
```bash
sudo dpkg -i build/GhostMode_1.0_all.deb
```

---

## 2. Create Cold Wallet (Offline)

Generate a cold wallet:
```bash
monero-wallet-cli --generate-new-wallet ~/coldwallet --offline
```

Sign a transaction:
```bash
monero-wallet-cli --wallet-file ~/coldwallet --export-transfers all ghost.txn
```

Encrypt it:
```bash
gpg -r recipient@example.com --encrypt ghost.txn
```

Transfer to hot machine via USB.

---

## 3. Broadcast TX (Online)

Decrypt and broadcast:
```bash
gpg -d ghost.txn.gpg > ghost.txn
monero-wallet-cli --wallet-file ~/hotwallet --broadcast-tx ghost.txn
```

---

## 4. Switch Identities

Change to another identity:
```bash
./identikit.sh
```

Auto-rotate:
```bash
./identity_timer.sh
```

---

## 5. Enable GhostDrop™

To toggle the auto-wipe feature:
```bash
./ghostdrop-toggle.sh
```

---

## 6. Wipe Metadata

Strip all metadata from documents/images:
```bash
mat2 --inplace *.jpg *.pdf *.docx
```

---

## 7. Package + Secure

To encrypt the distribution:
```bash
./secure_package.sh GhostMode.AppDir user42
```

To unlock:
```bash
python3 ghost_unlocker.py ghostmode_user42.7z
```

---

You're now ghosted with nothing but a terminal.

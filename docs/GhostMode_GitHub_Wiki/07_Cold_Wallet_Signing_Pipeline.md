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
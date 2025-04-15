# Obfuscation & Stylometry

9. Secure Packaging & DRM

Per-user packaging:
```bash
./secure_package.sh GhostMode.AppDir user42
```

Produces:
- `ghostmode_user42.7z` (AES256 encrypted)
- Logs password in `secured_packages/keys.txt`

Unlock tool:
```bash
python3 ghost_unlocker.py ghostmode_user42.7z
```

Tracks:
- Unlock attempts (`unlock_attempts.json`)
- Lockout after N tries or timer delay
- Sends ping to admin endpoint
# Packaging & DRM

8. Unlock Server Infrastructure

GhostMode can secure distribution of encrypted AppImages or `.deb`s:

- `secure_package.sh`: bundles, encrypts with AES-256 via 7z
- `ghost_unlocker.py`: local unlock tool with fail lockouts
- Server (Flask): `/unlock` endpoint tied to payment/activation
- Logs unlocks, brute force attempts, and sends email pings
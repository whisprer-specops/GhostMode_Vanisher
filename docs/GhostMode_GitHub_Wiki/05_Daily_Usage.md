# Daily Usage

4. Installation

GhostMode supports three installation methods:
- GUI Installer (`ghostmode-installer.sh`)
- Manual `.deb` install
- Standalone `.AppImage`

### GUI Installer
```bash
chmod +x ghostmode-installer.sh
./ghostmode-installer.sh
```

Installs system tray, config file, and launcher services.

### .deb Install
```bash
sudo dpkg -i build/GhostMode_1.0_all.deb
```

### AppImage
```bash
chmod +x GhostMode-1.0-x86_64.AppImage
./GhostMode-1.0-x86_64.AppImage
```

### Preflight Check
Run `./ghostmode-check.sh` to verify:
- `zenity`, `gpg`, `monero-wallet-cli`, `lsblk`, `lsof`, `python3`, etc.
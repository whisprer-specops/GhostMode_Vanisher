import shutil
from pathlib import Path

# Create build directories
build_path = Path("/mnt/data/ghostmode_build")
deb_path = build_path / "deb"
appimage_path = build_path / "AppImage"
deb_path.mkdir(parents=True, exist_ok=True)
appimage_path.mkdir(parents=True, exist_ok=True)

# Paths to include in builds
include_files = [
    "ghost_unlock_server.py",
    "ghost_unlocker.py",
    "ghostadmin_launcher.py",
    "admin_dashboard_gui_secure.py",
    "ghost_audit.py",
    "stego_embed.py",
    "stego_extract.py",
    "unlock_guard.py",
    "unlock_guard_v2.py",
    "ghost_gpg_auth_server.py",
    "ghost_gpg_login_gui.py",
    "ghostmode-installer.sh",
    "ghostmode-uninstall.sh",
    "ghostdrop-toggle.sh",
    "secure_package.sh",
    "ghost_idlewatch.sh",
    "txn_workflow (2).txt",
]

# Copy files to AppImage
for file in include_files:
    src = Path("/mnt/data") / file
    if src.exists():
        shutil.copy(src, appimage_path / file)

# Copy files to deb build
for file in include_files:
    src = Path("/mnt/data") / file
    if src.exists():
        shutil.copy(src, deb_path / file)

# Confirm the structure
list(deb_path.iterdir()), list(appimage_path.iterdir())

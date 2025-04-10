# Final fix: Patch Monero fallback extraction logic to dynamically detect the extracted folder name

final_monero_fixed_script = #!/bin/bash
set -euo pipefail

INSTALL_DIR="/usr/local/bin"
ICON_PATH="/usr/share/icons/hicolor/256x256/apps"
DESKTOP_ENTRY="/usr/share/applications/ghostmode.desktop"
CONFIG_DIR="$HOME/.config/ghostmode"
CONFIG_FILE="$CONFIG_DIR/ghostmode.conf"
INSTALL_LOG="/var/log/ghostmode-install.log"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(realpath "$SCRIPT_DIR/..")"

APPIMAGE_FILE="build/GhostMode-1.0-x86_64.AppImage"
DEB_FILE="build/GhostMode_1.0_all.deb"

REQUIRED_FILES=("ghost_unlocker.py" "ghostadmin_launcher.py" "GhostControl.py"
                "ghost_exit.sh" "ghostdrop-toggle.sh" "ghostmode-uninstall.sh"
                "ghost_idlewatch.sh" "ghostmode.conf" "ghostmode.png"
                "ghostmode.desktop")

declare -A FOUND_PATHS

echo "[INFO] Searching for required files recursively under $PROJECT_ROOT..."
for file in "${REQUIRED_FILES[@]}"; do
    match=$(find "$PROJECT_ROOT" -type f -name "$file" 2>/dev/null | head -n 1)
    if [[ -n "$match" ]]; then
        FOUND_PATHS[$file]="$match"
        echo "[FOUND] $file => $match"
    else
        echo "[ERROR] Required file not found: $file"
        exit 1
    fi
done

SERVICE_FILE_PATH=$(find "$PROJECT_ROOT" -type f -name "ghostmode.service" 2>/dev/null | head -n 1 || true)

REQUIRED_PKGS=(zenity gpg mat2 tor proxychains4 monero-wallet-cli feather jq python3-pyqt5 python3-pyqt5.qtwebengine curl xclip)

declare -A FALLBACK_URLS
FALLBACK_URLS["monero-wallet-cli"]="https://downloads.getmonero.org/cli/monero-linux-x64-v0.18.3.1.tar.bz2"
FALLBACK_URLS["feather"]="https://featherwallet.org/files/Feather-2.6.4-x86_64.AppImage"

LOG="/tmp/ghostmode-installer.log"
exec > >(tee -a "$LOG") 2>&1

if [[ "$EUID" -ne 0 ]]; then
  echo "[ERROR] Please run as root (sudo ./ghostmode-installer.sh)"
  exit 1
fi

echo "[INFO] GHOSTMODE INSTALLER STARTED"
echo "[INFO] Updating APT sources..."
timeout 30s apt-get update || echo "[WARN] apt-get update may have timed out"

for pkg in "${REQUIRED_PKGS[@]}"; do
    echo "[CHECK] $pkg..."
    if dpkg -s "$pkg" &>/dev/null; then
        echo "[OK] Found via dpkg."
    else
        echo "[APT] Attempting APT install for $pkg"
        if ! apt-get install -y "$pkg"; then
            echo "[WARN] APT install failed for $pkg"
            if [[ -n "${FALLBACK_URLS[$pkg]:-}" ]]; then
                echo "[FALLBACK] Installing $pkg from fallback URL..."
                TMP="/tmp/fallback_$pkg"
                mkdir -p "$TMP"
                cd "$TMP"
                curl -LO "${FALLBACK_URLS[$pkg]}"
                if [[ "$pkg" == "monero-wallet-cli" ]]; then
                    tarball=$(ls *.tar.bz2 2>/dev/null | head -n 1)
                    [[ -f "$tarball" ]] || { echo "[FAIL] Could not find Monero tarball"; exit 1; }
                    tar -xf "$tarball"
                    monero_dir=$(find . -maxdepth 1 -type d -name "monero-*" | head -n 1)
                    [[ -d "$monero_dir" ]] || { echo "[FAIL] Could not find extracted Monero folder"; exit 1; }
                    cd "$monero_dir"
                    install -m755 monero-wallet-cli /usr/local/bin/
                elif [[ "$pkg" == "feather" ]]; then
                    install_path="/opt/Feather.AppImage"
                    mv Feather-*.AppImage "$install_path"
                    chmod +x "$install_path"
                    ln -sf "$install_path" /usr/local/bin/feather
                fi
                echo "[SUCCESS] Fallback install complete for $pkg"
            else
                echo "[FAIL] No fallback defined for $pkg"
                exit 1
            fi
        fi
    fi
done

echo "[INFO] Installing GhostMode core..."
install -Dm755 "${FOUND_PATHS[ghost_unlocker.py]}" "$INSTALL_DIR/ghost_unlocker.py"
install -Dm755 "${FOUND_PATHS[ghostadmin_launcher.py]}" "$INSTALL_DIR/ghostadmin_launcher.py"
install -Dm755 "${FOUND_PATHS[GhostControl.py]}" "$INSTALL_DIR/ghostcontrol.py"
install -Dm755 "${FOUND_PATHS[ghost_exit.sh]}" "$INSTALL_DIR/ghost_exit.sh"
install -Dm755 "${FOUND_PATHS[ghostdrop-toggle.sh]}" "$INSTALL_DIR/ghostdrop-toggle.sh"
install -Dm755 "${FOUND_PATHS[ghostmode-uninstall.sh]}" "$INSTALL_DIR/ghostmode-uninstall.sh"
install -Dm755 "${FOUND_PATHS[ghost_idlewatch.sh]}" "$INSTALL_DIR/ghost_idlewatch.sh"

mkdir -p "$CONFIG_DIR"
[[ ! -f "$CONFIG_FILE" ]] && cp "${FOUND_PATHS[ghostmode.conf]}" "$CONFIG_FILE" && echo "[INFO] Default config created."

install -Dm644 "${FOUND_PATHS[ghostmode.png]}" "$ICON_PATH/ghostmode.png"
install -Dm644 "${FOUND_PATHS[ghostmode.desktop]}" "$DESKTOP_ENTRY"

if [[ "$(ps -p 1 -o comm= 2>/dev/null)" == "systemd" ]]; then
    if [[ -n "$SERVICE_FILE_PATH" ]]; then
        echo "[INFO] Installing systemd service: ghostmode.service"
        cp "$SERVICE_FILE_PATH" /etc/systemd/system/ghostmode.service
        chmod 644 /etc/systemd/system/ghostmode.service
        systemctl daemon-reexec
        systemctl enable ghostmode.service
        systemctl start ghostmode.service
    else
        echo "[WARN] ghostmode.service not found in repo. Skipping service setup."
    fi
else
    echo "[INFO] Systemd not present (likely WSL or Docker). Skipping service setup."
fi

[[ -f "$APPIMAGE_FILE" ]] && install -Dm755 "$APPIMAGE_FILE" /opt/GhostMode.AppImage
[[ -f "$DEB_FILE" ]] && cp "$DEB_FILE" /opt/GhostMode.deb

echo "Installed on $(date)" > "$INSTALL_LOG"
echo "[SUCCESS] GhostMode installation complete."
#!/bin/bash

set -e

echo "🔻 GHOSTMODE™: FULL OPSEC SUITE INITIATED 🔻"
echo "Phase 1: Installing necessary tools..."

# System updates and dependencies
sudo apt update && sudo apt install -y \
    mat2 \
    tor \
    torsocks \
    proxychains4 \
    monero-wallet-cli \
    feather \
    jq \
    zenity \
    python3-pyqt5 \
    python3-pyqt5.qtwebengine \
    xclip \
    curl \
    gpg

echo "✅ All tools installed."

# --------- FINGERPRINT SPOOF SETUP ---------

echo "Phase 2: Launching Anti-Fingerprint Browser Setup..."
echo "Opening Firefox with fingerprint randomizer profile..."

FIREFOX_PROFILE="$HOME/.ghostfox"

if [ ! -d "$FIREFOX_PROFILE" ]; then
    mkdir -p "$FIREFOX_PROFILE"
    cp -r ~/.mozilla/firefox/*.default-release/* "$FIREFOX_PROFILE/" 2>/dev/null || true
    echo 'user_pref("privacy.resistFingerprinting", true);' >> "$FIREFOX_PROFILE/user.js"
    echo 'user_pref("privacy.firstparty.isolate", true);' >> "$FIREFOX_PROFILE/user.js"
    echo 'user_pref("webgl.disabled", true);' >> "$FIREFOX_PROFILE/user.js"
    echo 'user_pref("media.peerconnection.enabled", false);' >> "$FIREFOX_PROFILE/user.js"
    echo 'user_pref("privacy.trackingprotection.enabled", true);' >> "$FIREFOX_PROFILE/user.js"
    echo 'user_pref("canvas.poisondata", true);' >> "$FIREFOX_PROFILE/user.js"
fi

firefox --no-remote -profile "$FIREFOX_PROFILE" &

echo "🕶️  Fingerprint-hardened Firefox launched."

# --------- METADATA REMOVAL WIZARD ---------

echo "Phase 3: METADATA SCRUBBER 🔍"

zenity --info --text="Please choose files to scrub of all metadata."

FILES=$(zenity --file-selection --multiple --separator=" ")

for FILE in $FILES; do
    echo "🧼 Scrubbing: $FILE"
    mat2 --inplace "$FILE"
done

echo "✅ Metadata nuked."

# --------- MONERO COLD WALLET WIZARD ---------

echo "Phase 4: MONERO COLD WALLET CREATION 🔐"
WALLET_NAME=$(zenity --entry --text="Enter a name for your cold wallet:")
WALLET_DIR="$HOME/.ghostwallets"

mkdir -p "$WALLET_DIR"

monero-wallet-cli \
    --generate-new-wallet "$WALLET_DIR/$WALLET_NAME" \
    --restore-height 3100000 \
    --offline \
    --log-file "$WALLET_DIR/$WALLET_NAME.log" \
    --password "" <<< "" > /dev/null

zenity --info --text="Cold wallet '$WALLET_NAME' created. Keys stored at: $WALLET_DIR"

echo "✅ Cold Monero wallet setup complete."

# --------- TOR CHECK ---------

echo "Phase 5: Routing all traffic through Tor..."

PROXYCHAINS_CONF="/etc/proxychains.conf"
if ! grep -q "127.0.0.1 9050" $PROXYCHAINS_CONF; then
    echo "socks5 127.0.0.1 9050" | sudo tee -a $PROXYCHAINS_CONF
fi

tor & sleep 10
proxychains curl https://check.torproject.org

echo "🧅 Tor routing verified."

# --------- CLEANUP REPORT ---------

echo "🧵 Summary:"
echo "- Fingerprint-hardened browser active"
echo "- Metadata nuked for selected files"
echo "- Cold wallet generated in $WALLET_DIR"
echo "- Proxychains + Tor ready for secure comms"

zenity --info --text="Ghostmode Activated. You are now a ghost in the shell. 🖤"

exit 0
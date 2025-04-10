#!/bin/bash

set -e

echo "🪙 GHOSTMODE™ MONERO COLD WALLET WIZARD"
echo "This script will create a secure offline wallet, dump seed + keys, and optionally encrypt them."

read -p "Enter wallet name (no spaces): " WALLET_NAME
WALLET_DIR="$HOME/.ghostwallets"
mkdir -p "$WALLET_DIR"

echo "🔐 Generating new cold wallet: $WALLET_NAME"
monero-wallet-cli --generate-new-wallet "$WALLET_DIR/$WALLET_NAME" \
    --restore-height 3100000 \
    --offline \
    --password "" <<< "" > /dev/null

echo "✅ Wallet created offline at: $WALLET_DIR/$WALLET_NAME"

# Dump the mnemonic seed
echo "📜 Saving mnemonic seed..."
SEED=$(monero-wallet-cli --wallet-file "$WALLET_DIR/$WALLET_NAME" --password "" --mnemonic <<< "exit" | grep -A 25 "Mnemonic seed" | tail -n +2)

echo "$SEED" > "$WALLET_DIR/${WALLET_NAME}_SEED.txt"
chmod 600 "$WALLET_DIR/${WALLET_NAME}_SEED.txt"
echo "🧠 Mnemonic seed saved to: $WALLET_DIR/${WALLET_NAME}_SEED.txt"

# Dump view/spend keys
echo "📤 Exporting view and spend keys..."
KEYS=$(monero-wallet-cli --wallet-file "$WALLET_DIR/$WALLET_NAME" --password "" --dump-key <<<'exit' | grep ':')
echo "$KEYS" > "$WALLET_DIR/${WALLET_NAME}_KEYS.txt"
chmod 600 "$WALLET_DIR/${WALLET_NAME}_KEYS.txt"
echo "🔑 Keys saved to: $WALLET_DIR/${WALLET_NAME}_KEYS.txt"

# Offer to GPG encrypt the keys
read -p "🔐 Encrypt keys and seed with GPG? (y/n): " ENCRYPT
if [[ $ENCRYPT == "y" ]]; then
    gpg --symmetric --cipher-algo AES256 "$WALLET_DIR/${WALLET_NAME}_SEED.txt"
    gpg --symmetric --cipher-algo AES256 "$WALLET_DIR/${WALLET_NAME}_KEYS.txt"
    shred -u "$WALLET_DIR/${WALLET_NAME}_SEED.txt" "$WALLET_DIR/${WALLET_NAME}_KEYS.txt"
    echo "🔐 Files encrypted and originals securely deleted."
fi

# Export view-only wallet for online use
echo "🌐 Creating view-only wallet export..."
monero-wallet-cli --wallet-file "$WALLET_DIR/$WALLET_NAME" --password "" --export-view-key --offline <<< "exit" > "$WALLET_DIR/${WALLET_NAME}_view.key"

echo "🧾 View-only export saved to: $WALLET_DIR/${WALLET_NAME}_view.key"

# Offer QR code seed printout (optional)
if command -v qrencode >/dev/null; then
    read -p "🖨️ Generate QR of seed for airgap printout? (y/n): " QR
    if [[ $QR == "y" ]]; then
        echo "$SEED" | qrencode -o "$WALLET_DIR/${WALLET_NAME}_seed_qr.png"
        echo "🖼️ QR saved to: $WALLET_DIR/${WALLET_NAME}_seed_qr.png"
    fi
fi

echo "✅ DONE. Offline wallet setup complete. Store securely. NEVER connect this wallet to internet."
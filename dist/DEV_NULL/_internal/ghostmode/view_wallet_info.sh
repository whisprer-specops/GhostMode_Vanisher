#!/bin/bash

WALLET_DIR="$HOME/.ghostwallets"
WALLET=$(zenity --file-selection --title="Select View-Only Wallet" --filename="$WALLET_DIR/")

zenity --info --text="Reading wallet info..."

INFO=$(monero-wallet-cli --wallet-file "$WALLET" --password "" --offline --log-file /dev/null <<< "address\nbalance\nexit")

zenity --text-info --title="View-Only Wallet Info" --width=600 --height=400 --filename=<(echo "$INFO")
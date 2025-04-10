#!/bin/bash
DATA="$1"
OUTPUT="airgap_qr.png"

if [[ -z "$DATA" ]]; then
  echo "Usage: $0 <text-to-encode>"
  exit 1
fi

qrencode -o "$OUTPUT" "$DATA"
echo "✅ QR saved to $OUTPUT — scan with your hot machine"

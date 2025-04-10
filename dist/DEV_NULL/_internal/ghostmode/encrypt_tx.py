#!/usr/bin/env python3
import sys
import subprocess

if len(sys.argv) != 3:
    print("Usage: encrypt_tx.py <txfile> <recipient_key_id>")
    sys.exit(1)

txfile = sys.argv[1]
recipient = sys.argv[2]
outfile = f"{txfile}.gpg"

subprocess.run(["gpg", "--output", outfile, "--encrypt", "--recipient", recipient, txfile])
print(f"✅ Encrypted {txfile} → {outfile}")

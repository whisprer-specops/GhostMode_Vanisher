#!/usr/bin/env python3
import sys
import subprocess

if len(sys.argv) != 2:
    print("Usage: decrypt_tx.py <txfile.gpg>")
    sys.exit(1)

infile = sys.argv[1]
outfile = infile.replace(".gpg", "")

subprocess.run(["gpg", "--output", outfile, "--decrypt", infile])
print(f"✅ Decrypted {infile} → {outfile}")

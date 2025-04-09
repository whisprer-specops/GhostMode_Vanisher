#!/usr/bin/env python3
import subprocess
import getpass
import os
from pathlib import Path

def extract_password(stego_path, stego_passphrase):
    if not Path(stego_path).exists():
        print("❌ Stego image not found:", stego_path)
        return None

    temp_output = "extracted_secret.txt"

    cmd = [
        "steghide", "extract",
        "-sf", stego_path,
        "-xf", temp_output,
        "-p", stego_passphrase
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0 and Path(temp_output).exists():
        with open(temp_output, "r") as f:
            secret = f.read().strip()
        os.remove(temp_output)
        print("✅ Password extracted successfully.")
        return secret
    else:
        print("❌ Steghide error:", result.stderr)
        return None

if __name__ == "__main__":
    print("🫥 GHOSTMODE // StegoDrop Extractor")
    stego = input("📁 Stego image (e.g. ghostdrop.jpg): ").strip()
    stego_pass = getpass.getpass("🔑 Stego passphrase: ")

    result = extract_password(stego, stego_pass)
    if result:
        print("🔐 Extracted password:", result)

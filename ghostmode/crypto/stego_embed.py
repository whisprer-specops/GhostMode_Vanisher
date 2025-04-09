#!/usr/bin/env python3
import subprocess
import os
import getpass
from pathlib import Path

def embed_password(carrier_path, password, output_path, stego_passphrase):
    if not Path(carrier_path).exists():
        print("❌ Carrier image not found:", carrier_path)
        return False

    temp_txt = "secret.txt"
    with open(temp_txt, "w") as f:
        f.write(password)

    cmd = [
        "steghide", "embed",
        "-cf", carrier_path,
        "-ef", temp_txt,
        "-sf", output_path,
        "-p", stego_passphrase,
        "-f"  # overwrite if exists
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    os.remove(temp_txt)

    if result.returncode == 0:
        print("✅ Password embedded successfully in:", output_path)
        return True
    else:
        print("❌ Steghide error:", result.stderr)
        return False

if __name__ == "__main__":
    print("🫥 GHOSTMODE // StegoDrop Embedder")
    carrier = input("🖼️  Carrier image (e.g. image.jpg): ").strip()
    output = input("💾 Output stego image (e.g. ghostdrop.jpg): ").strip()
    password = getpass.getpass("🔐 Unlock password to embed: ")
    stego_pass = getpass.getpass("👻 Stego passphrase: ")

    embed_password(carrier, password, output, stego_pass)

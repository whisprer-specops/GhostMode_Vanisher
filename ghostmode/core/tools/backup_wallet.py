#!/usr/bin/env python3
import os
import zipfile
import getpass
import shutil
from datetime import datetime
import sys

def find_wallet_files(wallet_dir):
    files = []
    for entry in os.listdir(wallet_dir):
        if entry.endswith((".keys", ".address.txt", ".log")):
            files.append(os.path.join(wallet_dir, entry))
    return files

def create_backup(wallet_dir, output_dir, zip_name, password=None):
    zip_path = os.path.join(output_dir, zip_name)
    mode = 'w'
    
    with zipfile.ZipFile(zip_path, mode, zipfile.ZIP_DEFLATED) as zf:
        for f in find_wallet_files(wallet_dir):
            print(f"📦 Adding {f}")
            arcname = os.path.basename(f)
            zf.write(f, arcname)

    if password:
        # Re-encrypt zip if password provided (workaround since zipfile doesn't natively encrypt)
        encrypted_path = zip_path.replace(".zip", "_encrypted.zip")
        shutil.move(zip_path, zip_path + ".tmp")

        try:
            import pyminizip
            files_to_zip = [zip_path + ".tmp"]
            pyminizip.compress_multiple(files_to_zip, [], encrypted_path, password, 5)
            os.remove(zip_path + ".tmp")
            print(f"🔐 Encrypted backup created at {encrypted_path}")
        except ImportError:
            print("[!] pyminizip not installed: cannot encrypt zip file.")
            os.rename(zip_path + ".tmp", zip_path)
            print(f"🗃️  Non-encrypted backup at {zip_path}")
    else:
        print(f"✅ Backup saved at {zip_path}")

def main():
    print("🧠 GhostMode Wallet Backup Utility")
    
    wallet_dir = input("📂 Path to wallet directory: ").strip()
    if not os.path.isdir(wallet_dir):
        print("[!] Invalid wallet directory.")
        sys.exit(1)

    output_dir = input("💾 Where to save the backup? [default: current dir]: ").strip() or "."
    os.makedirs(output_dir, exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"wallet_backup_{now}.zip"

    pw_choice = input("🔐 Encrypt with password? [y/N]: ").strip().lower()
    password = None
    if pw_choice == "y":
        password = getpass.getpass("🔑 Enter password: ")

    create_backup(wallet_dir, output_dir, zip_name, password)

if __name__ == "__main__":
    main()

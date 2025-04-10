#!/usr/bin/env python3
import subprocess
import platform
import os
import sys

def check_onionshare_installed():
    try:
        subprocess.run(["onionshare", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def launch_onionshare_send(filepath):
    print(f"[+] Launching OnionShare in 'send' mode for: {filepath}")
    subprocess.run(["onionshare", "--auto-start", "--copy-only", "--no-open", filepath])

def launch_onionshare_receive():
    print(f"[+] Launching OnionShare in 'receive' mode (dropbox)")
    subprocess.run(["onionshare", "receive"])

def main():
    if not check_onionshare_installed():
        print("[!] OnionShare is not installed.")
        print("    ➤ To install: pip install onionshare-cli")
        return

    if len(sys.argv) == 2 and sys.argv[1] == "receive":
        launch_onionshare_receive()
    elif len(sys.argv) >= 2:
        for f in sys.argv[1:]:
            if os.path.exists(f):
                launch_onionshare_send(f)
            else:
                print(f"[!] File not found: {f}")
    else:
        print("Usage:")
        print("  ➤ Send files:   python3 onionshare_drop.py <file1> [file2 ...]")
        print("  ➤ Receive mode: python3 onionshare_drop.py receive")

if __name__ == "__main__":
    main()

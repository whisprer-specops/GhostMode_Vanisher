#!/usr/bin/env python3
import os
import json
from pathlib import Path

IDENTITY_ROOT = Path.home() / ".ghost_identities"

default_metadata = {
    "name": "Unnamed Identity",
    "purpose": "general",
    "created": "unknown",
    "notes": ""
}

def ensure_metadata(path):
    metadata_file = path / "metadata.json"
    if not metadata_file.exists():
        print(f"➕ Creating metadata.json in {path.name}")
        with open(metadata_file, "w") as f:
            json.dump(default_metadata, f, indent=2)

def ensure_gpg_key(path):
    gpg_file = path / "gpg-key.asc"
    if not gpg_file.exists():
        print(f"➕ Creating empty gpg-key.asc in {path.name}")
        gpg_file.touch()

def ensure_firefox_profile(path):
    profile_path = path / "firefox-profile"
    if not profile_path.exists():
        print(f"➕ Creating empty firefox-profile/ in {path.name}")
        profile_path.mkdir()

def fix_identity(identity_path):
    if not identity_path.is_dir():
        return
    ensure_metadata(identity_path)
    ensure_gpg_key(identity_path)
    ensure_firefox_profile(identity_path)

def main():
    if not IDENTITY_ROOT.exists():
        print("⚠️ No identities found.")
        return

    for identity in IDENTITY_ROOT.iterdir():
        if identity.is_dir():
            print(f"🔍 Checking identity: {identity.name}")
            fix_identity(identity)

    print("\n✅ All identities checked and completed.")

if __name__ == "__main__":
    main()

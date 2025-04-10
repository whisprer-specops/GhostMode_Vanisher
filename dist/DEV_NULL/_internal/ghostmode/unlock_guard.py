#!/usr/bin/env python3
import hashlib
import hmac
import json
import os
import time
from cryptography.fernet import Fernet, hmac, hashlib
from pathlib import Path

# === CONFIG ===
ATTEMPT_LOG = "unlock_attempts.json"
SIG_FILE = ".unlock.sig"
SALT_FILE = ".salt"
KEY_FILE = ".fernet.key"

# Generate or load encryption key
def get_key():
    if not Path(KEY_FILE).exists():
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return Fernet(key)

# Generate or load salt
def get_salt():
    if not Path(SALT_FILE).exists():
        salt = os.urandom(16)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
    else:
        with open(SALT_FILE, "rb") as f:
            salt = f.read()
    return salt

def create_encrypted_signature():
    fernet = get_key()
    salt = get_salt()
    if not Path(ATTEMPT_LOG).exists():
        return False
    with open(ATTEMPT_LOG, "rb") as f:
        data = f.read()
    h = hmac.new(salt, data, hashlib.sha256).hexdigest()
    encrypted = fernet.encrypt(h.encode())
    with open(SIG_FILE, "wb") as f:
        f.write(encrypted)
    return True

def verify_sig(verbose=False):
    try:
        if not Path(SIG_FILE).exists():
            return (False, "❌ .sig file not found.")
        if not Path(SALT_FILE).exists():
            return (False, "❌ .salt file missing.")
        if not Path(KEY_FILE).exists():
            return (False, "❌ .key file missing.")
        if not Path(ATTEMPT_LOG).exists():
            return (False, "❌ unlock_attempts.json missing.")

        fernet = get_key()
        salt = get_salt()
        encrypted = Path(SIG_FILE).read_bytes()

        try:
            expected_hmac = fernet.decrypt(encrypted).decode()
        except Exception:
            return (False, "❌ Fernet decryption failed. Wrong key?")

        actual_hmac = hmac.new(salt, Path(ATTEMPT_LOG).read_bytes(), hashlib.sha256).hexdigest()

        if not hmac.compare_digest(expected_hmac, actual_hmac):
            return (False, "❌ HMAC mismatch — file tampering detected.")

        return (True, "✅ Signature valid and verified.")
    except Exception as e:
        return (False, f"❌ Exception: {e}")

# === DEMO: Create sig or verify it ===
if __name__ == "__main__":
    if not Path(ATTEMPT_LOG).exists():
        print("❌ No log found.")
    elif not Path(SIG_FILE).exists():
        print("🔐 Creating encrypted sig...")
        if create_encrypted_signature():
            print("✅ Signature created.")
    else:
        print("🕵️ Verifying...")
        if verify_encrypted_signature():
            print("✅ Integrity confirmed.")
        else:
            print("🚨 TAMPER DETECTED.")

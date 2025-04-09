#!/usr/bin/env python3
import subprocess
import getpass
import os
import json
import time
import requests
import hmac
import hashlib
import smtplib
from email.message import EmailMessage
from cryptography.fernet import Fernet
from ghost_audit import log_event
from pathlib import Path

# === CONFIG ===
ARCHIVE = "ghostmode.7z"
OUTPUT_DIR = "unpacked"
ATTEMPT_LOG = "unlock_attempts.json"
SIG_FILE = ".unlock.sig"
SALT_FILE = ".salt"
KEY_FILE = ".fernet.key"
MAX_ATTEMPTS = 5
LOCKOUT_TIME = 600
EMAIL_NOTIFY = "you@example.com"
SMTP_SERVER = "localhost"
SMTP_PORT = 25
SERVER_URL = "http://localhost:5000/unlock"
API_KEY = "your-shared-secret"
PROFILE_PATH = "unlock_profile.json"
STEGO_IMG = "ghostdrop.jpg"
STEGO_TOOL = "steghide"
AUTO_WIPE_ARCHIVE = True  # 💣 Self-destruct the archive after successful decrypt
SHRED_LOGS_ON_SUCCESS = True

# === V2 UTILS ===
def get_key():
    if not Path(KEY_FILE).exists():
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return Fernet(key)

def get_salt():
    if not Path(SALT_FILE).exists():
        salt = os.urandom(16)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
    else:
        with open(SALT_FILE, "rb") as f:
            salt = f.read()
    return salt

def create_sig():
    fernet = get_key()
    salt = get_salt()
    with open(ATTEMPT_LOG, "rb") as f:
        data = f.read()
    h = hmac.new(salt, data, hashlib.sha256).hexdigest()
    encrypted = fernet.encrypt(h.encode())
    with open(SIG_FILE, "wb") as f:
        f.write(encrypted)

def verify_sig():
    if not all(Path(p).exists() for p in [SIG_FILE, SALT_FILE, KEY_FILE, ATTEMPT_LOG]):
        return False
    fernet = get_key()
    salt = get_salt()
    try:
        with open(SIG_FILE, "rb") as f:
            expected_hmac = fernet.decrypt(f.read()).decode()
        with open(ATTEMPT_LOG, "rb") as logf:
            actual_hmac = hmac.new(salt, logf.read(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected_hmac, actual_hmac)
    except:
        return False

def tamper_check():
    if not verify_sig():
        send_email("🚨 GhostUnlock Tamper Alert", "unlock_attempts.json was tampered with.")
        log_event("tamper_detected", "system")
        print("🛑 TAMPER DETECTED! Refusing to run.")
        exit(1)

def send_email(subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "ghostunlocker@localhost"
    msg["To"] = EMAIL_NOTIFY
    msg.set_content(body)
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as s:
            s.send_message(msg)
    except Exception as e:
        print("📭 Email failed:", e)

def load_log():
    if Path(ATTEMPT_LOG).exists():
        with open(ATTEMPT_LOG) as f:
            return json.load(f)
    return {"fails": 0, "last_fail": 0}

def save_log(log):
    with open(ATTEMPT_LOG, "w") as f:
        json.dump(log, f)
    create_sig()

def mark_attempt(success, user_id="unknown"):
    log = load_log()
    if success:
        log["fails"] = 0
        log_event("unlock_success", user_id)
    else:
        log["fails"] += 1
        log["last_fail"] = time.time()
        log_event("unlock_failed", user_id)
    save_log(log)

    def request_server_key(user_id, token=None):
        headers = {"X-API-Key": API_KEY}
        data = {"user_id": user_id}
        if token:
            data["token"] = token
        r = requests.post(SERVER_URL, json=data, headers=headers)
sif r.ok:
    result = r.json()
    ip = result.get("last_ip", "unknown")
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(result.get("last_access", 0)))
    user = profile.get("user_id", "unknown")

    subprocess.Popen(["zenity", "--info", "--title=Unlock Complete",
        f"--text=✅ {user} unlocked at {ts} from IP {ip}"])

def load_profile():
    return json.load(open(PROFILE_PATH)) if Path(PROFILE_PATH).exists() else {}

def save_profile(user_id, token):
    with open(PROFILE_PATH, "w") as f:
        json.dump({"user_id": user_id, "token": token}, f)

def stego_extract(stego_path, stego_passphrase):
    temp_output = "extracted_secret.txt"
    cmd = [STEGO_TOOL, "extract", "-sf", stego_path, "-xf", temp_output, "-p", stego_passphrase]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0 and Path(temp_output).exists():
        secret = open(temp_output).read().strip()
        os.remove(temp_output)
        return secret
    return None

def main():
    tamper_check()
    if not Path(ARCHIVE).exists():
        print(f"❌ Archive not found: {ARCHIVE}")
        return

    log = load_log()
    if log["fails"] >= MAX_ATTEMPTS and time.time() - log["last_fail"] < LOCKOUT_TIME:
        print("🚫 Too many failed attempts. Try again later.")
        return

    choice = input("🔐 Unlock via [L]ocal, [S]erver, or [T]Stego? ").strip().lower()
    password = None
    user_id = "unknown"

    if choice == "s":
        profile = load_profile()
        user_id = profile.get("user_id") or input("👤 Enter user ID: ").strip()
        token = profile.get("token") or input("🔑 Enter your unlock token: ").strip()
        save_profile(user_id, token)
        password = request_server_key(user_id, token or None)
    elif choice == "t":
        stego_pass = getpass.getpass("👻 Enter Stego passphrase: ")
        password = stego_extract(STEGO_IMG, stego_pass)
    else:
        password = getpass.getpass("🔐 Enter unlock password: ")

    if not password:
        print("❌ Password retrieval failed.")
        mark_attempt(False, user_id)
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    result = subprocess.run(["7z", "x", "-y", f"-p{password}", f"-o{OUTPUT_DIR}", ARCHIVE],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    #!/bin/bash

    SIGCHECK_RESULT=$(python3 -c '
    from unlock_guard_v2 import verify_sig
    print("✅ Signature Verified" if verify_sig() else "❌ Signature Check Failed")
    ')

    zenity --info \
      --title="Unlock Signature Check" \
      --text="$SIGCHECK_RESULT"

    if result.returncode == 0:
        print("✅ Archive decrypted successfully.")
        mark_attempt(True, user_id)
        send_email("✅ GhostUnlock Success", f"Unlocked at {time.ctime()}")
        if AUTO_WIPE_ARCHIVE and Path(ARCHIVE).exists():
            os.remove(ARCHIVE)
            print("💣 Archive wiped.")
    else:
        print("❌ Incorrect password.")
        mark_attempt(False, user_id)

    if SHRED_LOGS_ON_SUCCESS:
        for f in [ATTEMPT_LOG, SIG_FILE, SALT_FILE, KEY_FILE, PROFILE_PATH]:
            if Path(f).exists():
                subprocess.run(["shred", "-u", f])
        print("🧨 Logs securely shredded.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import requests
import subprocess
import tempfile
import os
import base64

SERVER_URL = "http://localhost:5051"  # GPG auth endpoint
GPG_ID = "your-gpg-key-id"            # e.g. email or fingerprint
USER_ID = "admin001"                  # GhostAdmin user ID

def request_challenge(user_id):
    r = requests.post(f"{SERVER_URL}/auth/challenge", json={"user_id": user_id})
    return r.json().get("challenge")

def sign_with_gpg(data):
    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write(data)
        f.flush()
        sig_file = f.name + ".asc"
        cmd = ["gpg", "--default-key", GPG_ID, "--armor", "--output", sig_file, "--sign", f.name]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print("GPG signing failed:", result.stderr.decode())
            return None
        with open(sig_file, "r") as sig:
            return sig.read()

def verify_response(user_id, signature):
    r = requests.post(f"{SERVER_URL}/auth/verify", json={
        "user_id": user_id,
        "signature": signature
    })
    return r.json()

if __name__ == "__main__":
    print(f"Requesting challenge for {USER_ID}...")
    challenge = request_challenge(USER_ID)
    if not challenge:
        print("❌ Failed to obtain challenge.")
        exit(1)

    print("🔐 Signing challenge...")
    signature = sign_with_gpg(challenge)
    if not signature:
        print("❌ GPG signing failed.")
        exit(1)

    print("📨 Verifying with server...")
    result = verify_response(USER_ID, signature)
    print("✅ Result:", result)

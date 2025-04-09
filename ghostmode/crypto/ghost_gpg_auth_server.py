#!/usr/bin/env python3
from flask import Flask, request, jsonify
import os, random, string, tempfile, subprocess, shutil
from tinydb import TinyDB, Query
import time

app = Flask(__name__)
CHALLENGES = {}
KEYS_DIR = "trusted_keys"
os.makedirs(KEYS_DIR, exist_ok=True)

db = TinyDB("users.json")
User = Query()

def generate_challenge(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route("/auth/challenge", methods=["POST"])
def get_challenge():
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400
    challenge = generate_challenge()
    CHALLENGES[user_id] = challenge
    return jsonify({"challenge": challenge})

@app.route("/auth/verify", methods=["POST"])
def verify_signature():
    data = request.json
    user_id = data.get("user_id")
    signature = data.get("signature")

    if not user_id or not signature:
        return jsonify({"error": "Missing data"}), 400
    challenge = CHALLENGES.get(user_id)
    if not challenge:
        return jsonify({"error": "No challenge issued"}), 403

    # Save sig and challenge to temp files
    with tempfile.TemporaryDirectory() as tmpdir:
        sig_file = os.path.join(tmpdir, "sig.asc")
        msg_file = os.path.join(tmpdir, "msg.txt")
        with open(sig_file, "w") as f:
            f.write(signature)
        with open(msg_file, "w") as f:
            f.write(challenge)

        # Loop through all known keys in trusted_keys/
        for pubkey_file in os.listdir(KEYS_DIR):
            key_path = os.path.join(KEYS_DIR, pubkey_file)
            gpg_home = os.path.join(tmpdir, "gnupg")
            os.makedirs(gpg_home, exist_ok=True)
            subprocess.run(["gpg", "--homedir", gpg_home, "--import", key_path],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            result = subprocess.run(["gpg", "--homedir", gpg_home, "--verify", sig_file, msg_file],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                del CHALLENGES[user_id]
                return jsonify({"status": "verified", "fingerprint": pubkey_file})

    return jsonify({"status": "failed", "reason": "Signature could not be verified"}), 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5051)

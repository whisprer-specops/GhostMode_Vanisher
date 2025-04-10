#!/usr/bin/env python3
import sys
import requests
import subprocess
import tempfile
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QFormLayout, QDialog, QMessageBox
)
from cryptography.fernet import Fernet
from ghost_audit import log_event
from admin_dashboard_gui_secure import AdminClient, CONFIG_FILE, load_encrypted_config

SERVER_URL = "http://localhost:5051"

class GPGLoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔐 GPG Admin Login")
        self.user_id_input = QLineEdit()
        self.gpg_id_input = QLineEdit()
        layout = QFormLayout()
        layout.addRow("GhostAdmin User ID:", self.user_id_input)
        layout.addRow("GPG Key ID (email/fingerprint):", self.gpg_id_input)
        self.setLayout(layout)

    def get_credentials(self):
        return self.user_id_input.text().strip(), self.gpg_id_input.text().strip()

def get_challenge(user_id):
    try:
        r = requests.post(f"{SERVER_URL}/auth/challenge", json={"user_id": user_id})
        return r.json().get("challenge")
    except Exception as e:
        return None

def sign_challenge(gpg_id, challenge):
    try:
        with tempfile.NamedTemporaryFile("w", delete=False) as msgfile:
            msgfile.write(challenge)
            msgfile.flush()
            sig_file = msgfile.name + ".asc"
            subprocess.run([
                "gpg", "--default-key", gpg_id,
                "--armor", "--output", sig_file, "--sign", msgfile.name
            ], check=True)
            with open(sig_file, "r") as f:
                return f.read()
    except Exception:
        return None

def verify_signature(user_id, signature):
    try:
        r = requests.post(f"{SERVER_URL}/auth/verify", json={"user_id": user_id, "signature": signature})
        return r.status_code == 200 and r.json().get("status") == "verified"
    except Exception:
        return False

class PassphraseDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔑 Config Decryption")
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        layout = QFormLayout()
        layout.addRow("Config Passphrase:", self.pass_input)
        self.setLayout(layout)

    def get_passphrase(self):
        return self.pass_input.text().strip()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    gpg_dlg = GPGLoginDialog()
    if not gpg_dlg.exec_():
        sys.exit(0)

    user_id, gpg_id = gpg_dlg.get_credentials()
    log_event("admin_login_attempt", user_id)
    challenge = get_challenge(user_id)
    if not challenge:
        QMessageBox.critical(None, "Failed", "Could not get challenge.")
        sys.exit(1)

    signature = sign_challenge(gpg_id, challenge)
    if not signature:
        QMessageBox.critical(None, "Failed", "Failed to sign challenge.")
        sys.exit(1)

    if not verify_signature(user_id, signature):
    log_event("admin_login_failed", user_id)
        QMessageBox.critical(None, "Failed", "GPG Signature invalid.")
        sys.exit(1)

    log_event("admin_login_success", user_id)

    # Now unlock encrypted config
    pass_dlg = PassphraseDialog()
    if not pass_dlg.exec_():
        sys.exit(1)
    passphrase = pass_dlg.get_passphrase()
    config = load_encrypted_config(passphrase)

    if config:
        win = AdminClient(config)
        win.show()
        sys.exit(app.exec_())
    else:
        QMessageBox.critical(None, "Failed", "Failed to decrypt config.")
        sys.exit(1)

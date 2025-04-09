#!/usr/bin/env python3
import sys
import requests
import subprocess
import tempfile
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QInputDialog,
    QMessageBox, QLineEdit, QDialog, QFormLayout
)

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

class GhostLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GhostMode Admin Login")
        self.layout = QVBoxLayout()

        self.info = QLabel("Click to login with GPG.")
        self.layout.addWidget(self.info)

        self.login_btn = QPushButton("🔑 GPG Login")
        self.login_btn.clicked.connect(self.attempt_login)
        self.layout.addWidget(self.login_btn)

        self.setLayout(self.layout)

    def attempt_login(self):
        dlg = GPGLoginDialog()
        if dlg.exec_():
            user_id, gpg_id = dlg.get_credentials()
            self.info.setText("🕵️ Requesting challenge...")
            QApplication.processEvents()
            challenge = get_challenge(user_id)
            if not challenge:
                QMessageBox.critical(self, "Error", "Failed to get challenge.")
                return

            self.info.setText("✍️ Signing...")
            QApplication.processEvents()
            signature = sign_challenge(gpg_id, challenge)
            if not signature:
                QMessageBox.critical(self, "Error", "Failed to sign challenge.")
                return

            self.info.setText("📡 Verifying...")
            QApplication.processEvents()
            if verify_signature(user_id, signature):
                QMessageBox.information(self, "Access Granted", "✅ Verified.")
                self.close()
            else:
                QMessageBox.critical(self, "Access Denied", "❌ Signature invalid.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = GhostLogin()
    win.show()
    sys.exit(app.exec_())

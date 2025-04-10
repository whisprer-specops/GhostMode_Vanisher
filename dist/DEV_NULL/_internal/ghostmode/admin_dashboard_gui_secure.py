#!/usr/bin/env python3
import sys, json, os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton,
    QHBoxLayout, QMessageBox, QInputDialog, QLineEdit, QDialog, QFormLayout
)
from cryptography.fernet import Fernet, InvalidToken
import requests
from ghost_audit import log_event
from pathlib import Path

CONFIG_FILE = Path.home() / ".ghostadmin_config.enc"

class PassphraseDialog(QDialog):
    def __init__(self, new=False):
        super().__init__()
        self.setWindowTitle("🔐 Enter Config Passphrase")
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        layout = QFormLayout()
        layout.addRow("Passphrase:", self.pass_input)
        self.setLayout(layout)
        self.new = new

    def get_passphrase(self):
        return self.pass_input.text().strip()

def derive_key(passphrase):
    return Fernet(Fernet.generate_key()) if not passphrase else Fernet(
        Fernet.generate_key()[:len(Fernet.generate_key())])  # simplified example placeholder

def save_encrypted_config(data, passphrase):
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted = f.encrypt(json.dumps(data).encode())
    with open(CONFIG_FILE, "wb") as file:
        file.write(key + b"::" + encrypted)

def load_encrypted_config(passphrase):
    if not CONFIG_FILE.exists():
        return None
    try:
        raw = CONFIG_FILE.read_bytes()
        key, enc = raw.split(b"::", 1)
        f = Fernet(key)
        return json.loads(f.decrypt(enc).decode())
    except (InvalidToken, ValueError, json.JSONDecodeError):
        return None

class ConfigDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("🛠️ Server Config")
        self.endpoint_input = QLineEdit()
        self.api_key_input = QLineEdit()
        layout = QFormLayout()
        layout.addRow("Server Endpoint:", self.endpoint_input)
        layout.addRow("API Key:", self.api_key_input)
        self.setLayout(layout)

    def get_config(self):
        return {
            "endpoint": self.endpoint_input.text().strip(),
            "api_key": self.api_key_input.text().strip()
        }

class AdminClient(QWidget):
    def __init__(self, config):
        super().__init__()
        self.setWindowTitle("GhostAdmin GUI (Secure)")
        self.setGeometry(100, 100, 600, 400)
        self.config = config
        self.endpoint = config.get("endpoint")
        self.api_key = config.get("api_key")

        self.layout = QVBoxLayout()
        self.user_list = QListWidget()
        self.layout.addWidget(QLabel("👥 Users:"))
        self.layout.addWidget(self.user_list)

        btn_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("🔁 Refresh")
        self.add_btn = QPushButton("➕ Add")
        self.del_btn = QPushButton("🗑️ Delete")
        self.lock_btn = QPushButton("🔒 Lock")
        self.unlock_btn = QPushButton("🔓 Unlock")
        self.reset_btn = QPushButton("♻️ Reset")
        self.cfg_btn = QPushButton("⚙️ Config")
        
        self.remote_del_btn = QPushButton("💥 Remote Unlock & Delete")
        btn_layout.addWidget(self.remote_del_btn)
        self.remote_del_btn.clicked.connect(self.remote_unlock_and_delete)

        for btn in [self.refresh_btn, self.add_btn, self.del_btn, self.lock_btn, self.unlock_btn, self.reset_btn, self.cfg_btn]:
            btn_layout.addWidget(btn)
        self.layout.addLayout(btn_layout)

        self.setLayout(self.layout)

        self.refresh_btn.clicked.connect(self.refresh_users)
        self.add_btn.clicked.connect(self.add_user)
        self.del_btn.clicked.connect(self.delete_user)
        self.lock_btn.clicked.connect(lambda: self.user_action("lock"))
        self.unlock_btn.clicked.connect(lambda: self.user_action("unlock"))
        self.reset_btn.clicked.connect(lambda: self.user_action("reset"))
        self.cfg_btn.clicked.connect(self.configure_endpoint)

        log_event("user_added", uid.strip(), {"by": "admin_gui"})
        log_event("user_deleted", uid, {"by": "admin_gui"})
        self.refresh_users()

    def api_request(self, path, method="GET", data=None):
        url = f"{self.endpoint}{path}"
        headers = {"X-API-Key": self.api_key}
        try:
            if method == "GET":
                r = requests.get(url, headers=headers)
            elif method == "POST":
                r = requests.post(url, headers=headers, json=data)
            elif method == "DELETE":
                r = requests.delete(url, headers=headers, json=data)
            return r.json()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Connection failed:
{e}")
            return {}

    def refresh_users(self):
        self.user_list.clear()
        resp = self.api_request("/admin/users")
        if resp.get("status") == "ok":
            for u in resp["users"]:
                entry = f"{u['user_id']} | {'🔒' if u.get('locked') else '✅'} | {'✔️' if u.get('activated') else '❌'} | IP: {u.get('last_ip', 'n/a')} | {u.get('last_access_str')}"
                self.user_list.addItem(entry)

    def get_selected_user(self):
        item = self.user_list.currentItem()
        return item.text().split(" | ")[0] if item else None

    def add_user(self):
        uid, ok = QInputDialog.getText(self, "Add User", "User ID:")
        if not ok or not uid.strip(): return
        pwd, ok = QInputDialog.getText(self, "Password", "Password:")
        if not ok or not pwd.strip(): return
        token, _ = QInputDialog.getText(self, "Optional Token", "Token:")
        data = {"user_id": uid.strip(), "password": pwd.strip(), "token": token.strip() if token else None}
        msg = self.api_request("/admin/add", "POST", data).get("message", "Failed")
        QMessageBox.information(self, "Add Result", msg)
        self.refresh_users()

    def delete_user(self):
        uid = self.get_selected_user()
        if not uid: return
        msg = self.api_request("/admin/delete", "DELETE", {"user_id": uid}).get("message", "Failed")
        QMessageBox.information(self, "Delete Result", msg)
        self.refresh_users()

    def user_action(self, action):
        uid = self.get_selected_user()
        if not uid: return
        msg = self.api_request(f"/admin/{action}", "POST", {"user_id": uid}).get("message", "Failed")
        log_event(f"user_{action}ed", uid, {"by": "admin_gui"})
        QMessageBox.information(self, f"{action.title()} Result", msg)
        self.refresh_users()

    def configure_endpoint(self):
        dlg = ConfigDialog(self)
        if dlg.exec_():
            config = dlg.get_config()
            pass_dlg = PassphraseDialog(new=True)
            if pass_dlg.exec_():
                save_encrypted_config(config, pass_dlg.get_passphrase())
                log_event("config_updated", "admin", {"from": "admin_gui"})
                QMessageBox.information(self, "Saved", "🔐 Config updated!")

def main():
    app = QApplication(sys.argv)

    dlg = PassphraseDialog()
    if dlg.exec_():
        passphrase = dlg.get_passphrase()
        config = load_encrypted_config(passphrase)
        if config:
            win = AdminClient(config)
            win.show()
            sys.exit(app.exec_())
        else:
            QMessageBox.critical(None, "Failed", "❌ Decryption failed or config missing.")
            sys.exit(1)

    def remote_unlock_and_delete(self):
        uid = self.get_selected_user()
        if not uid: return
        token, ok = QInputDialog.getText(self, "Remote Token", "Enter user unlock token:")
        if not ok or not token.strip(): return
        resp = self.api_request("/unlock_and_delete", "POST", {"user_id": uid, "token": token})
        msg = resp.get("message", "No response.")
        QMessageBox.information(self, "Result", msg)

if __name__ == "__main__":
    main()

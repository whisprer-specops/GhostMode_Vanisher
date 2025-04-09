#!/usr/bin/env python3
import sys
import requests
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton,
    QHBoxLayout, QMessageBox, QInputDialog, QLineEdit, QDialog, QFormLayout
)

API_KEY = "your-shared-secret"
DEFAULT_ENDPOINT = "http://localhost:5050"

class ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Server Config")
        self.endpoint_input = QLineEdit()
        self.endpoint_input.setText(DEFAULT_ENDPOINT)
        layout = QFormLayout()
        layout.addRow("Server Endpoint:", self.endpoint_input)
        self.setLayout(layout)

    def get_endpoint(self):
        return self.endpoint_input.text().strip()

class AdminClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GhostAdmin Remote Client")
        self.setGeometry(100, 100, 600, 400)
        self.endpoint = DEFAULT_ENDPOINT

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

        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.del_btn)
        btn_layout.addWidget(self.lock_btn)
        btn_layout.addWidget(self.unlock_btn)
        btn_layout.addWidget(self.reset_btn)
        btn_layout.addWidget(self.cfg_btn)
        self.layout.addLayout(btn_layout)

        self.setLayout(self.layout)

        self.refresh_btn.clicked.connect(self.refresh_users)
        self.add_btn.clicked.connect(self.add_user)
        self.del_btn.clicked.connect(self.delete_user)
        self.lock_btn.clicked.connect(lambda: self.user_action("lock"))
        self.unlock_btn.clicked.connect(lambda: self.user_action("unlock"))
        self.reset_btn.clicked.connect(lambda: self.user_action("reset"))
        self.cfg_btn.clicked.connect(self.configure_endpoint)

        self.refresh_users()

    def api_request(self, path, method="GET", data=None):
        url = f"{self.endpoint}{path}"
        headers = {"X-API-Key": API_KEY}
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
        else:
            QMessageBox.warning(self, "Error", "Failed to retrieve user list.")

    def get_selected_user(self):
        item = self.user_list.currentItem()
        if not item:
            QMessageBox.warning(self, "No Selection", "No user selected.")
            return None
        return item.text().split(" | ")[0]

    def add_user(self):
        uid, ok = QInputDialog.getText(self, "Add User", "User ID:")
        if not ok or not uid.strip():
            return
        pwd, ok = QInputDialog.getText(self, "Set Password", "Password:")
        if not ok or not pwd.strip():
            return
        token, _ = QInputDialog.getText(self, "Optional Token", "Token:")
        data = {
            "user_id": uid.strip(),
            "password": pwd.strip(),
            "token": token.strip() if token else None
        }
        resp = self.api_request("/admin/add", "POST", data)
        QMessageBox.information(self, "Result", resp.get("message", "Failed"))
        self.refresh_users()

    def delete_user(self):
        uid = self.get_selected_user()
        if not uid:
            return
        resp = self.api_request("/admin/delete", "DELETE", {"user_id": uid})
        QMessageBox.information(self, "Result", resp.get("message", "Failed"))
        self.refresh_users()

    def user_action(self, action):
        uid = self.get_selected_user()
        if not uid:
            return
        path = f"/admin/{action}"
        resp = self.api_request(path, "POST", {"user_id": uid})
        QMessageBox.information(self, "Result", resp.get("message", "Failed"))
        self.refresh_users()

    def configure_endpoint(self):
        dlg = ConfigDialog()
        if dlg.exec_():
            self.endpoint = dlg.get_endpoint()
            QMessageBox.information(self, "Config Updated", f"New endpoint: {self.endpoint}")
            self.refresh_users()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AdminClient()
    win.show()
    sys.exit(app.exec_())

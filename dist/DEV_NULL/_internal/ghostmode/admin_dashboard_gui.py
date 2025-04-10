#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit,
    QHBoxLayout, QMessageBox, QListWidget, QInputDialog
)
from tinydb import TinyDB, Query
import time

db = TinyDB("users.json")
User = Query()

class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GhostAdmin Panel")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.user_list = QListWidget()
        self.refresh_users()
        self.layout.addWidget(QLabel("👤 Users:"))
        self.layout.addWidget(self.user_list)

        # Buttons
        btn_layout = QHBoxLayout()
        self.view_btn = QPushButton("🔁 Refresh")
        self.delete_btn = QPushButton("🗑️ Delete")
        self.lock_btn = QPushButton("🔒 Lock")
        self.unlock_btn = QPushButton("🔓 Unlock")
        self.reset_btn = QPushButton("♻️ Reset")
        self.add_btn = QPushButton("➕ Add")

        btn_layout.addWidget(self.view_btn)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.lock_btn)
        btn_layout.addWidget(self.unlock_btn)
        btn_layout.addWidget(self.reset_btn)

        self.layout.addLayout(btn_layout)

        self.setLayout(self.layout)

        # Connect buttons
        self.view_btn.clicked.connect(self.refresh_users)
        self.delete_btn.clicked.connect(self.delete_user)
        self.lock_btn.clicked.connect(lambda: self.toggle_lock(True))
        self.unlock_btn.clicked.connect(lambda: self.toggle_lock(False))
        self.reset_btn.clicked.connect(self.reset_user)
        self.add_btn.clicked.connect(self.add_user)

    def refresh_users(self):
        self.user_list.clear()
        users = db.all()
        for u in users:
            line = f"{u['user_id']} | {'🔒' if u.get('locked') else '✅'} | {'✔️' if u.get('activated') else '❌'} | IP: {u.get('last_ip', 'n/a')} | {time.ctime(u['last_access']) if u.get('last_access') else 'Never'}"
            self.user_list.addItem(line)

    def get_selected_user(self):
        item = self.user_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Error", "No user selected.")
            return None
        return item.text().split(" | ")[0]

    def delete_user(self):
        uid = self.get_selected_user()
        if uid and db.remove(User.user_id == uid):
            QMessageBox.information(self, "Success", f"Deleted {uid}")
            self.refresh_users()

    def toggle_lock(self, lock):
        uid = self.get_selected_user()
        if uid and db.update({"locked": lock}, User.user_id == uid):
            QMessageBox.information(self, "Success", f"{'Locked' if lock else 'Unlocked'} {uid}")
            self.refresh_users()

    def reset_user(self):
        uid = self.get_selected_user()
        if uid and db.update({"activated": False, "locked": False, "last_ip": None, "last_access": None}, User.user_id == uid):
            QMessageBox.information(self, "Success", f"Reset {uid}")
            self.refresh_users()

    def add_user(self):
        uid, ok = QInputDialog.getText(self, "Add User", "Enter new user ID:")
        if not ok or not uid.strip():
            return
        if db.contains(User.user_id == uid):
            QMessageBox.warning(self, "Error", "User already exists.")
            return
        pwd, ok = QInputDialog.getText(self, "Add Password", "Enter password:")
        if not ok or not pwd.strip():
            return
        token, _ = QInputDialog.getText(self, "Optional Token", "Enter unlock token (optional):")
        record = {
            "user_id": uid.strip(),
            "password": pwd.strip(),
            "token": token.strip() if token else None,
            "locked": False,
            "activated": False,
            "last_ip": None,
            "last_access": None
        }
        db.insert(record)
        QMessageBox.information(self, "User Created", f"User '{uid}' added.")
        self.refresh_users()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    panel = AdminPanel()
    panel.show()
    sys.exit(app.exec_())

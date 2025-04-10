#!/usr/bin/env python3
import os
import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class GhostControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GhostMode Control Panel")

        layout = QVBoxLayout()

        layout.addWidget(self.make_button("Backup Wallet", self.backup_wallet))
        layout.addWidget(self.make_button("View Wallet Info", self.view_wallet_info))
        layout.addWidget(self.make_button("Stylometry Obfuscator", self.stylometry_obfuscator))
        layout.addWidget(self.make_button("OnionShare Drop", self.onionshare_drop))

        self.setLayout(layout)

    def make_button(self, label, callback):
        btn = QPushButton(label)
        btn.clicked.connect(callback)
        return btn

    def get_script_path(self, name):
        base = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base, "..", "scripts", name)

    def launch_script(self, script):
        fullpath = self.get_script_path(script)
        if os.path.exists(fullpath):
            subprocess.Popen(["python", fullpath], shell=True)
        else:
            print(f"[ERROR] Script not found: {fullpath}")

    def backup_wallet(self):
        self.launch_script("backup_wallet.py")

    def view_wallet_info(self):
        self.launch_script("view_wallet_info.py")

    def stylometry_obfuscator(self):
        self.launch_script("stylometry_obfuscator.py")

    def onionshare_drop(self):
        self.launch_script("onionshare_drop.py")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    panel = GhostControlPanel()
    panel.show()
    sys.exit(app.exec_())

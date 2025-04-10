#!/usr/bin/env python3
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer

class GhostSystray:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.tray = QSystemTrayIcon()
        self.menu = QMenu()

        self.icon_path = QIcon.fromTheme("security-high")
        self.tray.setIcon(self.icon_path)
        self.tray.setVisible(True)

        self.add_actions()
        self.tray.setContextMenu(self.menu)

    def add_actions(self):
        splash_action = QAction("Show Splash")
        splash_action.triggered.connect(lambda: os.system("python3 ~/ghostmode/tools/gui/ghostmode_splash.py &"))
        self.menu.addAction(splash_action)

        identity_switch = QAction("Switch Identity")
        identity_switch.triggered.connect(lambda: os.system("python3 ~/ghostmode/identity/identity_switcher_gui.py &"))
        self.menu.addAction(identity_switch)

        generate_key = QAction("Generate Temp GPG Key")
        generate_key.triggered.connect(lambda: os.system("bash ~/ghostmode/tools/crypto/generate_temp_key.sh &"))
        self.menu.addAction(generate_key)

        fix_identities = QAction("Fix Identities")
        fix_identities.triggered.connect(lambda: os.system("bash ~/ghostmode/identity/tools/ghost_fix_identities.sh &"))
        self.menu.addAction(fix_identities)

        qr_unlock = QAction("Show Unlock QR")
        qr_unlock.triggered.connect(lambda: os.system("bash ~/ghostmode/tools/qr/qr_export_token.sh PLACEHOLDER_TOKEN &"))
        self.menu.addAction(qr_unlock)

        audit_upload = QAction("Upload Audit Logs")
        audit_upload.triggered.connect(lambda: os.system("bash ~/ghostmode/tools/logging/upload_encrypted_log.sh &"))
        self.menu.addAction(audit_upload)

        stealth_exit = QAction("🔒 Stealth Exit")
        stealth_exit.triggered.connect(self.confirm_exit)
        self.menu.addAction(stealth_exit)

    def confirm_exit(self):
        reply = QMessageBox.question(
            None, "Confirm Exit",
            "Wipe & close GhostMode?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            os.system("bash ~/ghostmode/timers/ghost_idlewatch.sh --force-wipe &")
            self.tray.hide()
            sys.exit()

    def run(self):
        self.app.exec_()

if __name__ == "__main__":
    tray = GhostSystray()
    tray.run()

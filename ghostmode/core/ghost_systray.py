#!/usr/bin/env python3
import sys
import os
import configparser
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox,subprocess
from PyQt5.QtGui import QIcon
import subprocess

CONFIG_PATH = os.path.expanduser("~/.config/ghostmode/ghostmode.conf")

fix_identities_action = QAction("🧹 Scan & Fix Identities")
fix_identities_action.triggered.connect(lambda: subprocess.Popen(["ghost_fix_identities_gui.sh"]))

tray_menu.addAction(fix_identities_action)

class GhostTrayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        self.config = self.load_config()

        # Load icon
        icon = QIcon.fromTheme("ghostmode", QIcon("ghostmode.png"))
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(icon)

        # Menu
        self.menu = QMenu()
        self.add_actions()

        if not self.config.getboolean("General", "stealth_mode", fallback=False):
            self.tray.setVisible(True)
            self.tray.setContextMenu(self.menu)

    def add_actions(self):
        launch_action = QAction("🧠 Open GhostControl")
        launch_action.triggered.connect(self.launch_control)
        self.menu.addAction(launch_action)

        usb_check_action = QAction("🔌 Check USB")
        usb_check_action.triggered.connect(self.check_usb)
        self.menu.addAction(usb_check_action)

        exit_action = QAction("❌ Exit")
        exit_action.triggered.connect(self.exit_app)
        self.menu.addAction(exit_action)

    gen_temp_action = QAction("🔐 Generate Temp GPG Key")
    gen_temp_action.triggered.connect(lambda: subprocess.Popen(["/usr/local/bin/tools/generate_temp_key.sh"]))

    menu = QMenu()

    start_service_action = QAction("Start GhostMode Service")
    stop_service_action = QAction("Stop GhostMode Service")

    start_service_action.triggered.connect(lambda: subprocess.run(["sc", "start", "GhostModeService"]))
    stop_service_action.triggered.connect(lambda: subprocess.run(["sc", "stop", "GhostModeService"]))

menu.addAction(start_service_action)
menu.addAction(stop_service_action)




    tray_menu.addAction(gen_temp_action)

    def load_config(self):
        config = configparser.ConfigParser()
        default_config = {
            "General": {
                "stealth_mode": "false",
                "control_command": "ghostcontrol.py"
            }
        }

        if not os.path.exists(CONFIG_PATH):
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            config.read_dict(default_config)
            with open(CONFIG_PATH, "w") as configfile:
                config.write(configfile)
        else:
            config.read(CONFIG_PATH)

        return config

    def launch_control(self):
        cmd = self.config.get("General", "control_command", fallback="ghostcontrol.py")
        subprocess.Popen([cmd])

    def check_usb(self):
        try:
            out = subprocess.check_output("lsblk -o MOUNTPOINT -nr | grep -E '^/media|^/mnt' | head -n1", shell=True)
            mount = out.decode().strip()
            if mount:
                QMessageBox.information(None, "USB Detected", f"USB Mounted at: {mount}")
            else:
                QMessageBox.warning(None, "No USB", "No USB drive mounted.")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Could not check USB:\n{e}")

    def exit_app(self):
        self.tray.setVisible(False)
        self.app.quit()

        def run(self):
            self.app.exec_()

    switch_id_action = QAction("🎭 Switch Identity")
    switch_id_action.triggered.connect(lambda: subprocess.Popen(["identity_switcher_gui.py"]))
    tray_menu.addAction(switch_id_action)

if __name__ == "__main__":
    ghost = GhostTrayApp()
    ghost.run()

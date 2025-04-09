import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QFileDialog
)
import sys
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QMessageBox
import subprocess
import sys

class GhostPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GhostMode 🔐 Transaction Manager")
        layout = QVBoxLayout()

        self.export_btn = QPushButton("Export + Encrypt TX (cold)")
        self.broadcast_btn = QPushButton("Decrypt + Broadcast TX (hot)")

        self.export_btn.clicked.connect(self.export_tx)
        self.broadcast_btn.clicked.connect(self.broadcast_tx)

        layout.addWidget(self.export_btn)
        layout.addWidget(self.broadcast_btn)
        self.setLayout(layout)

    def export_tx(self):
        wallet, _ = QFileDialog.getOpenFileName(self, "Select Cold Wallet")
        if not wallet: return
        label, _ = QFileDialog.getSaveFileName(self, "Save TX As")
        if not label: return
        recipient, _ = QFileDialog.getOpenFileName(self, "Select Recipient GPG Key (asc)")
        if not recipient: return

        subprocess.run(["monero-wallet-cli", "--wallet-file", wallet, "--export-transfers", "all", label])
        subprocess.run(["gpg", "--import", recipient])
        subprocess.run(["python3", "usr/bin/encrypt_tx.py", label, "ghostrecipient"])

        QMessageBox.information(self, "Exported", f"Encrypted TX saved to {label}.gpg")

    def broadcast_tx(self):
        txfile, _ = QFileDialog.getOpenFileName(self, "Select TX File (.gpg)")
        if not txfile: return
        view_wallet, _ = QFileDialog.getOpenFileName(self, "Select View-Only Wallet")
        if not view_wallet: return

        subprocess.run(["python3", "usr/bin/decrypt_tx.py", txfile])
        plain_tx = txfile.replace(".gpg", "")
        subprocess.run(["monero-wallet-cli", "--wallet-file", view_wallet, "--broadcast-tx", plain_tx])

        QMessageBox.information(self, "Broadcasted", f"Transaction {plain_tx} was broadcast.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GhostPanel()
    window.show()
    sys.exit(app.exec_())

class GhostControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("👻 GHOSTMODE™ Control Panel")
        self.setGeometry(500, 300, 400, 400)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("🎛️ All Ops Modules – Click To Activate"))

        buttons = {
            "📡 MAC Address Randomizer": self.randomize_mac,
            "🧼 Metadata Nuker": self.nuke_metadata,
            "🔐 GPG Encrypt/Sign Tool": self.launch_gpg_gui,
            "🧅 OnionShare Dropzone": self.onionshare_upload,
            "🪙 Monero Cold Wallet Wizard": self.monero_coldwallet,
            "🎭 Identity Rotation Manager": self.identity_manager,
            "🧠 AI Stylometry Jammer": self.stylometry_jammer,
            "🧾 View Wallet Info": self.view_wallet_info,
            "💽 Backup Wallet to USB": self.backup_wallet,
            "✍️ Sign TX (Cold)": self.sign_tx,
            "📡 Broadcast TX (Hot)": self.broadcast_tx,
            "🎭 Identity Rotation Manager": self.identity_manager,
            "⏱️ Identity Timer Auto-Rotator": self.identity_timer,
            "💣 Enable Self-Wipe After Inactivity": self.enable_idle_wipe,
        }

        for label, method in buttons.items():
            btn = QPushButton(label)
            btn.clicked.connect(method)
            layout.addWidget(btn)

        self.setLayout(layout)

    def export_tx():
        wallet_file, _ = QFileDialog.getOpenFileName(None, "Select Cold Wallet")
        output_file, _ = QFileDialog.getSaveFileName(None, "Save TX to USB")
        subprocess.run([
            "monero-wallet-cli",
            "--wallet-file", wallet_file,
            "--export-transfers", "all",
            output_file
        ])
        QMessageBox.information(None, "Export", "TX exported successfully.")

    def broadcast_tx():
        wallet_file, _ = QFileDialog.getOpenFileName(None, "Select View-Only Wallet")
        tx_file, _ = QFileDialog.getOpenFileName(None, "Select TX File")
        subprocess.run([
            "monero-wallet-cli",
            "--wallet-file", wallet_file,
            "--broadcast-tx", tx_file
        ])
        QMessageBox.information(None, "Broadcast", "TX broadcasted.")

    def randomize_mac(self):
        iface = "wlan0"  # Change to your interface
        subprocess.call(f"sudo ifconfig {iface} down", shell=True)
        subprocess.call(f"sudo macchanger -r {iface}", shell=True)
        subprocess.call(f"sudo ifconfig {iface} up", shell=True)
        mac = subprocess.check_output(f"macchanger -s {iface}", shell=True).decode()
        QMessageBox.information(self, "MAC Changed", mac)

    def nuke_metadata(self):
        subprocess.call('bash -c "zenity --file-selection --multiple --separator=\\\" \\\" | xargs -d \\\" \\\" -I{{}} mat2 --inplace {{}}"', shell=True)

    def launch_gpg_gui(self):
        subprocess.Popen(["bash", "gpg_gui.sh"])

    def onionshare_upload(self):
        subprocess.Popen(["bash", "-c", "FILE=$(zenity --file-selection --multiple); onionshare-cli --public $FILE"])

    def monero_coldwallet(self):
        subprocess.Popen(["bash", "monero_cold_wallet_wizard.sh"])
    
    def identity_manager(self):
        subprocess.Popen(["bash", "identikit.sh"])

    def stylometry_jammer(self):
        subprocess.Popen(["bash", "stylometry_obfuscator.sh"])

    def view_wallet_info(self):
        subprocess.Popen(["bash", "view_wallet_info.sh"])

    def backup_wallet(self):
        subprocess.Popen(["bash", "coldwallet_backup_to_usb.sh"])

    def sign_tx(self):
        subprocess.Popen(["bash", "cold_sign_tx.sh"])

    def broadcast_tx(self):
        subprocess.Popen(["bash", "hot_broadcast_tx.sh"])

    def identity_manager(self):
    subprocess.Popen(["bash", "identikit.sh"])

    def identity_timer(self):
    subprocess.Popen(["bash", "identity_timer.sh"])

    def enable_idle_wipe(self):
    from PyQt5.QtWidgets import QInputDialog

    timeout, ok = QInputDialog.getInt(
        self,
        "Idle Timeout",
        "Enter inactivity timeout in minutes:",
        min=1,
        max=720
    )

    if ok:
        subprocess.Popen([
            "bash", "ghost_idlewatch.sh", str(timeout)
        ])

    def is_online():
    try:
        socket.gethostbyname("getmonero.org")
        return True
    except:
        return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ghost = GhostControlPanel()
    ghost.show()
    sys.exit(app.exec_())

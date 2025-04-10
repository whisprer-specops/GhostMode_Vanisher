import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
)
import sys
import os
import subprocess
import ctypes

class GhostControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("👻 GHOSTMODE™ Control Panel")
        self.setGeometry(500, 300, 400, 400)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("🎛️ All Ops Modules – Click To Activate"))

        buttons = {
            "🧬 Identity Generator": self.generate_identity,
            "🌀 Identity Switcher GUI": self.identity_switcher,
#            "📋 Admin Dashboard (Local)": self.admin_dashboard,
            "🌐 Admin Dashboard (Remote)": self.admin_dashboard_remote,
            "🔐 GPG Login Prompt": self.gpg_login,
            "📤 Upload Audit Log": self.upload_audit_log,
            "🧠 Stylometry Obfuscator": self.launch_stylometry_tool,
            "📡 Show Unlock QR Code": self.show_qr_code,
            "📡 MAC Address Randomizer": self.randomize_mac,
            "🧼 Metadata Nuker": self.nuke_metadata,
            "🔐 GPG Encrypt/Sign Tool": self.launch_gpg_gui,
            "🧅 OnionShare Dropzone": self.onionshare_upload,
            "🪙 Monero Cold Wallet Wizard": self.monero_coldwallet,
            "🎭 Identity Rotation Manager": self.identity_manager,
            "🧠 AI Stylometry Jammer": self.stylometry_jammer
        }

        for label, method in buttons.items():
            btn = QPushButton(label)
            btn.clicked.connect(method)
            layout.addWidget(btn)

        self.setLayout(layout)

    def generate_identity(self):
        subprocess.Popen(["python3", os.path.expanduser("~/ghostmode/identity/generate_identity.py")])

    def identity_switcher(self):
        subprocess.Popen(["python3", os.path.expanduser("~/ghostmode/identity/identity_switcher_gui.py")])

    def admin_dashboard(self):
        subprocess.Popen(["python3", os.path.expanduser("~/ghostmode/admin/admin_dashboard_gui.py")])

    def admin_dashboard_remote(self):
        subprocess.Popen(["python3", os.path.expanduser("~/ghostmode/admin/admin_dashboard_gui_remote.py")])

    def gpg_login(self):
        subprocess.Popen(["python3", os.path.expanduser("~/ghostmode/tools/auth/ghost_gpg_login_gui.py")])

    def upload_audit_log(self):
        subprocess.Popen(["bash", os.path.expanduser("~/ghostmode/tools/logging/upload_encrypted_log.sh")])

    def launch_stylometry_tool(self):
        subprocess.Popen(["bash", os.path.expanduser("~/ghostmode/tools/stylometry/stylometry_obfuscator.sh")])

    def show_qr_code(self):
        token = "PLACEHOLDER_TOKEN"  # TODO: inject real token
        subprocess.Popen(["bash", os.path.expanduser("~/ghostmode/tools/qr/qr_export_token.sh"), token])

    def stylometry_jammer(self):
        subprocess.Popen(["bash", "stylometry_obfuscator.sh"])

    def randomize_mac(self):
        iface = "wlan0"  # Adjust as needed
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

#    def install_service_if_needed():
#        service_name = "GhostModeService"
#        try:
#            # Check if service exists
#            result = subprocess.run(["sc", "query", service_name], capture_output=True, text=True)
#            if "FAILED" in result.stdout or "does not exist" in result.stdout:
#                # Trigger bat installer silently
#                script_path = os.path.join(os.path.dirname(__file__), "..", "tools", "wind", "install_with_service.bat")
#                abs_path = os.path.abspath(script_path)
#
#                # Run as admin silently
#                ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", f'/c "{abs_path}"', None, 0)
#        except Exception as e:
#            print(f"[WARN] Could not check/install service: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ghost = GhostControlPanel()
    ghost.show()
    sys.exit(app.exec_())

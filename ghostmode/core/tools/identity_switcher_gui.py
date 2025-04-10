#!/usr/bin/env python3
import sys, os, json
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QTextEdit, QMessageBox

IDENTITY_ROOT = Path.home() / ".ghost_identities"
ACTIVE_SYMLINK = Path.home() / ".ghostmode" / "active_identity"

class IdentitySwitcher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧑‍🎤 Ghost Identity Switcher")
        self.resize(400, 300)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.combo = QComboBox()
        self.combo.currentIndexChanged.connect(self.preview_identity)
        self.layout.addWidget(QLabel("Choose an identity:"))
        self.layout.addWidget(self.combo)

        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.layout.addWidget(self.preview)

        self.activate_btn = QPushButton("🔗 Activate This Identity")
        self.activate_btn.clicked.connect(self.activate_identity)
        self.layout.addWidget(self.activate_btn)

        self.load_identities()

    def load_identities(self):
        if not IDENTITY_ROOT.exists():
            QMessageBox.critical(self, "Error", f"Identity folder missing: {IDENTITY_ROOT}")
            self.close()
        self.identities = sorted([p for p in IDENTITY_ROOT.iterdir() if p.is_dir()])
        self.combo.addItems([p.name for p in self.identities])
        self.preview_identity(0)

    def preview_identity(self, index):
        try:
            meta = self.identities[index] / "metadata.json"
            if meta.exists():
                data = json.loads(meta.read_text())
                self.preview.setText(json.dumps(data, indent=2))
            else:
                self.preview.setText("⚠️ metadata.json not found.")
        except Exception as e:
            self.preview.setText(f"❌ Error reading identity: {e}")

    def activate_identity(self):
        selected = self.identities[self.combo.currentIndex()]
        ACTIVE_SYMLINK.parent.mkdir(parents=True, exist_ok=True)
        if ACTIVE_SYMLINK.exists() or ACTIVE_SYMLINK.is_symlink():
            ACTIVE_SYMLINK.unlink()
        os.symlink(selected, ACTIVE_SYMLINK)

        # ⟳ Repoint config
        conf = selected / "ghostmode.conf"
        if conf.exists():
            CONFIG_SYMLINK.unlink(missing_ok=True)
            CONFIG_SYMLINK.symlink_to(conf)

        QMessageBox.information(self, "Activated", f"🔗 Identity '{selected.name}' is now active!\nConfig reloaded.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = IdentitySwitcher()
    win.show()
    sys.exit(app.exec_())

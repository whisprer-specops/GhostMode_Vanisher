#!/usr/bin/env python3
import os, json
from pathlib import Path
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QTextEdit, QMessageBox

IDENTITY_ROOT = Path.home() / ".ghost_identities"

class IdentityPreviewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("👁️ Preview Identity")
        self.resize(500, 350)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Select identity:"))
        self.combo = QComboBox()
        self.combo.currentIndexChanged.connect(self.load_preview)
        layout.addWidget(self.combo)

        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        layout.addWidget(self.preview)

        self.load_identities()

    def load_identities(self):
        self.identities = sorted([p for p in IDENTITY_ROOT.iterdir() if p.is_dir()])
        self.combo.addItems([p.name for p in self.identities])
        if self.identities:
            self.load_preview(0)

    def load_preview(self, index):
        if index >= len(self.identities):
            return
        identity = self.identities[index]
        preview_lines = []

        # metadata.json
        meta_file = identity / "metadata.json"
        if meta_file.exists():
            try:
                meta = json.loads(meta_file.read_text())
                preview_lines.append("Name: " + meta.get("name", ""))
                preview_lines.append("Purpose: " + meta.get("purpose", ""))
                preview_lines.append("Created: " + meta.get("created", ""))
            except:
                preview_lines.append("⚠️ Error reading metadata.json")
        else:
            preview_lines.append("⚠️ No metadata.json found.")

        # gpg-key.asc
        gpg_file = identity / "gpg-key.asc"
        if gpg_file.exists():
            result = os.popen(f"gpg --with-fingerprint {gpg_file}").read()
            preview_lines.append("🔐 GPG Fingerprint:\n" + result)
        else:
            preview_lines.append("🔐 No GPG key found.")

        # folder stats
        total_size = sum(f.stat().st_size for f in identity.rglob("*") if f.is_file())
        preview_lines.append(f"📦 Size: {round(total_size / 1024 / 1024, 2)} MB")

        last_mod = datetime.fromtimestamp(identity.stat().st_mtime)
        preview_lines.append("🕒 Last Modified: " + last_mod.strftime("%Y-%m-%d %H:%M:%S"))

        self.preview.setText("\n".join(preview_lines))

if __name__ == "__main__":
    app = QApplication([])
    win = IdentityPreviewer()
    win.show()
    app.exec_()

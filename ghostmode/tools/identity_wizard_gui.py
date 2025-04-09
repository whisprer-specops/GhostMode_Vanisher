#!/usr/bin/env python3
import os, json, subprocess
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QCheckBox, QPushButton, QMessageBox

IDENTITY_ROOT = Path.home() / ".ghost_identities"

class IdentityWizard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("➕ Create New Ghost Identity")
        self.resize(400, 350)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Identity Name:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Purpose / Notes:"))
        self.notes_input = QTextEdit()
        layout.addWidget(self.notes_input)

        self.gpg_checkbox = QCheckBox("Generate new GPG key")
        layout.addWidget(self.gpg_checkbox)

        self.create_btn = QPushButton("Create Identity")
        self.create_btn.clicked.connect(self.create_identity)
        layout.addWidget(self.create_btn)

    def create_identity(self):
        name = self.name_input.text().strip()
        notes = self.notes_input.toPlainText().strip()

        if not name:
            QMessageBox.warning(self, "Missing", "Please enter an identity name.")
            return

        identity_path = IDENTITY_ROOT / name
        if identity_path.exists():
            QMessageBox.warning(self, "Exists", f"Identity '{name}' already exists.")
            return

        identity_path.mkdir(parents=True)
        (identity_path / "firefox-profile").mkdir()

        metadata = {
            "name": name,
            "purpose": notes,
            "created": str(Path().absolute()),
        }

        with open(identity_path / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        if self.gpg_checkbox.isChecked():
            email = f"{name}@ghost.id"
            subprocess.run(["gpg", "--quick-generate-key", f"{name} <{email}>", "default", "default", "1y"])
            result = subprocess.run(["gpg", "--armor", "--export", email], capture_output=True, text=True)
            if result.returncode == 0:
                with open(identity_path / "gpg-key.asc", "w") as f:
                    f.write(result.stdout)

        QMessageBox.information(self, "Done", f"🎭 Identity '{name}' created successfully!")
        self.close()

if __name__ == "__main__":
    app = QApplication([])
    win = IdentityWizard()
    win.show()
    app.exec_()

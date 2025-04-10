#!/usr/bin/env python3
import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox

TOGGLE_FILE = os.path.expanduser("~/.ghostmode_disposable")

class GhostDropToggler(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GhostDrop™ Mode Toggle")

        layout = QVBoxLayout()

        self.status_label = QLabel(self.status_text())
        layout.addWidget(self.status_label)

        self.toggle_btn = QPushButton("Toggle GhostDrop Mode")
        self.toggle_btn.clicked.connect(self.toggle)
        layout.addWidget(self.toggle_btn)

        self.setLayout(layout)

    def status_text(self):
        return "GhostDrop is ENABLED" if os.path.exists(TOGGLE_FILE) else "GhostDrop is DISABLED"

    def toggle(self):
        if os.path.exists(TOGGLE_FILE):
            os.remove(TOGGLE_FILE)
        else:
            with open(TOGGLE_FILE, "w") as f:
                f.write("DISPOSABLE MODE ENABLED\n")

        self.status_label.setText(self.status_text())
        QMessageBox.information(self, "GhostDrop™", self.status_text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = GhostDropToggler()
    win.show()
    sys.exit(app.exec_())

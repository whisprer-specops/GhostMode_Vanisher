#!/usr/bin/env python3
import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit,
    QFileDialog, QMessageBox
)

LOG_DIR = os.path.expanduser("~/.ghostmode/logs")

class LogViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GhostMode Log Viewer")

        layout = QVBoxLayout()

        self.view_button = QPushButton("Open a Log File")
        self.view_button.clicked.connect(self.open_log)
        layout.addWidget(self.view_button)

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)

        self.setLayout(layout)

    def open_log(self):
        if not os.path.exists(LOG_DIR):
            QMessageBox.warning(self, "No Logs", "Log directory not found.")
            return

        filename, _ = QFileDialog.getOpenFileName(self, "Select a Log File", LOG_DIR, "Log Files (*.log *.txt)")
        if filename:
            try:
                with open(filename, "r") as f:
                    self.text_area.setPlainText(f.read())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = LogViewer()
    viewer.show()
    sys.exit(app.exec_())

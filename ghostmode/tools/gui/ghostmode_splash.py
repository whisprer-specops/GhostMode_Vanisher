#!/usr/bin/env python3
import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        # Load splash image
        splash_path = os.path.expanduser("assets/splash.png")
        pixmap = QPixmap(splash_path)
        if pixmap.isNull():
            label = QLabel("Missing splash image")
            label.setStyleSheet("color: red; font-size: 16pt;")
            layout.addWidget(label)
        else:
            image_label = QLabel()
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(image_label)

        version_label = QLabel("GhostMode v1.2.0")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setFont(QFont("Arial", 12))
        version_label.setStyleSheet("color: white;")
        layout.addWidget(version_label)

        self.setLayout(layout)
        self.resize(pixmap.width() + 20, pixmap.height() + 60)
        self.center()

    def center(self):
        frame_geometry = self.frameGeometry()
        center_point = QApplication.desktop().screenGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    app.exec_()

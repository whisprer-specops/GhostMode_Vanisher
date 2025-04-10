#!/usr/bin/env python3
import os
import sys
import shutil
import tempfile
import urllib.request
import zipfile
from PyQt5.QtWidgets import QApplication, QMessageBox

# CHANGE THIS TO YOUR REAL REPO FILE PATH
UPDATE_URL = "https://your-domain.com/ghostmode/DEV_NULL-latest.zip"

def self_update():
    app = QApplication(sys.argv)

    temp_dir = tempfile.mkdtemp()
    update_file = os.path.join(temp_dir, "update.zip")

    try:
        urllib.request.urlretrieve(UPDATE_URL, update_file)
    except Exception as e:
        QMessageBox.critical(None, "Update Failed", f"Could not download update:\n{e}")
        return

    try:
        with zipfile.ZipFile(update_file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
    except Exception as e:
        QMessageBox.critical(None, "Update Failed", f"Could not extract update:\n{e}")
        return

    try:
        current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                src = os.path.join(root, file)
                rel_path = os.path.relpath(src, temp_dir)
                dst = os.path.join(current_dir, rel_path)

                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)

        QMessageBox.information(None, "Update Complete", "GhostMode has been updated. Please restart it now.")
    except Exception as e:
        QMessageBox.critical(None, "Update Error", f"Update failed during copy:\n{e}")
    finally:
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    self_update()

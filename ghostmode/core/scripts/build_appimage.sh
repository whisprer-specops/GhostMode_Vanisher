appimage_script = """#!/bin/bash
APPDIR=GhostMode.AppDir
BIN_DIR="$APPDIR/usr/bin"

mkdir -p "$BIN_DIR" "$APPDIR/usr/share/applications" "$APPDIR/usr/share/icons/hicolor/256x256/apps"

cp /usr/local/bin/ghostadmin_launcher.py "$BIN_DIR/ghostadmin_launcher"
cp /usr/local/bin/ghost_unlocker.py "$BIN_DIR/ghost_unlocker"
cp /usr/local/bin/ghostcontrol.py "$BIN_DIR/ghostcontrol"
cp /usr/local/bin/tools/* "$BIN_DIR/"

cp /usr/share/applications/ghostmode.desktop "$APPDIR/usr/share/applications/"
cp /usr/share/icons/hicolor/256x256/apps/ghostmode.png "$APPDIR/usr/share/icons/hicolor/256x256/apps/"

echo -e "[Desktop Entry]\\nName=GhostMode\\nExec=ghostadmin_launcher\\nIcon=ghostmode\\nType=Application" > "$APPDIR/AppRun"
chmod +x "$APPDIR/AppRun"

ARCH=x86_64 appimagetool "$APPDIR" GhostMode-1.0-x86_64.AppImage
"""
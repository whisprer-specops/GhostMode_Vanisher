deb_script = """#!/bin/bash
DEBROOT=GhostMode_1.0
mkdir -p "$DEBROOT/DEBIAN" "$DEBROOT/usr/local/bin" "$DEBROOT/usr/share/applications" "$DEBROOT/usr/share/icons/hicolor/256x256/apps"

cp /usr/local/bin/ghostadmin_launcher.py "$DEBROOT/usr/local/bin/"
cp /usr/local/bin/ghost_unlocker.py "$DEBROOT/usr/local/bin/"
cp /usr/local/bin/ghostcontrol.py "$DEBROOT/usr/local/bin/"
cp /usr/local/bin/tools/* "$DEBROOT/usr/local/bin/"

cp /usr/share/applications/ghostmode.desktop "$DEBROOT/usr/share/applications/"
cp /usr/share/icons/hicolor/256x256/apps/ghostmode.png "$DEBROOT/usr/share/icons/hicolor/256x256/apps/"

cat <<EOF > "$DEBROOT/DEBIAN/control"
Package: ghostmode
Version: 1.0
Architecture: all
Maintainer: GhostPetey
Description: GhostMode - Secure Transaction & Identity Toolkit
EOF

dpkg-deb --build "$DEBROOT"
mv GhostMode_1.0.deb GhostMode_1.0_all.deb
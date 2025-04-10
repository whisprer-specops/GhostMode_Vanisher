@echo off
REM Launch OnionShare Drop (Windows/Tor)

echo [*] Launching OnionShare Dropzone...
onionshare-cli.exe --receive --public --no-autostart
pause

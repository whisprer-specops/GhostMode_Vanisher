@echo off
REM Strip metadata from files using ExifTool (Windows version)

set TARGET_DIR=%1
if "%TARGET_DIR%"=="" set TARGET_DIR=.

echo [*] Nuking metadata in %TARGET_DIR%...
for %%F in (%TARGET_DIR%\*.jpg %TARGET_DIR%\*.png %TARGET_DIR%\*.mp4) do (
    exiftool -all= "%%F"
)
echo [+] Done nuking metadata.
pause

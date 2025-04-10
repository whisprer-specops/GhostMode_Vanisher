:: tools/install_ghostmode_service.bat
@echo off
set SERVICE_NAME=GhostModeService
set APP_PATH=%~dp0..\dist\DEV_NULL.exe

echo Installing GhostMode as a Windows service...
nssm install %SERVICE_NAME% "%APP_PATH%"

echo Start the service with:
echo     nssm start %SERVICE_NAME%
echo To remove the service later:
echo     nssm remove %SERVICE_NAME%
pause

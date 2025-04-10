:: ghostmode/tools/windows/uninstall_ghostmode_service.bat

@echo off
set SERVICE_NAME=GhostModeService
set NSSM_PATH=%~dp0nssm.exe

echo [INFO] Stopping and removing GhostMode service...
"%NSSM_PATH%" stop %SERVICE_NAME%
"%NSSM_PATH%" remove %SERVICE_NAME% confirm
pause

@echo off
set "NSSM_PATH=%~dp0nssm.exe"
set "SERVICE_NAME=GhostModeService"
set "APP_PATH=%~dp0..\..\dist\DEV_NULL.exe"
set "WORK_DIR=%~dp0..\..\dist"
set "LOG_PATH=%WORK_DIR%\ghostmode_service.log"

echo [INFO] Installing GhostMode service...
"%NSSM_PATH%" install %SERVICE_NAME% "%APP_PATH%"
"%NSSM_PATH%" set %SERVICE_NAME% AppDirectory "%WORK_DIR%"
"%NSSM_PATH%" set %SERVICE_NAME% AppStdout "%LOG_PATH%"
"%NSSM_PATH%" set %SERVICE_NAME% AppStderr "%LOG_PATH%"
"%NSSM_PATH%" set %SERVICE_NAME% AppExit Default Restart

echo [INFO] Starting GhostMode service...
"%NSSM_PATH%" start %SERVICE_NAME%

echo [SUCCESS] DEV NULL service installed & running in background.
pause

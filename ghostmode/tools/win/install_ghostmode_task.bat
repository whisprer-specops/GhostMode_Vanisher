@echo off
:: ----------------------------------------------------------------------
:: GhostMode Autostart Task Installer (Windows Task Scheduler)
:: Adds a task that runs GhostMode on user login.
:: ----------------------------------------------------------------------

set "TASKNAME=GhostMode AutoStart"
set "EXENAME=DEV_NULL.exe"
set "EXEPATH=%~dp0..\..\dist\%EXENAME%"

echo.
echo [GhostMode Task Installer]
echo --------------------------
echo Task Name : %TASKNAME%
echo Target EXE: %EXEPATH%
echo.

if not exist "%EXEPATH%" (
    echo [ERROR] Cannot find executable: %EXEPATH%
    echo Make sure you have built DEV_NULL.exe in the /dist folder.
    pause
    exit /b 1
)

echo Registering GhostMode as a startup task...
schtasks /create ^
  /tn "GhostMode AutoStart" ^
  /tr "\"C:\Path\To\DEV_NULL.exe\"" ^
  /sc onstart ^
  /ru SYSTEM ^
  /rl HIGHEST ^
  /f


if %ERRORLEVEL% equ 0 (
    echo [SUCCESS] Task "%TASKNAME%" registered.
) else (
    echo [FAILURE] Task creation failed.
)

echo.
pause
exit /b

:: tools/install_ghostmode_task.bat
@echo off
set TASKNAME=GhostMode AutoStart
set EXEPATH=%~dp0..\dist\DEV_NULL.exe

echo Registering GhostMode with Task Scheduler...
schtasks /create /tn "%TASKNAME%" /tr "\"%EXEPATH%\"" /sc onlogon /rl HIGHEST /f

echo Done. You can manage this task in Task Scheduler UI.
pause

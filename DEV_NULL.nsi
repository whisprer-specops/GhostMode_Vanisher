!define APPNAME "DEV_NULL"
!define VERSION "1.0"
!define COMPANY "GhostMode Labs"
!define INSTALLDIR "$PROGRAMFILES\${APPNAME}"
!define EXENAME "DEV_NULL.exe"

SetCompressor /SOLID lzma

Name "${APPNAME}"
OutFile "DEV_NULL_Installer.exe"
InstallDir "${INSTALLDIR}"
InstallDirRegKey HKCU "Software\${APPNAME}" "Install_Dir"
RequestExecutionLevel admin
ShowInstDetails show
ShowUninstDetails show

Page directory
Page instfiles
UninstPage uninstConfirm
UninstPage instfiles

Section "Install"
  SetOutPath "$INSTDIR"
  
  ; Main app
  File "dist\${EXENAME}"
  
  ; Launcher BATs
  File "bat_launchers\launch_devnull.bat"
  File "bat_launchers\launch_systray.bat"
  File "bat_launchers\launch_tools.bat"
  File "bat_launchers\launch_unlocker.bat"
  
  ; Icons and splash if wanted
  ; File "ghostmode\assets\splash.png"
  ; File "ghostmode\share\icons\ghostmode_256x256.ico"

  ; Add Start Menu shortcuts
  CreateDirectory "$SMPROGRAMS\${APPNAME}"
  CreateShortCut "$SMPROGRAMS\${APPNAME}\Launch DEV_NULL.lnk" "$INSTDIR\launch_devnull.bat"
  CreateShortCut "$SMPROGRAMS\${APPNAME}\Systray UI.lnk" "$INSTDIR\launch_systray.bat"
  CreateShortCut "$SMPROGRAMS\${APPNAME}\Tools Panel.lnk" "$INSTDIR\launch_tools.bat"
  CreateShortCut "$SMPROGRAMS\${APPNAME}\Unlocker.lnk" "$INSTDIR\launch_unlocker.bat"
  CreateShortCut "$SMPROGRAMS\${APPNAME}\Uninstall ${APPNAME}.lnk" "$INSTDIR\Uninstall.exe"

  ; Write uninstall data
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  WriteRegStr HKCU "Software\${APPNAME}" "Install_Dir" "$INSTDIR"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\${EXENAME}"
  Delete "$INSTDIR\launch_*.bat"
  Delete "$INSTDIR\Uninstall.exe"

  Delete "$SMPROGRAMS\${APPNAME}\*.*"
  RMDir "$SMPROGRAMS\${APPNAME}"
  RMDir "$INSTDIR"
  DeleteRegKey HKCU "Software\${APPNAME}"
SectionEnd

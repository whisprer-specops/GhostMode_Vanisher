; DEV_NULL.nsi — NSIS installer script for DEV_NULL

Outfile "DEV_NULL_Installer.exe"
InstallDir "$PROGRAMFILES\DEV_NULL"
RequestExecutionLevel admin
ShowInstDetails hide
ShowUninstDetails hide
SetCompressor /SOLID lzma

!include "MUI2.nsh"

; === SPLASH SCREEN ===
!define MUI_WELCOMEFINISHPAGE_BITMAP "C:\GitHub\GhostMode_Vanisher\ghostmode\assets\splash.png"

; === INSTALLER ICON ===
Icon "C:\GitHub\GhostMode_Vanisher\ghostmode\assets\DEV_NULL.ico"
!define MUI_ICON "C:\GitHub\GhostMode_Vanisher\ghostmode\assets\DEV_NULL.ico"

; === EULA ===
!define MUI_LICENSEPAGE_CHECKBOX
!insertmacro MUI_PAGE_LICENSE "C:\GitHub\GhostMode_Vanisher\ghostmode\assets\EULA.txt"

; === INSTALL PAGES ===
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES

; === UNINSTALL PAGES ===
!insertmacro MUI_UNPAGE_INSTFILES

; === HEADERS ===
!insertmacro MUI_LANGUAGE "English"

Section "Install DEV_NULL" SEC01
  SetOutPath "$INSTDIR"
  File /r "C:\GitHub\GhostMode_Vanisher\ghostmode\dist\DEV_NULL\*.*"
  CreateShortcut "$DESKTOP\DEV_NULL.lnk" "$INSTDIR\DEV_NULL.exe"
  WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Uninstall"
  Delete "$DESKTOP\DEV_NULL.lnk"
  Delete "$INSTDIR\Uninstall.exe"
  RMDir /r "$INSTDIR"
SectionEnd

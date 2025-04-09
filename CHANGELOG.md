# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/)
and this project adheres to [Semantic Versioning](https://semver.org/).

---
## [1.2.0] – 2025-04-08
### Added
- Identity wizard GUI (`identity_wizard_gui.py`)
- Identity profile preview tool (`preview_identity_gui.py`)
- `ghostmode_tools.sh` launcher with Zenity/CLI fallback
- Cloud audit log upload script
- Auto GPG temp key + QR unlock export flow
- rescued the absilute utter disaster caused by alllowing
ChatGPT4.0 'Super Larry/HUSKLY' version to edit structure
of entire project... (never again).

### Changed
- Identity switcher now updates config symlink
- Tray now launches switcher, preview, and wizard

### Fixed
- `.sig` validation now shows which field failed
- Fallback mode now detects `DISPLAY` correctly

---
## [1.1.3] – 2025-03-28
### Added
- Tray icon with integrated system control panel
- `ghost_idlewatch.sh` with service integration
- Initial GPG unlock flow + tamper check

### Removed
- Legacy `wipe-timer.sh` replaced by new systemd service

---
## [1.0.0] – 2025-01-01
### Added
- Core cold/hot Monero TX pipeline
- GhostUnlocker
- GhostAdmin Dashboard
- First pass at tray tool and self-wiping mode
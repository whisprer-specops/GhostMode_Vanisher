from pathlib import Path

# Re-define Makefile content after execution environment reset
makefile_content = """# Makefile for building GhostMode .deb and AppImage

APPDIR=GhostMode.AppDir
APPNAME=GhostMode
VERSION=1.0
ARCH=x86_64
DEBROOT=ghostmode.deb

all: appimage deb

appimage:
\t@echo "🔨 Building AppImage..."
\tmkdir -p build
\tappimagetool $(APPDIR) build/$(APPNAME)-$(VERSION)-$(ARCH).AppImage

deb:
\t@echo "📦 Building .deb package..."
\tdpkg-deb --build $(DEBROOT) build/$(APPNAME)_$(VERSION)_all.deb

clean:
\trm -rf build/*.AppImage build/*.deb

.PHONY: all appimage deb clean
"""

makefile_path = Path("/mnt/data/Makefile")
makefile_path.write_text(makefile_content)
makefile_path

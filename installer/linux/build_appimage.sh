#!/usr/bin/env bash
# Build PyGrind AppImage from PyInstaller output.
#
# Prerequisites:
#   1. Build with: python scripts/build.py
#   2. Install appimagetool: https://github.com/AppImage/AppImageKit/releases
#      or: wget https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage
#
# Usage:
#   bash installer/linux/build_appimage.sh
#
# Output: dist/PyGrind-x86_64.AppImage

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DIST_DIR="$PROJECT_ROOT/dist"
PYINSTALLER_OUT="$DIST_DIR/pygrind"
APPDIR="$DIST_DIR/PyGrind.AppDir"

# Check prerequisites
if [ ! -d "$PYINSTALLER_OUT" ]; then
    echo "ERROR: PyInstaller output not found at $PYINSTALLER_OUT"
    echo "Run 'python scripts/build.py' first."
    exit 1
fi

if ! command -v appimagetool &>/dev/null; then
    echo "ERROR: appimagetool not found in PATH."
    echo "Download from: https://github.com/AppImage/appimagetool/releases"
    exit 1
fi

echo "Building AppImage..."

# Create AppDir structure
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/share/icons/hicolor/scalable/apps"

# Copy PyInstaller output
cp -r "$PYINSTALLER_OUT"/* "$APPDIR/usr/bin/"

# Copy desktop integration files
cp "$SCRIPT_DIR/pygrind.desktop" "$APPDIR/"
cp "$SCRIPT_DIR/pygrind.svg" "$APPDIR/"
cp "$SCRIPT_DIR/pygrind.svg" "$APPDIR/usr/share/icons/hicolor/scalable/apps/"

# Create AppRun launcher
cat > "$APPDIR/AppRun" << 'APPRUN'
#!/bin/bash
HERE="$(dirname "$(readlink -f "${0}")")"
exec "$HERE/usr/bin/pygrind" "$@"
APPRUN
chmod +x "$APPDIR/AppRun"

# Build the AppImage
ARCH=x86_64 appimagetool "$APPDIR" "$DIST_DIR/PyGrind-x86_64.AppImage"

echo ""
echo "AppImage built: $DIST_DIR/PyGrind-x86_64.AppImage"
echo "To run: chmod +x dist/PyGrind-x86_64.AppImage && ./dist/PyGrind-x86_64.AppImage"

#!/bin/bash
# Build script for Wallpaper Engine executable

set -e

echo "Building Wallpaper Engine executable..."
echo ""

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Navigate to the script directory
cd "$(dirname "$0")"

echo "Running PyInstaller..."
pyinstaller wallpaper_engine.spec

echo ""
echo "Build complete!"
echo "Executable is located in: dist/wallpaper_engine"
echo ""
echo "To run the wallpaper:"
echo "  ./dist/wallpaper_engine"
echo "or for fullscreen:"
echo "  ./dist/wallpaper_engine --fullscreen"

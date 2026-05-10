#!/bin/bash
# Quick start guide for installation and running Wallpaper Engine

set -e

echo "Wallpaper Engine - Installation and Setup"
echo "=========================================="
echo ""

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Step 1: Installing dependencies..."
pip install -e . 2>&1 | tail -5

echo ""
echo "Step 2: Testing installation..."
python -c "import wallpaper_engine; print('✓ Successfully imported wallpaper_engine')"

echo ""
echo "Installation complete!"
echo ""
echo "To run the wallpaper, use:"
echo "  python -m wallpaper_engine"
echo ""
echo "For fullscreen mode:"
echo "  python -m wallpaper_engine --fullscreen"
echo ""
echo "To build a standalone executable:"
echo "  ./build.sh"
echo ""
echo "Then run:"
echo "  ./dist/wallpaper_engine"

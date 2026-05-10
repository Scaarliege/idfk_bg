@echo off
REM Build script for Wallpaper Engine executable (Windows)

echo Building Wallpaper Engine executable...
echo.

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
)

echo Running PyInstaller...
pyinstaller wallpaper_engine.spec

echo.
echo Build complete!
echo Executable is located in: dist\wallpaper_engine.exe
echo.
echo To run the wallpaper:
echo   dist\wallpaper_engine.exe
echo or for fullscreen:
echo   dist\wallpaper_engine.exe --fullscreen

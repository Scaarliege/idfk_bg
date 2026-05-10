# Quick Start Guide for Wallpaper Engine

## Installation

### Option 1: Run with Python directly

```bash
cd wallpaper_engine
pip install -e .
python -m wallpaper_engine
```

### Option 2: Run from source without installation

```bash
cd wallpaper_engine
pip install pygame
python -m wallpaper_engine
```

## Building Standalone Executable

### Linux/macOS

```bash
cd wallpaper_engine
./build.sh
./dist/wallpaper_engine --fullscreen
```

### Windows

```bash
cd wallpaper_engine
build.bat
dist\wallpaper_engine.exe --fullscreen
```

## Usage

**Windowed mode (default):**
```bash
python -m wallpaper_engine
```

**Fullscreen mode:**
```bash
python -m wallpaper_engine --fullscreen
```

**Standalone executable:**
```bash
./dist/wallpaper_engine [--fullscreen]
```

## Controls

- **Click + Drag**: Apply force to nearby particles
- **ESC**: Exit
- **Close Window**: Exit

## Package Structure

```
wallpaper_engine/
├── wallpaper_engine/          # Main package
│   ├── __init__.py
│   ├── __main__.py           # CLI entry point
│   ├── app.py                # Main application
│   ├── particles.py          # Particle system
│   └── effects.py            # Visual effects
├── setup.py                  # Installation configuration
├── wallpaper_engine.spec     # PyInstaller configuration
├── build.sh                  # Build script (Linux/Mac)
├── build.bat                 # Build script (Windows)
├── install.sh                # Installation script
├── README.md                 # Documentation
├── MANIFEST.in               # Package manifest
├── LICENSE                   # MIT License
└── .gitignore                # Git ignore rules
```

## Customization

Edit `wallpaper_engine/app.py` to change:

- Resolution: `WallpaperEngine(width=1920, height=1080)`
- Particle count: `ParticleSystem(..., num_particles=200)`
- Connection radius: `self.particles.connection_radius = 150`
- FPS: `self.fps = 120`
- Motion blur: `self.screen.fill((0, 0, 0, 30))` (increase last number for more blur)
- Noise amount: `add_noise(self.screen, amount=1000, max_alpha=20)`

## System Requirements

- Python 3.8+ (for source mode)
- Pygame 2.1.0+
- ~50MB (for executable)
- Any OS: Windows, macOS, Linux

## Troubleshooting

**ImportError: No module named pygame**
```bash
pip install pygame
```

**Permission denied on build.sh (Linux/Mac)**
```bash
chmod +x build.sh install.sh
./build.sh
```

**PyInstaller not found**
```bash
pip install pyinstaller
./build.sh
```

## Delivery/Distribution

The package can be distributed as:

1. **Source package** - Users run: `pip install wallpaper-engine`
2. **Executable** - Run `build.sh`/`build.bat` to create distributable .exe/.app/.bin
3. **Python wheel** - Build with: `python -m build`

All are ready to use!

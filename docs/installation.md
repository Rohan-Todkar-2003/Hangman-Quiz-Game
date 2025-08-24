# 📦 Installation Guide

## System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.7 or higher
- **RAM**: Minimum 512MB available
- **Storage**: 50MB free space
- **Display**: 1024x768 minimum resolution

## Installation Methods

### Method 1: Automated Setup (Recommended)

The easiest way to get started:

```bash
# Clone the repository
git clone https://github.com/yourusername/hangman-mcq-game.git
cd hangman-mcq-game

# Run automated setup with all features
python setup.py --install --extras video

# Launch the game
python hangman_game.py
```

### Method 2: Virtual Environment (Isolated Installation)

For a clean, isolated installation:

```bash
# Clone the repository
git clone https://github.com/yourusername/hangman-mcq-game.git
cd hangman-mcq-game

# Create virtual environment
python setup.py --venv game-env

# Activate virtual environment
# Windows:
game-env\Scripts\activate
# macOS/Linux:
source game-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch the game
python hangman_game.py
```

### Method 3: Manual Installation

If you prefer manual control:

```bash
# Clone the repository
git clone https://github.com/yourusername/hangman-mcq-game.git
cd hangman-mcq-game

# Install core dependencies
pip install pygame>=2.0.0 numpy>=1.19.0

# Optional: Install video support
pip install opencv-python>=4.5.0 Pillow>=8.0.0

# Launch the game
python hangman_game.py
```

## Platform-Specific Instructions

### Windows

**Prerequisites:**
```cmd
# Ensure Python is in PATH
python --version

# If tkinter missing (rare):
# Download Python from python.org (includes tkinter)
```

**Installation:**
```cmd
git clone https://github.com/yourusername/hangman-mcq-game.git
cd hangman-mcq-game
python setup.py --install --extras video
python hangman_game.py
```

**Using Launch Script:**
```cmd
# Double-click launch_game.bat or run:
scripts\launch_game.bat
```

### macOS

**Prerequisites:**
```bash
# Install Python 3.7+ (if not already installed)
brew install python@3.11

# Verify installation
python3 --version
```

**Installation:**
```bash
git clone https://github.com/yourusername/hangman-mcq-game.git
cd hangman-mcq-game
python3 setup.py --install --extras video
python3 hangman_game.py
```

**Using Launch Script:**
```bash
chmod +x scripts/launch_game.sh
./scripts/launch_game.sh
```

### Linux (Ubuntu/Debian)

**Prerequisites:**
```bash
# Update package list
sudo apt update

# Install Python and tkinter
sudo apt install python3 python3-pip python3-tk python3-venv

# Verify installation
python3 --version
```

**Installation:**
```bash
git clone https://github.com/yourusername/hangman-mcq-game.git
cd hangman-mcq-game
python3 setup.py --install --extras video
python3 hangman_game.py
```

**Using Launch Script:**
```bash
chmod +x scripts/launch_game.sh
./scripts/launch_game.sh
```

## Dependency Details

### Core Dependencies
- **pygame**: Handles sound effects and audio management
- **numpy**: Used for generating fallback beep sounds
- **tkinter**: GUI framework (usually included with Python)

### Optional Dependencies
- **opencv-python**: Enables MP4 video playback for celebrations
- **Pillow**: Image processing for video frame conversion

## Verification

After installation, verify everything works:

```bash
# Test dependencies
python setup.py --install

# Quick dependency check
python -c "import pygame, numpy, tkinter; print('✅ Core dependencies OK')"

# Test optional video support
python -c "import cv2, PIL; print('✅ Video support OK')"
```

## Common Installation Issues

### Issue: "pygame not found"
**Solution:**
```bash
pip install pygame
# If that fails:
pip install --user pygame
```

### Issue: "No module named 'tkinter'"
**Solutions by platform:**
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **CentOS/RHEL**: `sudo yum install tkinter` or `sudo dnf install python3-tkinter`
- **macOS**: Usually included; try `brew install python-tk` if missing
- **Windows**: Usually included; reinstall Python from python.org

### Issue: "Permission denied" during pip install
**Solutions:**
```bash
# Use --user flag
pip install --user pygame numpy

# Or create virtual environment
python -m venv game-env
# Activate and install normally
```

### Issue: Video not playing
**Solution:**
```bash
# Install video support packages
pip install opencv-python Pillow

# If OpenCV fails on Linux:
sudo apt-get install python3-opencv
```

### Issue: "Microsoft Visual C++ required" (Windows)
**Solution:**
- Download and install "Microsoft C++ Build Tools"
- Or install "Visual Studio Community" with C++ tools
- Alternative: Use pre-compiled wheels with `pip install --only-binary=all opencv-python`

## Development Setup

For contributors who want to modify the game:

```bash
# Clone your fork
git clone https://github.com/yourusername/hangman-mcq-game.git
cd hangman-mcq-game

# Create development environment
python setup.py --venv dev-env
source dev-env/bin/activate  # or dev-env\Scripts\activate on Windows

# Install with all features
pip install -r requirements.txt

# Make your changes and test
python hangman_game.py
```

## Uninstallation

To remove the game and dependencies:

```bash
# If using virtual environment (recommended):
rm -rf game-env/  # or delete the folder

# If installed system-wide:
pip uninstall pygame numpy opencv-python Pillow

# Remove game directory
rm -rf hangman-mcq-game/
```

## Next Steps

After successful installation:
1. Read the [Gameplay Guide](gameplay.md) to understand game mechanics
2. Check [Troubleshooting](troubleshooting.md) if you encounter issues
3. Start playing: `python hangman_game.py`

## Getting Help

If you're still having trouble:
1. Check the [troubleshooting guide](troubleshooting.md)
2. Search existing [GitHub issues](../../issues)
3. Create a new issue with:
   - Your operating system and Python version
   - Complete error message
   - Steps you've already tried

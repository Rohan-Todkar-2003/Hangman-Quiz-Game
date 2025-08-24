# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### Installation Problems

#### "pygame not found" or "No module named 'pygame'"
**Cause**: pygame is not installed
**Solutions:**
```bash
# Try standard installation
pip install pygame

# If that fails, try user installation
pip install --user pygame

# For conda users
conda install pygame

# For Ubuntu/Debian users
sudo apt-get install python3-pygame
```

#### "No module named 'tkinter'"
**Cause**: tkinter is not installed (common on Linux)
**Solutions by OS:**

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**CentOS/RHEL/Fedora:**
```bash
# CentOS/RHEL
sudo yum install tkinter
# Fedora
sudo dnf install python3-tkinter
```

**macOS:**
```bash
# Usually included, but if missing:
brew install python-tk
```

**Windows:**
- tkinter is usually included with Python
- Reinstall Python from python.org if missing

#### "Microsoft Visual C++ required" (Windows)
**Cause**: Some packages need C++ build tools
**Solutions:**
```bash
# Option 1: Install pre-compiled wheels
pip install --only-binary=all opencv-python

# Option 2: Install Microsoft C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

#### Permission Denied During Installation
**Solutions:**
```bash
# Use --user flag
pip install --user pygame numpy

# Or create virtual environment
python -m venv game-env
# Windows: game-env\Scripts\activate
# Unix: source game-env/bin/activate
pip install pygame numpy
```

### Runtime Issues

#### Game Window Not Opening
**Possible Causes & Solutions:**

1. **Display Issues:**
   ```bash
   # Check display environment (Linux)
   echo $DISPLAY
   
   # If using SSH, enable X11 forwarding
   ssh -X username@hostname
   ```

2. **Python Path Issues:**
   ```bash
   # Run from correct directory
   cd hangman-mcq-game
   python hangman_game.py
   ```

3. **File Path Issues:**
   - Ensure you're running from the repository root
   - Check that `hangman_game.py` exists in current directory

#### "ModuleNotFoundError: No module named 'cv2'"
**Cause**: OpenCV not installed (video features won't work)
**Solutions:**
```bash
# Install OpenCV
pip install opencv-python

# If installation fails, try:
pip install --user opencv-python

# Alternative: Install without video features
# (Game will work, but no video celebrations)
```

#### No Sound Playing
**Possible Causes & Solutions:**

1. **pygame Audio Issues:**
   ```python
   # Test pygame audio
   python -c "import pygame; pygame.mixer.init(); print('Audio OK')"
   ```

2. **System Audio Issues:**
   - Check system volume levels
   - Close other audio applications
   - Try different audio output device

3. **Missing Sound Files:**
   - Verify sound files exist in `assets/files/sounds/`
   - Game generates beep fallbacks if numpy is available

4. **Linux Audio Issues:**
   ```bash
   # Install audio dependencies
   sudo apt-get install libasound2-dev
   
   # For PulseAudio
   sudo apt-get install pulseaudio
   ```

#### Video Not Playing (Perfect Score Celebration)
**Causes & Solutions:**

1. **Missing Dependencies:**
   ```bash
   pip install opencv-python Pillow
   ```

2. **Video File Missing:**
   - Check if `assets/files/images/stickman-dance.mp4` exists
   - Game falls back to static animation if missing

3. **Video Codec Issues:**
   ```bash
   # Try different OpenCV version
   pip uninstall opencv-python
   pip install opencv-python-headless
   ```

### Performance Issues

#### Game Running Slowly
**Solutions:**
1. Close unnecessary applications
2. Update graphics drivers
3. Reduce system load
4. Install without video features:
   ```bash
   pip install pygame numpy
   # Skip opencv-python and Pillow
   ```

#### High CPU Usage
**Causes:**
- Video playback using too many resources
- Multiple pygame mixer instances

**Solutions:**
- Restart the game
- Install lighter version without video support
- Close other applications

### File and Path Issues

#### "FileNotFoundError: assets/files/sounds/..."
**Solutions:**
1. **Check Working Directory:**
   ```bash
   pwd  # Should be in hangman-mcq-game directory
   ls assets/files/sounds/  # Should show .mp3 files
   ```

2. **Verify File Structure:**
   ```
   hangman-mcq-game/
   ├── hangman_game.py
   └── assets/
       └── files/
           └── sounds/
               ├── start.mp3
               ├── coin.mp3
               └── ...
   ```

3. **Fix Path Issues:**
   - Use forward slashes in paths
   - Avoid absolute paths
   - Run from repository root directory

#### Video File Not Found
**Solutions:**
1. **Check Video File:**
   ```bash
   ls -la assets/files/images/stickman-dance.mp4
   ```

2. **Path Issues:**
   - Ensure video is in correct location
   - Check file permissions (readable)

### Platform-Specific Issues

#### Windows Specific

1. **Python Not in PATH:**
   ```cmd
   # Add Python to PATH during installation
   # Or use full path: C:\Python39\python.exe hangman_game.py
   ```

2. **Windows Defender Blocking:**
   - Add game folder to Windows Defender exceptions
   - Some antivirus software flags pygame as suspicious

#### macOS Specific

1. **Gatekeeper Warnings:**
   ```bash
   # If Python blocked by Gatekeeper
   sudo xattr -r -d com.apple.quarantine /path/to/python
   ```

2. **Audio Permissions:**
   - Grant microphone permissions if prompted
   - Check System Preferences > Security & Privacy

#### Linux Specific

1. **X11 Issues:**
   ```bash
   # Install X11 if missing
   sudo apt-get install xorg
   
   # Set DISPLAY if using SSH
   export DISPLAY=:0
   ```

2. **Audio System Issues:**
   ```bash
   # Install ALSA development files
   sudo apt-get install libasound2-dev
   
   # For PulseAudio users
   sudo apt-get install pulseaudio-dev
   ```

## Debug Mode

### Enable Verbose Output
Add debug prints to `hangman_game.py` if needed:

```python
# Add at the top of __init__ method
print(f"Loading sounds from: {Path('assets/files/sounds').absolute()}")
print(f"Video path: {self.default_video_path.absolute()}")
```

### Test Individual Components

#### Test Pygame Audio:
```python
import pygame
pygame.mixer.init()
# Should not raise an exception
```

#### Test tkinter:
```python
import tkinter as tk
root = tk.Tk()
root.title("Test")
root.mainloop()
```

#### Test Video Support:
```python
import cv2
from PIL import Image
print("Video support available")
```

## Error Message Decoder

### Common Error Messages

#### `pygame.error: No available audio device`
**Meaning**: System has no audio output
**Solution**: 
- Check audio drivers
- Connect headphones/speakers
- Try `pygame.mixer.pre_init()` before `pygame.mixer.init()`

#### `cv2.error: (-2:Unspecified error)`
**Meaning**: Video file can't be read
**Solution**:
- Check video file exists and is readable
- Try different video codec
- Verify OpenCV installation

#### `TclError: no display name and no $DISPLAY environment variable`
**Meaning**: No GUI display available (Linux/SSH)
**Solution**:
```bash
# For SSH with X11 forwarding
ssh -X username@hostname
export DISPLAY=:0
```

## Getting Help

### Before Reporting Issues

1. **Try These Steps:**
   - Restart the game
   - Check your Python version: `python --version`
   - Verify installation: `python setup.py --install`
   - Test dependencies: `python -c "import pygame, numpy, tkinter"`

2. **Gather Information:**
   - Operating system and version
   - Python version
   - Complete error message
   - Steps to reproduce the issue

### Reporting Bugs

When creating a GitHub issue, include:

```
**Environment:**
- OS: [e.g., Windows 10, Ubuntu 20.04, macOS 12]
- Python Version: [e.g., 3.9.7]
- Game Version: [latest commit hash]

**Problem Description:**
[Clear description of what went wrong]

**Steps to Reproduce:**
1. [First step]
2. [Second step]
3. [etc.]

**Expected Behavior:**
[What should have happened]

**Actual Behavior:**
[What actually happened]

**Error Messages:**
```
[Full error traceback if any]
```

**Additional Context:**
[Any other relevant information]
```

### Community Support

- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For questions and general help
- **Wiki**: For community-contributed guides and tips

## Advanced Troubleshooting

### Clean Reinstallation

If all else fails, try a clean installation:

```bash
# Remove existing installation
pip uninstall pygame numpy opencv-python Pillow

# Clear pip cache
pip cache purge

# Fresh installation
pip install --no-cache-dir pygame numpy

# Test basic functionality
python -c "import pygame, numpy; print('Clean install successful')"
```

### Virtual Environment Reset

```bash
# Remove existing environment
rm -rf venv/  # or your venv name

# Create fresh environment
python -m venv fresh-env
source fresh-env/bin/activate  # or fresh-env\Scripts\activate on Windows

# Install fresh dependencies
pip install -r requirements.txt
```

### Log Collection

For persistent issues, collect logs:

```bash
# Run with verbose output
python hangman_game.py > game.log 2>&1

# Check the log file for errors
cat game.log
```

Remember: Most issues are related to missing dependencies or incorrect file paths. The setup script (`python setup.py --install`) resolves 90% of common problems!

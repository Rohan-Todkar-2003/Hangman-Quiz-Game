# scripts/launch_game.sh
#!/bin/bash
echo "🎯 Starting Interactive Hangman MCQ Game..."
echo "======================================"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Go to parent directory (repository root)
cd "$SCRIPT_DIR/.."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Error: Python not found. Please install Python 3.7+ and try again."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Check if main game file exists
if [ ! -f "hangman_game.py" ]; then
    echo "❌ Error: hangman_game.py not found in current directory."
    echo "Please run this script from the repository root."
    exit 1
fi

# Check basic dependencies
echo "🔍 Checking dependencies..."
$PYTHON_CMD -c "import pygame, tkinter, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Warning: Some dependencies missing. Run 'python setup.py --install' first."
    echo "Attempting to run anyway..."
fi

echo "🚀 Launching game..."
echo ""

# Launch the game
$PYTHON_CMD hangman_game.py

echo ""
echo "🎮 Thanks for playing!"

---

# scripts/launch_game.bat
@echo off
echo 🎯 Starting Interactive Hangman MCQ Game...
echo ======================================

REM Change to script directory then go to parent (repository root)
cd /d "%~dp0\.."

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python not found. Please install Python 3.7+ and add it to PATH.
    echo Download from: https://python.org/downloads/
    pause
    exit /b 1
)

REM Check if main game file exists
if not exist "hangman_game.py" (
    echo ❌ Error: hangman_game.py not found in current directory.
    echo Please run this script from the repository root.
    pause
    exit /b 1
)

REM Check basic dependencies
echo 🔍 Checking dependencies...
python -c "import pygame, tkinter, numpy" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Warning: Some dependencies missing. Run 'python setup.py --install' first.
    echo Attempting to run anyway...
)

echo 🚀 Launching game...
echo.

REM Launch the game
python hangman_game.py

echo.
echo 🎮 Thanks for playing!
pause

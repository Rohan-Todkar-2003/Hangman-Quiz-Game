#!/usr/bin/env python3
"""
setup.py

Enhanced setup script for Interactive Hangman MCQ Game.

Features:
- Python version check (>= 3.7)
- Optional virtualenv creation (--venv)
- Install core dependencies, and optional extras (video support)
- Try pip --user fallback when system-level install fails
- Generate requirements.txt
- Create cross-platform launch scripts
- Validate basic asset paths
- Test dependencies (pygame, tkinter, numpy, optional: opencv, pillow)
- Clear, colorized console output (if supported)
- Safe error handling and informative messages

Usage examples:
    python setup.py --install
    python setup.py --install --extras video
    python setup.py --venv venv
    python setup.py --generate-requirements
"""

from __future__ import annotations
import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

# Minimum supported Python
MIN_PYTHON_MAJOR = 3
MIN_PYTHON_MINOR = 7

# Packages
CORE_PACKAGES = [
    "pygame>=2.0.0",
    "numpy>=1.19.0"
]

VIDEO_PACKAGES = [
    "opencv-python>=4.5.0",
    "Pillow>=8.0.0"
]

# Files & assets that are expected (not mandatory but recommended)
EXPECTED_ASSETS = [
    Path("assets/files/sounds"),
    Path("assets/files/images"),
    Path("assets/files/images/stickman-dance.mp4"),
    Path("hangman_game.py"),  # Main entry expected name (or adapt)
    Path("hangman_mcq_game_updated_attempts.py")
]

# Colors (simple)
def _color(text: str, code: str) -> str:
    if sys.stdout.isatty():
        return f"\033[{code}m{text}\033[0m"
    return text

OK = lambda s: _color(s, "92")     # green
WARN = lambda s: _color(s, "93")   # yellow
ERR = lambda s: _color(s, "91")    # red
BOLD = lambda s: _color(s, "1")

# Utility command runner
def run_cmd(cmd: List[str], capture: bool = True, check: bool = True) -> Tuple[int, str, str]:
    """Run a subprocess command and return (returncode, stdout, stderr)."""
    try:
        completed = subprocess.run(cmd, capture_output=capture, text=True, check=check)
        out = completed.stdout.strip() if completed.stdout else ""
        err = completed.stderr.strip() if completed.stderr else ""
        return completed.returncode, out, err
    except subprocess.CalledProcessError as e:
        out = e.stdout.strip() if e.stdout else ""
        err = e.stderr.strip() if e.stderr else str(e)
        return e.returncode if e.returncode is not None else 1, out, err
    except FileNotFoundError as e:
        return 1, "", str(e)

# Python version check
def check_python_version() -> bool:
    v = sys.version_info
    ok = (v.major > MIN_PYTHON_MAJOR) or (v.major == MIN_PYTHON_MAJOR and v.minor >= MIN_PYTHON_MINOR)
    if ok:
        print(OK(f"✅ Python {v.major}.{v.minor}.{v.micro} — OK (>= {MIN_PYTHON_MAJOR}.{MIN_PYTHON_MINOR})"))
    else:
        print(ERR(f"❌ Python {MIN_PYTHON_MAJOR}.{MIN_PYTHON_MINOR}+ is required. Current: {v.major}.{v.minor}.{v.micro}"))
    return ok

# Create a virtual environment (optional)
def create_virtualenv(path: Path) -> bool:
    """Create a virtualenv at the given path using the venv module."""
    if path.exists():
        print(WARN(f"⚠️ Virtual environment path {path} already exists — skipping creation."))
        return True
    print(BOLD(f"🐣 Creating virtual environment at {path} ..."))
    rc, out, err = run_cmd([sys.executable, "-m", "venv", str(path)], capture=True, check=False)
    if rc == 0:
        print(OK("✅ Virtual environment created."))
        return True
    else:
        print(ERR(f"❌ Failed to create virtualenv: {err or out}"))
        return False

# Pip installer with graceful fallbacks
def pip_install(packages: List[str], use_user_fallback: bool = True, verbose: bool = False) -> List[str]:
    """Install packages via pip. Returns list of failed package specs."""
    failed = []
    for pkg in packages:
        print(BOLD(f"📦 Installing {pkg} ..."))
        cmd = [sys.executable, "-m", "pip", "install", pkg]
        rc, out, err = run_cmd(cmd, capture=True, check=False)
        if rc != 0:
            if use_user_fallback and ("Permission denied" in err or "Could not install packages" in err or rc != 0):
                print(WARN(f"⚠️ System install failed for {pkg}, trying --user fallback ..."))
                cmd_user = [sys.executable, "-m", "pip", "install", "--user", pkg]
                rc2, out2, err2 = run_cmd(cmd_user, capture=True, check=False)
                if rc2 != 0:
                    print(ERR(f"❌ Failed to install {pkg} even with --user: {err2 or out2}"))
                    failed.append(pkg)
                else:
                    if verbose:
                        print(out2)
                    print(OK(f"✅ {pkg} installed with --user"))
            else:
                print(ERR(f"❌ Failed to install {pkg}: {err or out}"))
                failed.append(pkg)
        else:
            if verbose and out:
                print(out)
            print(OK(f"✅ {pkg} installed"))
    return failed

# Generate a minimal requirements.txt
def generate_requirements(target: Path, packages: List[str], extras: List[str] = None) -> bool:
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        lines = packages.copy()
        if extras:
            lines += extras
        # Normalize to newline separated
        with target.open("w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(OK(f"✅ requirements written to {target}"))
        return True
    except Exception as e:
        print(ERR(f"❌ Failed to write requirements: {e}"))
        return False

# Check tkinter availability, with instructions
def check_tkinter() -> bool:
    try:
        import tkinter  # type: ignore
        print(OK("✅ Tkinter is available"))
        return True
    except Exception:
        print(WARN("⚠️ Tkinter not available in this Python environment."))
        print("  Installation suggestions:")
        system = platform.system().lower()
        if "linux" in system:
            print("    - Ubuntu / Debian: sudo apt-get install python3-tk")
        elif "darwin" in system:
            print("    - macOS: Tkinter is usually bundled; use brew/python.org installers if missing.")
        elif "windows" in system:
            print("    - Windows: Tkinter is usually bundled with official Python installers.")
        else:
            print("    - Refer to your OS package manager to install tkinter / tk")
        return False

# Lightweight dependency tests (non-exhaustive)
def test_dependencies(check_video: bool = False) -> bool:
    """Return True if core dependencies seem okay. Print diagnostic info."""
    ok = True
    print(BOLD("\n🧪 Testing dependencies..."))

    # pygame
    try:
        import pygame  # type: ignore
        try:
            pygame.mixer.init()
            pygame.mixer.quit()
            print(OK("✅ pygame ok (audio subsystem initialized)"))
        except Exception as e:
            print(WARN(f"⚠️ pygame imported but audio init failed: {e}"))
    except Exception:
        print(ERR("❌ pygame not importable. Install with `pip install pygame`"))
        ok = False

    # numpy
    try:
        import numpy  # type: ignore
        print(OK("✅ numpy is available"))
    except Exception:
        print(WARN("⚠️ numpy not available — beep fallbacks will not be generated"))

    # tkinter
    if not check_tkinter():
        ok = False

    # optional video stack
    if check_video:
        try:
            import cv2  # type: ignore
            from PIL import Image  # type: ignore
            print(OK("✅ OpenCV and Pillow available for video playback"))
        except Exception:
            print(WARN("⚠️ OpenCV / Pillow not available — video playback will be disabled"))
            ok = False

    return ok

# Create cross-platform launch script(s)
def create_launch_script(main_script: str = "hangman_game.py"):
    """Write a small launch script for Windows and Unix-like systems."""
    # Windows .bat
    if os.name == "nt":
        bat = Path("launch_game.bat")
        content = f"""@echo off
REM Launch script for Interactive Hangman MCQ Game
echo Starting Interactive Hangman MCQ Game...
python "{main_script}"
pause
"""
        bat.write_text(content, encoding="utf-8")
        print(OK(f"✅ Created {bat}"))
    # Unix .sh
    sh = Path("launch_game.sh")
    content_sh = f"""#!/usr/bin/env bash
# Launch script for Interactive Hangman MCQ Game
echo "Starting Interactive Hangman MCQ Game..."
python3 "{main_script}"
"""
    sh.write_text(content_sh, encoding="utf-8")
    try:
        sh.chmod(0o755)
    except Exception:
        pass
    print(OK(f"✅ Created {sh}"))

# Check for some expected assets and warn if missing
def check_assets(expected: List[Path]):
    print(BOLD("\n📁 Checking expected asset files/folders..."))
    missing = []
    for p in expected:
        if not p.exists():
            missing.append(p)
            print(WARN(f" - Missing: {p}"))
        else:
            print(OK(f" - Found: {p}"))
    if missing:
        print(WARN("\n⚠️ Some assets or files are missing. The game may still run but may lack sounds/images/videos."))
    else:
        print(OK("\n✅ All expected assets found (or at least present)."))

# Entrypoint
def main(argv: List[str] | None = None):
    parser = argparse.ArgumentParser(prog="setup.py", description="Setup helper for Interactive Hangman MCQ Game")
    parser.add_argument("--install", action="store_true", help="Install core dependencies via pip")
    parser.add_argument("--extras", choices=["none", "video"], default="none", help="Install optional extras")
    parser.add_argument("--venv", nargs="?", const="venv", help="Create a virtualenv at provided path (default: ./venv)")
    parser.add_argument("--generate-requirements", action="store_true", help="Write a requirements.txt file with packages")
    parser.add_argument("--main-script", default="hangman_game.py", help="Main python script filename for launch scripts")
    parser.add_argument("--no-assets-check", action="store_true", help="Skip checking for expected asset files")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args(argv)

    print(BOLD("\n🎯 Interactive Hangman MCQ Game - Setup Helper\n" + "=" * 60))

    if not check_python_version():
        print(ERR("Please install a compatible Python version and re-run setup."))
        sys.exit(1)

    if args.venv:
        venv_path = Path(args.venv)
        if not create_virtualenv(venv_path):
            print(ERR("Virtualenv creation failed — aborting."))
            sys.exit(1)
        print(OK("✅ Virtualenv created. Activate it before installing packages if you want isolation."))
        print("  - Windows: venv\\Scripts\\activate")
        print("  - Unix: source venv/bin/activate")
        # Do not automatically install into venv — user can activate

    # Asset checks
    if not args.no_assets_check:
        check_assets(EXPECTED_ASSETS)

    # Install packages
    failed_pkgs: List[str] = []
    installed_any = False
    if args.install:
        to_install = CORE_PACKAGES.copy()
        extras_installed = []
        if args.extras == "video":
            to_install += VIDEO_PACKAGES
            extras_installed = VIDEO_PACKAGES
            print(BOLD("\n🔎 Installing with video support (opencv + pillow) ..."))
        else:
            print(BOLD("\n🔎 Installing core packages ..."))

        failed_pkgs = pip_install(to_install, use_user_fallback=True, verbose=args.verbose)
        installed_any = True

        if failed_pkgs:
            print(WARN(f"\n⚠️ Some packages failed to install: {', '.join(failed_pkgs)}"))
            print("You may try to re-run with elevated permissions or install the failed packages manually.")
        else:
            print(OK("\n✅ All requested packages installed."))

    # requirements.txt generation
    if args.generate_requirements:
        extras = VIDEO_PACKAGES if args.extras == "video" else []
        generate_requirements(Path("requirements.txt"), CORE_PACKAGES, extras)

    # Provide a simple dependency quick-test if we installed or user asked
    if installed_any:
        ok = test_dependencies(check_video=(args.extras == "video"))
        if ok:
            print(OK("\n✅ Dependency smoke-test passed."))
        else:
            print(WARN("\n⚠️ Some dependency tests reported issues. See messages above."))

    # Create launch scripts (always create; user can ignore)
    create_launch_script(main_script=args.main_script)

    print(BOLD("\n🚀 Setup finished - Next steps"))
    print("-" * 40)
    print("1) To run the game:")
    print(f"   - python {args.main_script}")
    print("   - or use launch_game.sh / launch_game.bat created by this script.")
    print("2) If you created a virtualenv, activate it before installing or running:")
    print("   - Windows: venv\\Scripts\\activate")
    print("   - Unix: source venv/bin/activate")
    print("3) If sounds or videos don't play, ensure pygame, numpy, opencv-python and pillow are installed.")
    print("\n🎮 Enjoy the game!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n" + WARN("Setup interrupted by user."))
        sys.exit(1)
    except Exception as e:
        print(ERR(f"Unexpected error during setup: {e}"))
        sys.exit(2)

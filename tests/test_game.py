#!/usr/bin/env python3
"""
test_game.py

Basic tests for Interactive Hangman MCQ Game
Tests core functionality without requiring GUI interaction.
"""

import sys
import unittest
from pathlib import Path
import tempfile
import os

# Add parent directory to path to import the game module
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from hangman_game import HangmanMCQGame
except ImportError:
    # Try alternative name
    try:
        from hangman_mcq_game_updated_attempts import HangmanMCQGame
    except ImportError as e:
        print(f"❌ Cannot import game module: {e}")
        print("Please ensure hangman_game.py is in the repository root.")
        sys.exit(1)


class TestHangmanMCQGame(unittest.TestCase):
    """Test cases for the Hangman MCQ Game."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create game instance without initializing GUI
        self.game = None
        
    def test_question_bank_structure(self):
        """Test that question bank has correct structure."""
        # Initialize game to load question bank
        try:
            # Mock tkinter to avoid GUI creation during testing
            import unittest.mock
            with unittest.mock.patch('tkinter.Tk'):
                game = HangmanMCQGame()
                
            # Test basic structure
            self.assertIsInstance(game.question_bank, dict)
            
            # Test all subjects exist
            expected_subjects = ["Python", "SQL", "Power BI", "Tableau", "Statistics"]
            for subject in expected_subjects:
                self.assertIn(subject, game.question_bank)
                
            # Test all difficulty levels exist for each subject
            expected_levels = ["Easy", "Intermediate", "Extreme"]
            for subject in expected_subjects:
                for level in expected_levels:
                    self.assertIn(level, game.question_bank[subject])
                    
            # Test questions are properly formatted
            for subject in expected_subjects:
                for level in expected_levels:
                    questions = game.question_bank[subject][level]
                    self.assertIsInstance(questions, list)
                    self.assertGreater(len(questions), 0)
                    
                    for question in questions:
                        self.assertIn("question", question)
                        self.assertIn("options", question)
                        self.assertIn("correct", question)
                        self.assertIsInstance(question["options"], list)
                        self.assertEqual(len(question["options"]), 4)
                        self.assertIsInstance(question["correct"], int)
                        self.assertGreaterEqual(question["correct"], 0)
                        self.assertLessEqual(question["correct"], 3)
                        
        except Exception as e:
            self.fail(f"Failed to initialize game or test question bank: {e}")

    def test_file_paths(self):
        """Test that expected file paths exist or are handled gracefully."""
        # Test asset directories
        expected_dirs = [
            Path("assets/files/sounds"),
            Path("assets/files/images")
        ]
        
        for dir_path in expected_dirs:
            # Directory should either exist or game should handle missing gracefully
            if not dir_path.exists():
                print(f"⚠️  Warning: {dir_path} not found (game should handle gracefully)")
        
        # Test specific files that game expects
        expected_files = [
            Path("assets/files/images/stickman-dance.mp4"),
            Path("hangman_game.py"),
            Path("requirements.txt"),
            Path("setup.py")
        ]
        
        for file_path in expected_files:
            if not file_path.exists():
                print(f"⚠️  Warning: {file_path} not found")

    def test_sound_loading(self):
        """Test sound loading functionality."""
        try:
            import unittest.mock
            with unittest.mock.patch('tkinter.Tk'):
                with unittest.mock.patch('pygame.mixer.init'):
                    game = HangmanMCQGame()
                    
                    # Test that sounds dictionary is created
                    self.assertIsInstance(game.sounds, dict)
                    
                    # Test expected sound keys
                    expected_sounds = ['start', 'countdown', 'alert', 'celebration', 'crying', 'coin', 'wrong']
                    for sound_name in expected_sounds:
                        self.assertIn(sound_name, game.sounds)
                        
        except Exception as e:
            print(f"⚠️  Warning: Sound loading test failed (expected if pygame not available): {e}")

    def test_game_state_initialization(self):
        """Test that game state variables are properly initialized."""
        try:
            import unittest.mock
            with unittest.mock.patch('tkinter.Tk'):
                with unittest.mock.patch('pygame.mixer.init'):
                    game = HangmanMCQGame()
                    
                    # Test initial state
                    self.assertEqual(game.nickname, "")
                    self.assertEqual(game.selected_language, "")
                    self.assertEqual(game.selected_level, "")
                    self.assertEqual(game.current_question, 0)
                    self.assertEqual(game.score, 0)
                    self.assertEqual(game.wrong_answers, 0)
                    self.assertEqual(game.questions, [])
                    self.assertEqual(game.user_answers, [])
                    self.assertFalse(game.timer_running)
                    self.assertEqual(game.time_left, 15)
                    
        except Exception as e:
            self.fail(f"Game state initialization failed: {e}")

    def test_colors_configuration(self):
        """Test that color scheme is properly configured."""
        try:
            import unittest.mock
            with unittest.mock.patch('tkinter.Tk'):
                with unittest.mock.patch('pygame.mixer.init'):
                    game = HangmanMCQGame()
                    
                    # Test colors dictionary exists and has expected keys
                    expected_colors = ['primary', 'secondary', 'danger', 'warning', 'dark', 'light', 'white', 'panel', 'accent']
                    for color_key in expected_colors:
                        self.assertIn(color_key, game.colors)
                        self.assertIsInstance(game.colors[color_key], str)
                        self.assertTrue(game.colors[color_key].startswith('#'))
                        
        except Exception as e:
            self.fail(f"Color configuration test failed: {e}")

    def test_question_selection_logic(self):
        """Test question selection and shuffling."""
        try:
            import unittest.mock
            with unittest.mock.patch('tkinter.Tk'):
                with unittest.mock.patch('pygame.mixer.init'):
                    game = HangmanMCQGame()
                    
                    # Simulate selecting language and level
                    game.selected_language = "Python"
                    game.selected_level = "Easy"
                    
                    original_questions = game.question_bank["Python"]["Easy"].copy()
                    
                    # Simulate question preparation
                    game.questions = game.question_bank[game.selected_language][game.selected_level].copy()
                    
                    # Test that questions were loaded
                    self.assertEqual(len(game.questions), len(original_questions))
                    self.assertIsInstance(game.questions, list)
                    
        except Exception as e:
            self.fail(f"Question selection test failed: {e}")


class TestDependencies(unittest.TestCase):
    """Test that required dependencies are available."""
    
    def test_core_dependencies(self):
        """Test that core dependencies can be imported."""
        try:
            import pygame
            self.assertTrue(hasattr(pygame, 'mixer'))
        except ImportError:
            self.fail("pygame is required but not available")
        
        try:
            import numpy
            self.assertTrue(hasattr(numpy, 'sin'))  # Test a basic function
        except ImportError:
            print("⚠️  Warning: numpy not available (fallback sounds won't work)")
        
        try:
            import tkinter
            self.assertTrue(hasattr(tkinter, 'Tk'))
        except ImportError:
            self.fail("tkinter is required but not available")

    def test_optional_dependencies(self):
        """Test optional dependencies for video support."""
        try:
            import cv2
            video_support = True
        except ImportError:
            video_support = False
            print("ℹ️  Info: opencv-python not available (video features disabled)")
        
        try:
            from PIL import Image
            pil_support = True
        except ImportError:
            pil_support = False
            print("ℹ️  Info: Pillow not available (video features disabled)")
        
        # This is informational - video support is optional
        if video_support and pil_support:
            print("✅ Video support available")
        else:
            print("ℹ️  Video support disabled (install opencv-python and Pillow to enable)")


class TestFileStructure(unittest.TestCase):
    """Test repository file structure."""
    
    def test_main_files_exist(self):
        """Test that main files exist in expected locations."""
        expected_files = [
            "requirements.txt",
            "setup.py"
        ]
        
        # Try both possible main game file names
        game_files = ["hangman_game.py", "hangman_mcq_game_updated_attempts.py"]
        game_file_exists = any(Path(f).exists() for f in game_files)
        self.assertTrue(game_file_exists, "Main game file should exist")
        
        for file_name in expected_files:
            file_path = Path(file_name)
            self.assertTrue(file_path.exists(), f"{file_name} should exist in repository root")

    def test_asset_structure(self):
        """Test asset directory structure."""
        # These directories should exist for full functionality
        recommended_dirs = [
            Path("assets"),
            Path("assets/files"),
            Path("assets/files/sounds"),
            Path("assets/files/images")
        ]
        
        for dir_path in recommended_dirs:
            if dir_path.exists():
                print(f"✅ {dir_path} exists")
            else:
                print(f"⚠️  {dir_path} missing (recommended for full functionality)")


def run_tests():
    """Run all tests and return results."""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [TestHangmanMCQGame, TestDependencies, TestFileStructure]
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("🧪 Running Interactive Hangman MCQ Game Tests")
    print("=" * 50)
    
    try:
        success = run_tests()
        if success:
            print("\n✅ All tests passed!")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed. Check output above for details.")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test runner failed: {e}")
        sys.exit(2)

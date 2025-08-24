# hangman_mcq_game_updated_attempts.py
import tkinter as tk
from tkinter import messagebox
import pygame
import random
from pathlib import Path
import os

# Optional imports for video playback (cv2 + Pillow). If unavailable we gracefully fallback.
try:
    import cv2
    from PIL import Image, ImageTk
    OPENCV_AVAILABLE = True
except Exception:
    OPENCV_AVAILABLE = False


class HangmanMCQGame:
    def __init__(self):
        # Try initialize pygame for sound; if fails, continue without crash
        try:
            pygame.mixer.init()
            self.pygame_available = True
        except Exception:
            self.pygame_available = False

        # Main window setup
        self.root = tk.Tk()
        self.root.title("Interactive Hangman MCQ Game")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1a1a2e")  # Darker background for better contrast
        self.root.resizable(True, True)

        # Game state variables
        self.nickname = ""
        self.selected_language = ""
        self.selected_level = ""
        self.current_question = 0
        self.score = 0
        # wrong_answers counts only timeups (per request)
        self.wrong_answers = 0
        self.questions = []
        self.user_answers = []
        self.timer_running = False
        self.time_left = 15
        self.timer_after_id = None  # store after() id to cancel if needed

        # Video playback state
        self.video_capture = None
        self.video_after_id = None
        self.video_frame_image = None  # keep reference to PhotoImage to avoid GC
        self.video_playing = False
        # Default video path (user provided)
        self.default_video_path = Path("assets/files/images/stickman-dance.mp4")

        # UI Elements
        self.main_frame = None
        self.timer_label = None
        self.score_label = None
        self.hangman_canvas = None
        self.feedback_label = None  # show "Incorrect - try again!" feedback

        # Colors and styling - Updated color scheme
        self.colors = {
            'primary': '#4361ee',   # Vibrant blue
            'secondary': '#06d6a0', # Teal green
            'danger': '#ef476f',    # Coral red
            'warning': '#ffd166',   # Yellow
            'dark': '#1a1a2e',      # Dark blue
            'light': '#f8f9fa',     # Light gray
            'white': '#ffffff',
            'panel': '#2d4059',     # Darker panel
            'accent': '#7209b7'     # Purple accent
        }

        # Button sizing constants (consistent across the UI)
        self.BUTTON_WIDTH = 22
        self.BUTTON_HEIGHT = 2
        self.BUTTON_FONT = ("Montserrat", 12, "bold")  # More modern font

        # Load questions and sounds
        self.load_questions()
        self.load_sounds()

        # Start with the initial screen
        self.show_start_screen()

    def load_questions(self):
        """Full question bank (copied from your original)."""
        self.question_bank = {
            "Python": {
                "Easy": [
                    {"question": "What is the correct file extension for Python files?",
                     "options": [".py", ".python", ".pt", ".p"], "correct": 0},
                    {"question": "Which keyword is used to define a function in Python?",
                     "options": ["function", "def", "define", "func"], "correct": 1},
                    {"question": "What does 'len()' function return?",
                     "options": ["Length of object", "Last element", "First element", "Type of object"], "correct": 0},
                    {"question": "Which of these is a Python data type?",
                     "options": ["int", "string", "boolean", "All of the above"], "correct": 3},
                    {"question": "How do you create a comment in Python?",
                     "options": ["// comment", "/* comment */", "# comment", "-- comment"], "correct": 2},
                    {"question": "What is the output of print(2 + 3)?",
                     "options": ["23", "5", "Error", "None"], "correct": 1}
                ],
                "Intermediate": [
                    {"question": "What is a lambda function in Python?",
                     "options": ["Anonymous function", "Built-in function", "Class method", "Module function"], "correct": 0},
                    {"question": "Which method is used to add an element to a list?",
                     "options": ["add()", "append()", "insert()", "Both b and c"], "correct": 3},
                    {"question": "What is the purpose of '__init__' method?",
                     "options": ["Initialize object", "Delete object", "Copy object", "Print object"], "correct": 0},
                    {"question": "Which keyword is used for exception handling?",
                     "options": ["catch", "try", "handle", "exception"], "correct": 1},
                    {"question": "What does 'self' refer to in a class?",
                     "options": ["Class name", "Method name", "Current instance", "Parent class"], "correct": 2},
                    {"question": "Which of these is mutable in Python?",
                     "options": ["tuple", "string", "list", "int"], "correct": 2}
                ],
                "Extreme": [
                    {"question": "What is a decorator in Python?",
                     "options": ["Design pattern", "Function wrapper", "Class inheritance", "Module import"], "correct": 1},
                    {"question": "What is the Global Interpreter Lock (GIL)?",
                     "options": ["Memory manager", "Thread synchronization", "File lock", "Network protocol"], "correct": 1},
                    {"question": "Which method is called when an object is garbage collected?",
                     "options": ["__del__", "__gc__", "__free__", "__destroy__"], "correct": 0},
                    {"question": "What is monkey patching?",
                     "options": ["Bug fixing", "Dynamic modification", "Code testing", "Memory optimization"], "correct": 1},
                    {"question": "What does 'yield' keyword do?",
                     "options": ["Return value", "Create generator", "Pause function", "Both b and c"], "correct": 3},
                    {"question": "What is metaclass in Python?",
                     "options": ["Class of class", "Super class", "Abstract class", "Inner class"], "correct": 0}
                ]
            },
            "SQL": {
                "Easy": [
                    {"question": "Which command is used to retrieve data from a database?",
                     "options": ["GET", "SELECT", "FETCH", "RETRIEVE"], "correct": 1},
                    {"question": "What does SQL stand for?",
                     "options": ["Simple Query Language", "Structured Query Language", "Standard Query Language", "Sequential Query Language"], "correct": 1},
                    {"question": "Which clause is used to filter records?",
                     "options": ["FILTER", "WHERE", "HAVING", "CONDITION"], "correct": 1},
                    {"question": "What is a primary key?",
                     "options": ["Main table", "Unique identifier", "First column", "Important data"], "correct": 1},
                    {"question": "Which command adds new records to a table?",
                     "options": ["ADD", "INSERT", "CREATE", "NEW"], "correct": 1},
                    {"question": "What does ORDER BY clause do?",
                     "options": ["Filter data", "Sort data", "Group data", "Join tables"], "correct": 1}
                ],
                "Intermediate": [
                    {"question": "What is a foreign key?",
                     "options": ["External table", "Reference to primary key", "Encrypted key", "Backup key"], "correct": 1},
                    {"question": "Which JOIN returns all records from both tables?",
                     "options": ["INNER JOIN", "LEFT JOIN", "FULL OUTER JOIN", "RIGHT JOIN"], "correct": 2},
                    {"question": "What is normalization?",
                     "options": ["Data backup", "Reduce redundancy", "Increase speed", "Data encryption"], "correct": 1},
                    {"question": "Which aggregate function calculates average?",
                     "options": ["MEAN()", "AVG()", "AVERAGE()", "CALC()"], "correct": 1},
                    {"question": "What does HAVING clause do?",
                     "options": ["Filter groups", "Sort data", "Join tables", "Create index"], "correct": 0},
                    {"question": "Which constraint ensures unique values?",
                     "options": ["PRIMARY", "UNIQUE", "NOT NULL", "CHECK"], "correct": 1}
                ],
                "Extreme": [
                    {"question": "What is a CTE in SQL?",
                     "options": ["Common Table Expression", "Computed Table Entry", "Complex Transaction Event", "Continuous Table Execution"], "correct": 0},
                    {"question": "What is the difference between RANK() and DENSE_RANK()?",
                     "options": ["No difference", "RANK() skips numbers", "DENSE_RANK() skips numbers", "Both are identical"], "correct": 1},
                    {"question": "What is a window function?",
                     "options": ["GUI function", "Performs calculation across rows", "Opens new window", "Time-based function"], "correct": 1},
                    {"question": "What is ACID in database?",
                     "options": ["Database type", "Transaction properties", "Query language", "Storage method"], "correct": 1},
                    {"question": "What is a materialized view?",
                     "options": ["Virtual table", "Physical copy of query result", "Indexed view", "Temporary table"], "correct": 1},
                    {"question": "What is database sharding?",
                     "options": ["Data encryption", "Horizontal partitioning", "Backup strategy", "Index optimization"], "correct": 1}
                ]
            },
            "Power BI": {
                "Easy": [
                    {"question": "What is Power BI primarily used for?",
                     "options": ["Data visualization", "Programming", "Web development", "Game development"], "correct": 0},
                    {"question": "Which file format can Power BI import?",
                     "options": ["Excel", "CSV", "JSON", "All of the above"], "correct": 3},
                    {"question": "What is a Power BI Dashboard?",
                     "options": ["Single page view", "Multi-page report", "Data source", "Query editor"], "correct": 0},
                    {"question": "Which component is used to create calculations?",
                     "options": ["Power Query", "DAX", "Power Pivot", "M Language"], "correct": 1},
                    {"question": "What does ETL stand for?",
                     "options": ["Extract Transform Load", "Edit Text Language", "Export Table Logic", "Execute Test Logic"], "correct": 0},
                    {"question": "Which view is used to create relationships?",
                     "options": ["Data view", "Report view", "Model view", "Table view"], "correct": 2}
                ],
                "Intermediate": [
                    {"question": "What is a calculated column vs calculated measure?",
                     "options": ["Same thing", "Column stores values, measure calculates", "Measure stores values, column calculates", "No difference"], "correct": 1},
                    {"question": "What is row-level security?",
                     "options": ["Data encryption", "User-based data filtering", "Password protection", "Backup security"], "correct": 1},
                    {"question": "Which function creates a date table?",
                     "options": ["CALENDAR()", "DATEADD()", "TODAY()", "MONTH()"], "correct": 0},
                    {"question": "What is Power Query used for?",
                     "options": ["Creating visuals", "Data transformation", "Publishing reports", "User management"], "correct": 1},
                    {"question": "What is a slicer in Power BI?",
                     "options": ["Data filter", "Chart type", "Data source", "Calculation"], "correct": 0},
                    {"question": "What does SUMMARIZE function do?",
                     "options": ["Creates summary table", "Adds totals", "Counts rows", "Filters data"], "correct": 0}
                ],
                "Extreme": [
                    {"question": "What is the difference between DirectQuery and Import mode?",
                     "options": ["No difference", "DirectQuery queries live data", "Import queries live data", "Both cache data"], "correct": 1},
                    {"question": "What is a composite model?",
                     "options": ["Multiple data sources", "Complex visual", "Calculated table", "Shared dataset"], "correct": 0},
                    {"question": "What is incremental refresh?",
                     "options": ["Full data reload", "Partial data update", "Real-time streaming", "Data compression"], "correct": 1},
                    {"question": "What is the USERELATIONSHIP function for?",
                     "options": ["Create relationship", "Activate inactive relationship", "Delete relationship", "Modify relationship"], "correct": 1},
                    {"question": "What is a calculation group?",
                     "options": ["Multiple measures", "Time intelligence shortcuts", "Data grouping", "Visual grouping"], "correct": 1},
                    {"question": "What is Power BI Premium Per User?",
                     "options": ["Free version", "Individual licensing", "Enterprise license", "Developer version"], "correct": 1}
                ]
            },
            "Tableau": {
                "Easy": [
                    {"question": "What type of software is Tableau?",
                     "options": ["Database", "Data visualization", "Programming IDE", "Web browser"], "correct": 1},
                    {"question": "What is a worksheet in Tableau?",
                     "options": ["Data source", "Single visualization", "Dashboard", "Story"], "correct": 1},
                    {"question": "Which shelf is used for colors in Tableau?",
                     "options": ["Rows", "Columns", "Marks", "Filters"], "correct": 2},
                    {"question": "What does 'Show Me' panel do?",
                     "options": ["Shows data", "Suggests chart types", "Shows errors", "Shows filters"], "correct": 1},
                    {"question": "What is a dimension in Tableau?",
                     "options": ["Numerical data", "Categorical data", "Calculated field", "Parameter"], "correct": 1},
                    {"question": "How do you create a calculated field?",
                     "options": ["Data menu", "Analysis menu", "Right-click in data pane", "All of the above"], "correct": 3}
                ],
                "Intermediate": [
                    {"question": "What is the difference between a dashboard and a story?",
                     "options": ["No difference", "Dashboard is interactive, story is sequential", "Story is interactive, dashboard is sequential", "Both are identical"], "correct": 1},
                    {"question": "What is a parameter in Tableau?",
                     "options": ["Data source", "User input control", "Calculated field", "Filter"], "correct": 1},
                    {"question": "What does LOD stand for?",
                     "options": ["Level of Detail", "Line of Data", "Logic of Display", "List of Dimensions"], "correct": 0},
                    {"question": "Which join type returns all records from left table?",
                     "options": ["Inner", "Left", "Right", "Full Outer"], "correct": 1},
                    {"question": "What is a dual axis chart?",
                     "options": ["Two separate charts", "Chart with two Y-axes", "Chart with two X-axes", "Two-dimensional chart"], "correct": 1},
                    {"question": "What is data blending?",
                     "options": ["Combining multiple data sources", "Mixing colors", "Joining tables", "Filtering data"], "correct": 0}
                ],
                "Extreme": [
                    {"question": "What is the order of operations in Tableau?",
                     "options": ["Random", "Extract, Data Source, Context, Dimension, Measure filters", "Alphabetical", "User-defined"], "correct": 1},
                    {"question": "What is table calculation?",
                     "options": ["Database calculation", "Calculation on query result", "Excel formula", "SQL function"], "correct": 1},
                    {"question": "What is context filter?",
                     "options": ["Regular filter", "High priority filter", "Dashboard filter", "Quick filter"], "correct": 1},
                    {"question": "What is incremental extract refresh?",
                     "options": ["Full data refresh", "Partial data update", "Real-time data", "No refresh"], "correct": 1},
                    {"question": "What is Tableau Prep?",
                     "options": ["Data preparation tool", "Advanced analytics", "Server administration", "Mobile app"], "correct": 0},
                    {"question": "What is a Tableau hyperextract?",
                     "options": ["Large file", "Optimized data engine", "Cloud storage", "Backup file"], "correct": 1}
                ]
            },
            "Statistics": {
                "Easy": [
                    {"question": "What does mean represent?",
                     "options": ["Most frequent value", "Middle value", "Average value", "Highest value"], "correct": 2},
                    {"question": "What is the median of [1, 2, 3, 4, 5]?",
                     "options": ["2", "3", "4", "5"], "correct": 1},
                    {"question": "What does standard deviation measure?",
                     "options": ["Central tendency", "Spread of data", "Data type", "Sample size"], "correct": 1},
                    {"question": "What is population vs sample?",
                     "options": ["Same thing", "Population is entire group, sample is subset", "Sample is entire group, population is subset", "No difference"], "correct": 1},
                    {"question": "What is probability range?",
                     "options": ["0 to 100", "0 to 1", "-1 to 1", "Any number"], "correct": 1},
                    {"question": "What is mode in statistics?",
                     "options": ["Average", "Most frequent value", "Middle value", "Range"], "correct": 1}
                ],
                "Intermediate": [
                    {"question": "What is correlation coefficient range?",
                     "options": ["0 to 1", "-1 to 1", "0 to 100", "Any number"], "correct": 1},
                    {"question": "What does p-value indicate?",
                     "options": ["Population size", "Probability of result", "Sample mean", "Standard error"], "correct": 1},
                    {"question": "What is null hypothesis?",
                     "options": ["No relationship exists", "Strong relationship exists", "Data is invalid", "Sample is biased"], "correct": 0},
                    {"question": "What is Type I error?",
                     "options": ["Accepting false null", "Rejecting true null", "Wrong sample", "Calculation error"], "correct": 1},
                    {"question": "What is confidence interval?",
                     "options": ["Range of possible values", "Single point estimate", "Error measurement", "Sample size"], "correct": 0},
                    {"question": "What is regression analysis?",
                     "options": ["Data sorting", "Relationship modeling", "Data cleaning", "Sampling method"], "correct": 1}
                ],
                "Extreme": [
                    {"question": "What is heteroscedasticity?",
                     "options": ["Equal variance", "Unequal variance", "Normal distribution", "Random sampling"], "correct": 1},
                    {"question": "What is multicollinearity?",
                     "options": ["Multiple samples", "Correlated predictors", "Multiple outcomes", "Complex model"], "correct": 1},
                    {"question": "What is Bayesian statistics?",
                     "options": ["Frequentist approach", "Prior probability approach", "Sample-based approach", "Population-based approach"], "correct": 1},
                    {"question": "What is ANOVA used for?",
                     "options": ["Two group comparison", "Multiple group comparison", "Correlation analysis", "Regression analysis"], "correct": 1},
                    {"question": "What is Central Limit Theorem?",
                     "options": ["Sample distribution normality", "Population normality", "Data symmetry", "Error distribution"], "correct": 0},
                    {"question": "What is bootstrapping in statistics?",
                     "options": ["Starting analysis", "Resampling method", "Data collection", "Model validation"], "correct": 1}
                ]
            }
        }

    def load_sounds(self):
        """
        Load sounds from assets/files/sounds/ or fallback to generated beeps (if numpy available).
        Expected filenames (you can provide either .wav or .mp3):
          - start.wav / start.mp3
          - alert.wav / alert.mp3
          - celebration.wav / celebration.mp3
          - crying.wav / crying.mp3
          - coin.wav / coin.mp3
        """
        self.sounds = {}
        base_dir = Path("assets/files/sounds")
        
        expected = {
            'start': ["start.wav", "start.mp3"],
            'countdown': ["countdown.wav", "countdown.mp3"],   # NEW
            'alert': ["alert.wav", "alert.mp3"],               # (optional legacy alert)
            'celebration': ["celebration.wav", "celebration.mp3"],
            'crying': ["crying.wav", "crying.mp3"],
            'coin': ["coin.wav", "coin.mp3"],
            'wrong': ["wrong.wav", "wrong.mp3"]                # NEW
        }

        # Attempt to load from files
        if self.pygame_available:
            for name, candidates in expected.items():
                sound_obj = None
                for fname in candidates:
                    p = base_dir / fname
                    if p.exists():
                        try:
                            sound_obj = pygame.mixer.Sound(str(p))
                            break
                        except Exception:
                            sound_obj = None
                self.sounds[name] = sound_obj

        # If any sound missing, try to create a beep fallback (numpy required)
        def make_beep(freq, duration_ms):
            try:
                import numpy as np
                sample_rate = 22050
                frames = int(duration_ms * sample_rate / 1000)
                arr = (32767 * 0.5 * np.sin(2 * np.pi * freq * np.arange(frames) / sample_rate)).astype('int16')
                if self.pygame_available:
                    return pygame.sndarray.make_sound(arr)
            except Exception:
                return None
            return None

        fallback_map = {
            'start': (700, 300),
            'countdown': (1200, 80),   # short high tick for each second
            'alert': (900, 120),
            'celebration': (600, 500),
            'crying': (300, 800),   
            'coin': (1100, 120),
            'wrong': (350, 220)
        }
        for name, (f, d) in fallback_map.items():
            if name not in self.sounds or self.sounds[name] is None:
                self.sounds[name] = make_beep(f, d)

    def play_sound(self, sound_name):
        """Play a sound effect safely (no crash)."""
        try:
            snd = self.sounds.get(sound_name)
            if snd:
                snd.play()
        except Exception:
            pass

    def clear_screen(self):
        """Clear the current screen (and cancel pending timers if any)."""
        try:
            if self.timer_after_id:
                self.root.after_cancel(self.timer_after_id)
                self.timer_after_id = None
        except Exception:
            self.timer_after_id = None

        # Stop any video playback before destroying frames
        self.stop_video_playback()

        if self.main_frame:
            self.main_frame.destroy()
        self.main_frame = tk.Frame(self.root, bg=self.colors['dark'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def stop_video_playback(self):
        """Safely stop any running video playback and release resources."""
        self.video_playing = False
        try:
            if self.video_after_id:
                self.root.after_cancel(self.video_after_id)
                self.video_after_id = None
        except Exception:
            self.video_after_id = None
        try:
            if self.video_capture:
                try:
                    self.video_capture.release()
                except Exception:
                    pass
                self.video_capture = None
        except Exception:
            self.video_capture = None
        self.video_frame_image = None

    def create_back_button(self):
        """Create a back/home button (consistent size)."""
        back_btn = tk.Button(
            self.main_frame,
            text="🏠 Home",
            command=self.show_start_screen,
            bg=self.colors['danger'],
            fg=self.colors['white'],
            font=("Montserrat", 10, "bold"),
            width=10,
            padx=10,
            pady=6,
            relief=tk.FLAT,
            cursor="hand2",
            bd=0,
            activebackground=self.colors['danger'],
            activeforeground=self.colors['white']
        )
        back_btn.place(x=10, y=10)

    def uniform_button(self, parent, text, command, bg=None):
        """Create uniform buttons across the app."""
        bg = bg or self.colors['primary']
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=self.colors['white'],
            font=self.BUTTON_FONT,
            width=self.BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT,
            relief=tk.FLAT,
            cursor="hand2",
            bd=0,
            activebackground=bg,
            activeforeground=self.colors['white']
        )
        return btn

    def show_start_screen(self):
        """Display the initial start screen."""
        self.clear_screen()

        # Title
        title = tk.Label(
            self.main_frame,
            text="🎯 Interactive Hangman MCQ Game",
            font=("Montserrat", 28, "bold"),
            fg=self.colors['primary'],
            bg=self.colors['dark']
        )
        title.pack(pady=(40, 16))

        # Subtitle
        subtitle = tk.Label(
            self.main_frame,
            text="Test your knowledge across multiple subjects!",
            font=("Montserrat", 16),
            fg=self.colors['light'],
            bg=self.colors['dark']
        )
        subtitle.pack(pady=(0, 30))

        # Nickname input frame with rounded container
        input_container = tk.Frame(self.main_frame, bg=self.colors['panel'], relief=tk.FLAT, bd=0, padx=20, pady=20)
        input_container.pack(pady=10, ipadx=20, ipady=10)

        nickname_label = tk.Label(
            input_container,
            text="Enter your nickname:",
            font=("Montserrat", 18, "bold"),
            fg=self.colors['light'],
            bg=self.colors['panel']
        )
        nickname_label.pack(pady=(0, 8))

        self.nickname_entry = tk.Entry(
            input_container,
            font=("Montserrat", 16),
            width=30,
            justify='center',
            relief=tk.FLAT,
            bd=2,
            bg=self.colors['light'],
            fg=self.colors['dark']
        )
        self.nickname_entry.pack(pady=(0, 12), ipady=5)
        self.nickname_entry.bind('<Return>', lambda e: self.start_game())

        # Start button
        start_btn = self.uniform_button(input_container, "🚀 Start Game", self.start_game, bg=self.colors['secondary'])
        start_btn.pack(pady=10)

        # Focus on entry
        self.nickname_entry.focus()

    def start_game(self):
        """Process nickname and show welcome screen."""
        nickname = self.nickname_entry.get().strip()
        if not nickname:
            messagebox.showwarning("Warning", "Please enter your nickname!")
            return

        self.nickname = nickname
        # Play start sound
        self.play_sound('start')
        self.show_welcome_screen()

    def show_welcome_screen(self):
        """Show welcome screen with celebration animation."""
        self.clear_screen()
        self.create_back_button()

        # Welcome message
        welcome_msg = tk.Label(
            self.main_frame,
            text=f"🎉 Welcome, {self.nickname}!! 🎉",
            font=("Montserrat", 32, "bold"),
            fg=self.colors['secondary'],
            bg=self.colors['dark']
        )
        welcome_msg.pack(expand=True)

        # Celebration animation (simple text animation)
        self.animate_celebration()

        # Continue button (appears after animation)
        self.root.after(1200, self.show_continue_button)

    def animate_celebration(self):
        """Removed celebration animation (disabled)."""
        pass  # No celebration effect now


    def show_continue_button(self):
        """Show the continue button after (removed) celebration."""
        continue_btn = self.uniform_button(
            self.main_frame,
            "🎮 Let's Explore Hangman Game",   # Removed 🎮 emoji
            self.show_language_selection,
            bg=self.colors['primary']
        )
        continue_btn.config(width=30)  # Increased width
        continue_btn.pack(pady=20)


    def show_language_selection(self):
        """Display language selection screen."""
        self.clear_screen()
        self.create_back_button()

        # Title
        title = tk.Label(
            self.main_frame,
            text="📚 Choose Your Subject",
            font=("Montserrat", 28, "bold"),
            fg=self.colors['white'],
            bg=self.colors['dark']
        )
        title.pack(pady=(30, 20))

        # Language buttons frame
        lang_frame = tk.Frame(self.main_frame, bg=self.colors['dark'])
        lang_frame.pack(expand=True)

        languages = [
            ("🐍 Python", "Python"),
            ("🗃️ SQL", "SQL"),
            ("📊 Power BI", "Power BI"),
            ("📈 Tableau", "Tableau"),
            ("📉 Statistics", "Statistics")
        ]

        colors = [self.colors['primary'], self.colors['secondary'],
                  self.colors['warning'], self.colors['danger'], '#9b59b6']

        for i, (display_name, lang_name) in enumerate(languages):
            btn = self.uniform_button(lang_frame, display_name, lambda l=lang_name: self.select_language(l), bg=colors[i % len(colors)])
            btn.pack(pady=10)

    def select_language(self, language):
        """Select language and show level selection."""
        self.selected_language = language
        self.show_level_selection()

    def show_level_selection(self):
        """Display level selection screen."""
        self.clear_screen()
        self.create_back_button()

        # Title
        title = tk.Label(
            self.main_frame,
            text=f"🎯 {self.selected_language} - Choose Difficulty",
            font=("Montserrat", 26, "bold"),
            fg=self.colors['white'],
            bg=self.colors['dark']
        )
        title.pack(pady=(30, 20))

        # Level buttons
        levels = [
            ("🟢 Easy", "Easy", self.colors['secondary']),
            ("🟡 Intermediate", "Intermediate", self.colors['warning']),
            ("🔴 Extreme", "Extreme", self.colors['danger'])
        ]

        level_frame = tk.Frame(self.main_frame, bg=self.colors['dark'])
        level_frame.pack(expand=True)

        for display_name, level_name, color in levels:
            btn = self.uniform_button(level_frame, display_name, lambda l=level_name: self.select_level(l), bg=color)
            btn.pack(pady=10)

    def select_level(self, level):
        """Select level and start game."""
        self.selected_level = level
        self.questions = self.question_bank[self.selected_language][level].copy()
        random.shuffle(self.questions)
        self.current_question = 0
        self.score = 0
        self.wrong_answers = 0
        self.user_answers = []
        self.show_ready_screen()

    def show_ready_screen(self):
        """Show 'Let's go' screen briefly."""
        self.clear_screen()

        ready_msg = tk.Label(
            self.main_frame,
            text=f"🚀 Let's go, {self.nickname}!! 🚀",
            font=("Montserrat", 36, "bold"),
            fg=self.colors['secondary'],
            bg=self.colors['dark']
        )
        ready_msg.pack(expand=True)

        # Start first question after 800ms
        self.root.after(800, self.show_question)

    def show_question(self):
        """Display current MCQ question."""
        # Cancel any pending timer callback before rendering a new question
        try:
            if self.timer_after_id:
                self.root.after_cancel(self.timer_after_id)
            self.timer_after_id = None
        except Exception:
            self.timer_after_id = None

        if self.current_question >= len(self.questions):
            self.show_results()
            return

        self.clear_screen()
        self.create_back_button()

        question_data = self.questions[self.current_question]

        # Header with progress and score
        header_frame = tk.Frame(self.main_frame, bg=self.colors['dark'])
        header_frame.pack(fill=tk.X, pady=(0, 20))

        progress_text = f"Question {self.current_question + 1}/{len(self.questions)} | {self.selected_language} - {self.selected_level}"
        progress_label = tk.Label(
            header_frame,
            text=progress_text,
            font=("Montserrat", 14, "bold"),
            fg=self.colors['light'],
            bg=self.colors['dark']
        )
        progress_label.pack(side=tk.LEFT, padx=10)

        # Score label
        self.score_label = tk.Label(
            header_frame,
            text=f"Score: {self.score}",
            font=("Montserrat", 14, "bold"),
            fg=self.colors['secondary'],
            bg=self.colors['dark']
        )
        self.score_label.pack(side=tk.RIGHT, padx=10)

        # Main content frame
        content_frame = tk.Frame(self.main_frame, bg=self.colors['dark'])
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left side - Question and options
        question_frame = tk.Frame(content_frame, bg=self.colors['dark'])
        question_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))

        # Timer
        self.time_left = 15  # 15 seconds for each question
        self.timer_label = tk.Label(
            question_frame,
            text=f"⏰ {self.time_left}",
            font=("Montserrat", 24, "bold"),
            fg=self.colors['warning'],
            bg=self.colors['dark']
        )
        self.timer_label.pack(pady=(0, 16))

        # Question text container
        question_container = tk.Frame(question_frame, bg=self.colors['panel'], relief=tk.FLAT, bd=0, padx=15, pady=15)
        question_container.pack(fill=tk.X, pady=(0, 18))

        question_text = tk.Label(
            question_container,
            text=question_data["question"],
            font=("Montserrat", 16, "bold"),
            fg=self.colors['light'],
            bg=self.colors['panel'],
            wraplength=520,
            justify=tk.LEFT
        )
        question_text.pack()

        # Options
        self.selected_option = tk.IntVar()
        self.selected_option.set(-1)  # No option selected initially

        options_frame = tk.Frame(question_frame, bg=self.colors['dark'])
        options_frame.pack(fill=tk.X, pady=(0, 10))

        for i, option in enumerate(question_data["options"]):
            option_frame = tk.Frame(options_frame, bg=self.colors['dark'])
            option_frame.pack(fill=tk.X, pady=6)
            
            radio_btn = tk.Radiobutton(
                option_frame,
                text=f"{chr(65+i)}) {option}",
                variable=self.selected_option,
                value=i,
                font=("Montserrat", 14),
                fg=self.colors['light'],
                bg=self.colors['dark'],
                selectcolor=self.colors['panel'],
                activebackground=self.colors['dark'],
                activeforeground=self.colors['white'],
                wraplength=450,
                justify=tk.LEFT,
                anchor='w',
                indicatoron=1,
                relief=tk.FLAT
            )
            radio_btn.pack(anchor=tk.W)

        # Feedback label (for wrong attempts)
        self.feedback_label = tk.Label(question_frame, text="", font=("Montserrat", 14, "bold"),
                                       fg=self.colors['danger'], bg=self.colors['dark'])
        self.feedback_label.pack(pady=(6, 4))

        # Next button
        self.next_btn = self.uniform_button(question_frame, "Next Question ➡️", self.answer_question, bg=self.colors['primary'])
        self.next_btn.pack(pady=16)

        # Right side - Hangman drawing
        hangman_frame = tk.Frame(content_frame, bg=self.colors['dark'])
        hangman_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10,0))

        # Hangman canvas with container
        canvas_container = tk.Frame(hangman_frame, bg=self.colors['panel'], relief=tk.FLAT, bd=0, padx=10, pady=10)
        canvas_container.pack(pady=20)

        self.hangman_canvas = tk.Canvas(
            canvas_container,
            width=300,
            height=400,
            bg=self.colors['light'],
            highlightthickness=0,
            relief=tk.FLAT
        )
        self.hangman_canvas.pack()

        self.draw_hangman()

        # Start timer
        self.timer_running = True
        self.update_timer()

    def draw_hangman(self):
        """Draw hangman based on wrong answers."""
        canvas = self.hangman_canvas
        if not canvas:
            return

        canvas.delete("all")

        # Draw gallows
        canvas.create_rectangle(50, 350, 250, 370, fill="#795548", outline="#5D4037", width=2)
        canvas.create_rectangle(100, 50, 120, 350, fill="#795548", outline="#5D4037", width=2)
        canvas.create_rectangle(100, 50, 200, 70, fill="#795548", outline="#5D4037", width=2)
        canvas.create_rectangle(180, 70, 185, 100, fill="#795548", outline="#5D4037", width=2)

        # Draw hangman parts according to wrong_answers
        if self.wrong_answers >= 1:
            canvas.create_oval(160, 100, 200, 140, outline="#333333", width=4)  # Head
        if self.wrong_answers >= 2:
            canvas.create_line(180, 140, 180, 250, fill="#333333", width=4)  # Body
        if self.wrong_answers >= 3:
            canvas.create_line(180, 170, 220, 200, fill="#333333", width=4)  # Right arm
        if self.wrong_answers >= 4:
            canvas.create_line(180, 170, 140, 200, fill="#333333", width=4)  # Left arm
        if self.wrong_answers >= 5:
            canvas.create_line(180, 250, 220, 300, fill="#333333", width=4)  # Right leg
        if self.wrong_answers >= 6:
            canvas.create_line(180, 250, 140, 300, fill="#333333", width=4)  # Left leg
            # X eyes and sad mouth for game over
            canvas.create_line(168, 115, 175, 122, fill="red", width=3)
            canvas.create_line(175, 115, 168, 122, fill="red", width=3)
            canvas.create_line(185, 115, 192, 122, fill="red", width=3)
            canvas.create_line(192, 115, 185, 122, fill="red", width=3)
            canvas.create_arc(165, 125, 195, 135, start=0, extent=-180, outline="red", width=3, style=tk.ARC)

    def update_timer(self):
        """Update the countdown timer (safe cancelable scheduling)."""
        # If timer not running, don't schedule
        if not self.timer_running:
            return

        if self.time_left > 0:
            # Last 5 seconds: warning look + alert sound per second
            if self.time_left <= 5:
                self.timer_label.config(text=f"⏰ {self.time_left}", fg=self.colors['danger'], font=("Montserrat", 32, "bold"))
                # play alert sound once per second
                self.play_sound('countdown')
                # pulsing effect
                self.pulse_timer()
            else:
                self.timer_label.config(text=f"⏰ {self.time_left}", fg=self.colors['warning'], font=("Montserrat", 24, "bold"))

            # decrement and schedule next
            self.time_left -= 1
            self.timer_after_id = self.root.after(1000, self.update_timer)
        else:
            # Time's up -> increment hangman body once (per your request)
            self.timer_running = False
            self.timer_after_id = None
            # record unanswered (timeout)
            self.user_answers.append(-1)
            # Only timeouts increase the hangman body
            self.wrong_answers += 1
            self.draw_hangman()
            # Show time's up overlay and then show correct answer and move next
            self.show_timeout_message()

    def pulse_timer(self):
        """Create pulsing effect for timer in final seconds."""
        if not (hasattr(self, 'timer_label') and self.timer_label and self.timer_label.winfo_exists()):
            return
        try:
            self.timer_label.config(font=("Montserrat", 28, "bold"))
            self.root.after(250, lambda: self.timer_label.config(font=("Montserrat", 32, "bold")))
        except Exception:
            pass

    def show_timeout_message(self):
        """Show timeout message briefly then show correct answer and auto-move."""
        overlay = tk.Frame(self.main_frame, bg=self.colors['danger'])
        overlay.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.45)

        timeout_label = tk.Label(
            overlay,
            text="⏰ TIME'S UP! ⏰",
            font=("Montserrat", 28, "bold"),
            fg=self.colors['white'],
            bg=self.colors['danger']
        )
        timeout_label.pack(expand=True, pady=20)

        # play crying sound for timeups
        self.play_sound('crying')

        # After a short pause show correct answer (reuses show_correct_answer but without touching wrong_answers further)
        self.root.after(1000, lambda: [overlay.destroy(), self.show_correct_answer(autonext=True)])

    def answer_question(self):
        """Process the selected answer.

        NOTE: changed behavior per request:
         - If the selected option is correct -> stop timer, record answer, award points, move next.
         - If selected option is wrong -> DO NOT stop timer; provide transient feedback "Incorrect - try again!"
           and let user change selection within remaining time. Do NOT increment hangman on wrong selections.
         - Timeouts still increment hangman and auto-move.
        """
        selected = self.selected_option.get()
        if selected == -1:
            messagebox.showwarning("Warning", "Please select an answer!")
            return

        question_data = self.questions[self.current_question]
        correct_answer = question_data["correct"]

        if selected == correct_answer:
            # Correct answer: stop timer, reward, record and move on
            self.timer_running = False
            try:
                if self.timer_after_id:
                    self.root.after_cancel(self.timer_after_id)
                    self.timer_after_id = None
            except Exception:
                self.timer_after_id = None

            self.score += 2
            self.play_sound('coin')
            self.user_answers.append(selected)
            # Clear any feedback if present
            if self.feedback_label:
                self.feedback_label.config(text="")
            # Move to next question
            self.next_question()
        else:
            # Wrong selection: do NOT stop the timer; let user try again until time runs out.
            # Show transient feedback and play a small alert sound.
            if self.feedback_label:
                self.feedback_label.config(text="Incorrect — try again!")
                # clear the feedback after a short time so it doesn't clutter UI
                self.root.after(1200, lambda: self.feedback_label.config(text=""))
            # play a small alert sound indicating wrong attempt (no hangman increment)
            self.play_sound('wrong')
            # Do not append to user_answers here; wait for correct or timeout

    def show_correct_answer(self, autonext=False):
        """Briefly show the correct answer before proceeding."""

        question_data = self.questions[self.current_question]
        correct_option_text = question_data["options"][question_data["correct"]]

        overlay = tk.Frame(self.main_frame, bg=self.colors['panel'])
        overlay.place(x=0, y=0, relwidth=1, relheight=1)

        correct_label = tk.Label(
            overlay,
            text=f"Correct Answer: {correct_option_text}",
            font=("Montserrat", 20, "bold"),
            fg=self.colors['secondary'],
            bg=self.colors['panel'],
            padx=30,
            pady=20,
            relief=tk.FLAT
        )
        correct_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        def cleanup_and_next():
            try:
                overlay.destroy()
            except Exception:
                pass
            # record correct or timeout: if timeout we already appended -1; if user eventually answered correct,
            # user_answers already contains the correct index. For consistency, when showing correct answer due to timeout,
            # we leave user_answers as-is (it contains -1).
            self.next_question()

        self.root.after(1400, cleanup_and_next)

    def next_question(self):
        """Move to next question (reset timer properly)."""
        self.current_question += 1

        # update score label if exists
        if self.score_label:
            self.score_label.config(text=f"Score: {self.score}")

        # If game finished go to results
        if self.current_question >= len(self.questions):
            try:
                if self.timer_after_id:
                    self.root.after_cancel(self.timer_after_id)
                    self.timer_after_id = None
            except Exception:
                self.timer_after_id = None
            self.show_results()
            return

        # Small delay to let UI breathe (keeps consistent)
        self.root.after(300, self.show_question)

    def show_results(self):
        """Show final results screen."""
        try:
            if self.timer_after_id:
                self.root.after_cancel(self.timer_after_id)
                self.timer_after_id = None
        except Exception:
            self.timer_after_id = None

        # Stop any video playback that might be running
        self.stop_video_playback()

        self.clear_screen()
        self.create_back_button()

        total_questions = len(self.questions)
        correct_answers = self.score // 2

        results_frame = tk.Frame(self.main_frame, bg=self.colors['dark'])
        results_frame.pack(expand=True)

        title = tk.Label(
            results_frame,
            text="🎯 Game Results",
            font=("Montserrat", 32, "bold"),
            fg=self.colors['white'],
            bg=self.colors['dark']
        )
        title.pack(pady=(0, 20))

        content_frame = tk.Frame(results_frame, bg=self.colors['dark'])
        content_frame.pack()

        stats_frame = tk.Frame(content_frame, bg=self.colors['dark'])
        stats_frame.pack(side=tk.LEFT, padx=(0, 40))

        player_info = tk.Label(
            stats_frame,
            text=f"Player: {self.nickname}",
            font=("Montserrat", 18, "bold"),
            fg=self.colors['light'],
            bg=self.colors['dark']
        )
        player_info.pack(pady=5)

        subject_info = tk.Label(
            stats_frame,
            text=f"Subject: {self.selected_language} ({self.selected_level})",
            font=("Montserrat", 16),
            fg=self.colors['light'],
            bg=self.colors['dark']
        )
        subject_info.pack(pady=5)

        score_display = tk.Label(
            stats_frame,
            text=f"Final Score: {self.score} points",
            font=("Montserrat", 24, "bold"),
            fg=self.colors['secondary'],
            bg=self.colors['dark']
        )
        score_display.pack(pady=20)

        stats_text = f"""
✅ Correct Answers: {correct_answers}/{total_questions}
❌ Wrong (timeouts): {self.wrong_answers}
📈 Accuracy: {(correct_answers/total_questions)*100:.1f}%
        """

        stats_label = tk.Label(
            stats_frame,
            text=stats_text,
            font=("Montserrat", 14),
            fg=self.colors['light'],
            bg=self.colors['dark'],
            justify=tk.LEFT
        )
        stats_label.pack(pady=10)

        visual_frame = tk.Frame(content_frame, bg=self.colors['dark'])
        visual_frame.pack(side=tk.RIGHT)

        final_canvas = tk.Canvas(
            visual_frame,
            width=300,
            height=400,
            bg=self.colors['light'],
            highlightthickness=0
        )
        final_canvas.pack()

        # set hangman_canvas and draw
        self.hangman_canvas = final_canvas
        self.draw_hangman()

        # Determine outcome
        if correct_answers == total_questions:
            # Perfect
            self.play_sound('celebration')
            celebration_text = tk.Label(
                visual_frame,
                text="🎉 PERFECT SCORE! 🎉",
                font=("Montserrat", 18, "bold"),
                fg=self.colors['secondary'],
                bg=self.colors['dark']
            )
            celebration_text.pack(pady=10)
            # Attempt to play video inside this final canvas; fallback to existing animation if video can't play
            self.show_celebration_animation(final_canvas)
        elif self.wrong_answers >= 6:
            # Lost
            self.play_sound('crying')
            game_over_text = tk.Label(
                visual_frame,
                text="💀 Game Over! 💀",
                font=("Montserrat", 18, "bold"),
                fg=self.colors['danger'],
                bg=self.colors['dark']
            )
            game_over_text.pack(pady=10)
            self.show_crying_animation(final_canvas)
        else:
            # Mixed: play coin sounds for correct answers
            for i in range(correct_answers):
                self.root.after(i * 200, lambda: self.play_sound('coin'))

        # Action buttons
        button_frame = tk.Frame(results_frame, bg=self.colors['dark'])
        button_frame.pack(pady=30)

        play_again_btn = self.uniform_button(button_frame, "🔄 Play Again", self.show_language_selection, bg=self.colors['primary'])
        play_again_btn.pack(side=tk.LEFT, padx=10)

        home_btn = self.uniform_button(button_frame, "🏠 Home", self.show_start_screen, bg=self.colors['secondary'])
        home_btn.pack(side=tk.LEFT, padx=10)

    def show_celebration_animation(self, canvas):
        """Show celebration animation on canvas.

        NEW: Try to play an mp4 video inside the given canvas using OpenCV + Pillow if available.
        If libraries or the file are missing, fallback to a decorative confetti and star drawing.
        The video will LOOP continuously until the screen changes or stop_video_playback() is called.
        """
        # Clear any previous video
        self.stop_video_playback()

        # Decorative confetti always drawn under the video/fallback
        for i in range(10):
            x = random.randint(50, 250)
            y = random.randint(50, 300)
            canvas.create_text(x, y, text="✨", font=("Arial", 16), fill="gold")

        # If OpenCV & Pillow are available and the file exists, attempt to play the video
        video_path = self.default_video_path
        if OPENCV_AVAILABLE and video_path.exists():
            try:
                cap = cv2.VideoCapture(str(video_path))
                if not cap or not cap.isOpened():
                    try:
                        cap.release()
                    except Exception:
                        pass
                    raise RuntimeError("Cannot open video file")

                # Store capture and start loop via after; do not block
                self.video_capture = cap
                self.video_playing = True

                # compute fps and delay
                fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
                delay_ms = int(1000 / fps) if fps > 0 else 42

                # precompute canvas size
                canvas_w = int(canvas.cget('width') or 300)
                canvas_h = int(canvas.cget('height') or 400)

                # Center coordinates
                center_x = canvas_w // 2
                center_y = canvas_h // 2

                # create image item placeholder
                img_item = canvas.create_image(center_x, center_y, image=None)

                def stream_frame():
                    # stop condition
                    if not self.video_playing or self.video_capture is None:
                        try:
                            canvas.delete(img_item)
                        except Exception:
                            pass
                        return

                    ret, frame = self.video_capture.read()
                    # If frame not read (EOF or error), attempt to loop by seeking to frame 0 and continue
                    if not ret:
                        try:
                            # Try seek to beginning
                            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                            ret, frame = self.video_capture.read()
                        except Exception:
                            ret = False

                        if not ret:
                            # If still failing, fallback to a static celebratory star and stop playback
                            self.stop_video_playback()
                            try:
                                canvas.create_text(center_x, center_y, text="⭐", font=("Arial", 56), tags="celebration_star")
                            except Exception:
                                pass
                            return

                    # Convert BGR -> RGB
                    try:
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        img = Image.fromarray(frame_rgb)
                        # Resize to fit canvas while maintaining aspect ratio
                        img.thumbnail((canvas_w - 10, canvas_h - 10), Image.LANCZOS)
                        photo = ImageTk.PhotoImage(img)
                        # Keep reference to avoid GC
                        self.video_frame_image = photo
                        # Update canvas image
                        try:
                            canvas.itemconfigure(img_item, image=photo)
                        except Exception:
                            # in rare cases itemconfigure may fail, recreate image
                            try:
                                canvas.delete(img_item)
                            except Exception:
                                pass
                            img_item_local = canvas.create_image(center_x, center_y, image=photo)
                        # Schedule next frame
                        self.video_after_id = self.root.after(delay_ms, stream_frame)
                    except Exception:
                        # On any error during frame processing, fallback to static star and stop playback.
                        self.stop_video_playback()
                        try:
                            canvas.create_text(center_x, center_y, text="⭐", font=("Arial", 56), tags="celebration_star")
                        except Exception:
                            pass
                        return

                # launch streaming loop
                stream_frame()
                return
            except Exception:
                # any exception falls through to fallback animation
                self.stop_video_playback()

        # Fallback decorative celebration (if video can't be played)
        # Draw a large celebratory star and a simple moving effect
        try:
            canvas.create_text(150, 180, text="⭐", font=("Arial", 56), tags="celebration_star")
        except Exception:
            pass

        def animate_dance(count=0):
            if count < 10:
                canvas.delete("hangman_parts")
                offset = 2 if count % 2 == 0 else -2
                if self.wrong_answers >= 1:
                    canvas.create_oval(160+offset, 100, 200+offset, 140, outline="green", width=3, tags="hangman_parts")
                self.root.after(200, lambda: animate_dance(count + 1))

        animate_dance()

    def show_crying_animation(self, canvas):
        """Show crying animation for hangman."""
        for i in range(5):
            x = random.randint(170, 190)
            y = random.randint(140, 200)
            canvas.create_text(x, y, text="💧", font=("Arial", 12), fill="blue")

        def add_tears(count=0):
            if count < 8:
                x = random.randint(165, 195)
                y = 140 + count * 15
                canvas.create_text(x, y, text="💧", font=("Arial", 10), fill="blue")
                self.root.after(300, lambda: add_tears(count + 1))

        add_tears()

    def run(self):
        """Start the game application."""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"1000x700+{x}+{y}")
        self.root.mainloop()

if __name__ == "__main__":
    try:
        game = HangmanMCQGame()
        game.run()
    except Exception as e:
        print(f"Error starting game: {e}")
        print("Make sure you have pygame installed: pip install pygame")
        print("If you want video playback, install opencv-python and pillow: pip install opencv-python pillow")
        print("If numpy is missing for beep generation, the game will run without fallback sounds.")

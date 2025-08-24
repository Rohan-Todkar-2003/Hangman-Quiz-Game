# 🎮 Gameplay Guide

## How to Play

### Game Overview
Interactive Hangman MCQ Game combines the classic hangman concept with multiple-choice questions across programming and data science subjects. Answer questions correctly to avoid building the hangman!

### Getting Started

1. **Launch the Game**
   ```bash
   python hangman_game.py
   ```

2. **Enter Your Nickname**
   - Type your preferred nickname
   - Press Enter or click "Start Game"

3. **Choose Your Subject**
   - 🐍 Python: Programming concepts and syntax
   - 🗃️ SQL: Database queries and management
   - 📊 Power BI: Business intelligence and data visualization
   - 📈 Tableau: Advanced data visualization techniques
   - 📉 Statistics: Mathematical statistics and data analysis

4. **Select Difficulty Level**
   - 🟢 **Easy**: Basic concepts, beginner-friendly
   - 🟡 **Intermediate**: Applied knowledge, moderate difficulty
   - 🔴 **Extreme**: Advanced topics, expert-level challenges

### Question Mechanics

#### Timer System
- Each question has a **15-second countdown**
- Timer appears in yellow initially
- **Last 5 seconds**: Timer turns red and pulses with alert sounds
- **Timeout**: Automatically moves to next question

#### Answer System
- **Correct Answer**: 
  - ✅ +2 points awarded
  - 🎵 Coin sound plays
  - Immediately moves to next question
  
- **Incorrect Selection**:
  - ❌ "Incorrect - try again!" message appears
  - 🔊 Wrong answer sound plays
  - Timer continues running - you can try again!
  - **No hangman penalty** for wrong attempts

- **Timeout (No Answer)**:
  - ⏰ "TIME'S UP!" message shown
  - 😢 Crying sound plays
  - **Hangman body part added**
  - Shows correct answer briefly
  - Moves to next question

### Hangman Progression

The hangman is drawn progressively with each **timeout** (not wrong answers):

1. **1st Timeout**: Head
2. **2nd Timeout**: Body
3. **3rd Timeout**: Right arm
4. **4th Timeout**: Left arm
5. **5th Timeout**: Right leg
6. **6th Timeout**: Left leg + X eyes + sad mouth → **Game Over**

### Scoring System

- **Correct Answer**: +2 points
- **Wrong Attempt**: No point penalty (can retry)
- **Timeout**: No points gained
- **Maximum Possible Score**: Number of questions × 2

### Game Endings

#### Perfect Score (All Correct)
- 🎉 "PERFECT SCORE!" message
- 🎵 Celebration music
- 🎬 Dancing stick figure video (if video support installed)
- ✨ Confetti animation

#### Partial Success
- 📊 Score breakdown shown
- 💰 Coin sounds play for each correct answer
- 📈 Accuracy percentage displayed

#### Game Over (6 Timeouts)
- 💀 "Game Over!" message
- 😢 Crying sounds and tear animation
- 📊 Final statistics displayed

## Strategy Tips

### Time Management
- **Read Quickly**: Scan the question and options fast
- **Eliminate Obviously Wrong**: Cross out impossible answers mentally
- **Don't Panic**: You have 15 seconds - use them wisely
- **Guess if Needed**: Better to guess than timeout

### Subject-Specific Tips

#### 🐍 Python
- **Easy**: Focus on syntax and basic concepts
- **Intermediate**: Understand data types and methods
- **Extreme**: Know advanced features like decorators and GIL

#### 🗃️ SQL
- **Easy**: Basic SELECT, WHERE, INSERT commands
- **Intermediate**: JOINs, aggregate functions, constraints
- **Extreme**: Window functions, CTEs, advanced optimization

#### 📊 Power BI
- **Easy**: Basic interface and data import concepts
- **Intermediate**: DAX functions and data modeling
- **Extreme**: Advanced features like DirectQuery and composite models

#### 📈 Tableau
- **Easy**: Basic chart creation and data connection
- **Intermediate**: Parameters, calculations, dashboard design
- **Extreme**: Table calculations, order of operations, advanced analytics

#### 📉 Statistics
- **Easy**: Mean, median, mode, basic probability
- **Intermediate**: Correlation, hypothesis testing, confidence intervals
- **Extreme**: Advanced techniques like ANOVA, Bayesian methods

## Game Controls

### Keyboard Shortcuts
- **Enter**: Submit answer (when option selected)
- **Numbers 1-4**: Quick select options A-D (if implemented)
- **Escape**: Return to main menu (if implemented)

### Mouse Controls
- **Click**: Select radio button options
- **Click "Next Question"**: Submit selected answer
- **Click "Home"**: Return to start screen anytime

## Audio Features

### Sound Effects
- 🎵 **Start Sound**: Game initialization
- ⏰ **Countdown**: Ticking in final 5 seconds
- 💰 **Coin**: Correct answer reward
- ❌ **Wrong**: Incorrect attempt feedback
- 🎉 **Celebration**: Perfect score achievement
- 😢 **Crying**: Game over or timeout

### Audio Troubleshooting
- If no sound: Check pygame installation
- Volume issues: Adjust system volume
- Sound conflicts: Close other audio applications

## Performance Tips

### For Smooth Gameplay
- Close unnecessary applications
- Ensure stable system performance
- Use wired headphones for best audio experience

### For Slower Systems
- Skip video extras during installation
- Use basic installation without OpenCV/Pillow
- Close browser and other memory-intensive apps

## Accessibility

### Visual
- High contrast color scheme
- Large, readable fonts
- Clear visual feedback

### Audio
- Multiple audio cues for different events
- Visual timer backup for audio-impaired users

### Motor
- Large click targets
- Keyboard shortcuts available
- No time-critical precise clicking required

## Game Modes (Current)

### Single Player
- Personal challenge mode
- Track your own progress
- Compete against your previous scores

### Practice Mode Tips
- Start with "Easy" difficulty in your strongest subject
- Progress gradually through difficulty levels
- Review questions you got wrong
- Time yourself to improve speed

## Advanced Features

### Video Celebrations
- Requires opencv-python and Pillow
- Plays MP4 video on perfect scores
- Loops continuously during results screen
- Gracefully falls back to static animation if unavailable

### Sound System
- Dynamic beep generation if audio files missing
- Multiple fallback layers for compatibility
- No crashes if audio hardware unavailable

## Future Enhancements (Planned)

- **Custom Questions**: Import your own question sets
- **Multiplayer**: Compete with friends online
- **Achievements**: Unlock badges and rewards
- **Leaderboards**: Global and local high scores
- **More Subjects**: JavaScript, R, Machine Learning topics
- **Mobile Version**: Touch-friendly interface

## Getting Better at the Game

### Study Resources
- Review the subject matter between games
- Practice coding/querying in real environments
- Use official documentation for each technology
- Join online communities for each subject

### Practice Strategies
- Play different subjects to broaden knowledge
- Challenge yourself with higher difficulty levels
- Focus on speed without sacrificing accuracy
- Learn from the correct answers shown after timeouts

## Feedback and Suggestions

We welcome feedback to improve the game:
- Submit issues on GitHub for bugs
- Suggest new questions or subjects
- Report performance problems
- Share ideas for new features

Enjoy mastering your programming and data science knowledge through this interactive challenge!

# Quiz Builder - Offline Timed Quiz System 🎓

A complete quiz builder and live exam delivery system designed for educators. Build quizzes with an intuitive GUI, launch them as live timed exams, and automatically collect student results - all with beautiful multilingual support.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

## ✨ Features

### 📝 Quiz Builder (Tkinter GUI)
- **Visual Quiz Creation**: Intuitive drag-and-drop interface
- **Multiple Question Types**: 
  - Multiple Choice (Single/Multiple answers)
  - True/False
  - Short Answer
  - Paragraph/Essay
- **Quiz Properties**:
  - Quiz title and name
  - Mandatory student full-name field (optional)
  - Global countdown timer
  - Start and end messages
  - Question shuffling (optional)
  - Per-question scoring weights
- **Quiz Management**:
  - Create, edit, delete quizzes
  - Preview quiz before launching
  - Save quizzes locally as JSON files

### Student Interface (Web)
- **Kid-Friendly Design**: Clean, colorful, responsive interface
- **Server-Side Timer**: Authoritative countdown timer synced with server
- **Auto-Submit**: Automatically submits when time expires
- **Time Warning**: Visual and animated warnings as time runs low
- **Early Submission**: Students can submit early with confirmation
- **No Cheating**: 
  - One submission per device/session
  - Server-side validation
  - Session-based tracking prevents refresh/retake

### Results & Analytics
- **Automatic Export**: Results saved automatically on submission
- **Structured Storage**: One folder per quiz in `results/` directory
- **Dual Format Export**:
  - JSON: Complete detailed results with all answers
  - CSV: Tabular format for easy analysis in Excel/Sheets
- **Comprehensive Data**:
  - Student name and timestamp
  - Score (points earned, total, percentage)
  - Per-question answers and correctness
  - Session tracking

### Technical Features
- **Offline-First**: Works completely offline (except when sharing via ngrok)
- **Automatic Server Launch**: Click "Launch Quiz" to start Flask server and ngrok
- **Public URL Sharing**: Automatic ngrok tunnel for sharing with students
- **Graceful Shutdown**: Clean server shutdown with resource cleanup
- **Error Handling**: Comprehensive error handling and logging
- **Windows Executable**: Build as single .exe for easy distribution

## Installation

### Option 1: Automatic Installer (Recommended for End Users)

**The easiest way to install - just download one file!**

1. **Download** the installer:
   - Download `install.bat` from this repository
   - Or right-click and save: [Direct Download](../../raw/main/install.bat)

2. **Run** the installer:
   - Double-click `install.bat`
   - Enter the GitHub repository URL when prompted:
     ```
     https://github.com/YOUR_USERNAME/quiz-builder
     ```
   - Wait for automatic installation (clones repo, installs Python packages, creates folders)

3. **Launch** the app:
   - The installer will ask if you want to launch now
   - Or later: double-click `start_quiz_builder.bat` in the created folder

📖 **[Complete Installation Guide](INSTALL_INSTRUCTIONS.md)** - Troubleshooting, prerequisites, and more

---

### Option 2: Manual Installation (For Developers)

**If you prefer manual control:**

1. **Clone or Download** this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/quiz-builder
   cd quiz-builder
   ```

2. **Run Setup Script**:
   ```bash
   # Windows (automated)
   setup.bat
   
   # Or manually:
   python -m venv venv_win
   venv_win\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Launch the Application**:
   ```bash
   # Windows (one-click)
   start_quiz_builder.bat
   
   # Or manually:
   python main.py
   ```

---

### Option 3: Bootstrap Installer (Legacy)

```bash
python bootstrap.py
```

This will check Python, install dependencies, set up ngrok, and optionally build an executable.

3. **Manual Setup** (if bootstrap fails):
   ```bash
   # Install Python 3.8+ if not installed
   # Download from: https://www.python.org/downloads/
   
   # Activate virtual environment (if using venv)
   # Windows PowerShell:
   venv\Scripts\Activate.ps1
   # Windows CMD:
   venv\Scripts\activate.bat
   
   # Install dependencies
   pip install -r requirements.txt
   ```

### Manual Installation Steps

1. **Python Requirements**:
   - Python 3.8 or higher
   - pip package manager

2. **Install Dependencies**:
   ```bash
   pip install flask==3.0.0 pyngrok==6.0.0 pyinstaller==6.3.0
   ```

3. **Configure Ngrok** (Optional but Recommended):
   - Sign up for free at https://ngrok.com/
   - Get your auth token from https://dashboard.ngrok.com/get-started/your-authtoken
   - Set environment variable:
     ```powershell
     # Windows PowerShell
     $env:NGROK_AUTH_TOKEN = "your_token_here"
     # Or set permanently:
     [System.Environment]::SetEnvironmentVariable('NGROK_AUTH_TOKEN', 'your_token_here', 'User')
     ```
   - Without token, ngrok works but with 2-hour session limits

4. **Build Executable** (Optional):
   ```bash
   python build.py
   ```
   Executable will be in `dist/QuizBuilder.exe`

## Usage

### Creating a Quiz

1. **Launch the Application**:
   ```bash
   python gui/main.py
   ```
   Or double-click `dist/QuizBuilder.exe` if built

2. **Create New Quiz**:
   - Click "File" → "New Quiz" or click "New" button
   - Enter a quiz name (used for filename)
   - Set quiz properties:
     - Quiz title (displayed to students)
     - Timer duration (minutes)
     - Start/end messages
     - Enable question shuffling if desired

3. **Add Questions**:
   - Click "Add Question"
   - Select question type
   - Enter question text
   - Set points/weight
   - Add options for multiple choice
   - Set correct answer(s)
   - Click "Save"

4. **Edit Questions**:
   - Select question in list
   - Click "Edit Question"
   - Modify and save
   - Use "Move Up/Down" to reorder

5. **Preview Quiz**:
   - Click "Preview" to see quiz overview

6. **Save Quiz**:
   - Click "Save Quiz" (or it auto-saves on launch)
   - Quiz saved to `data/<quiz_name>.json`

### Launching a Quiz

1. **Launch Quiz**:
   - Click "Launch Quiz" button
   - Wait for server to start (2-3 seconds)
   - A dialog will show the public URL
   - URL is automatically copied to clipboard
   - Browser opens automatically

2. **Share with Students**:
   - Share the public URL (ngrok link)
   - Students access via any device with web browser
   - No installation needed for students

3. **Monitor Quiz**:
   - Status bar shows "Quiz launched - Server running"
   - Quiz editing is locked while running
   - Results appear in real-time in `results/` folder

4. **Stop Server**:
   - Close the application to stop server
   - Or close ngrok tunnel manually if needed

### Taking a Quiz (Student View)

1. **Access Quiz**:
   - Open the shared URL in any web browser
   - Works on computers, tablets, phones

2. **Start Quiz**:
   - Read start message
   - Enter full name (required if enabled)
   - Click "Start Quiz"

3. **Answer Questions**:
   - Timer visible at top (synced with server)
   - Answer all questions
   - Can submit early or wait for auto-submit

4. **Timer Warnings**:
   - Yellow warning at 5 minutes remaining
   - Red pulsing at 1 minute remaining
   - Auto-submits at 0 seconds

5. **Submit**:
   - Click "Submit Quiz" when done
   - Or wait for auto-submit when time expires
   - Confirmation shown with score (if auto-grading enabled)

### Viewing Results

1. **Results Location**:
   - `results/<quiz_name>/` folder
   - One folder per quiz

2. **File Formats**:
   - **JSON**: `StudentName_Timestamp.json`
     - Complete detailed data
     - All answers, scores, timestamps
   - **CSV**: `<quiz_name>_results.csv`
     - Tabular format
     - Easy to open in Excel/Google Sheets
     - One row per submission

3. **Export Results**:
   - Open CSV in Excel/Sheets for analysis
   - Filter by score, student, date
   - Calculate averages, distributions

## Project Structure

```
quiz/
├── gui/                      # Tkinter GUI application
│   ├── __init__.py
│   ├── main.py              # Main entry point
│   ├── quiz_builder.py      # Main GUI application
│   └── quiz_manager.py      # Quiz data management
├── server/                   # Flask server
│   ├── __init__.py
│   ├── app.py               # Main Flask app
│   └── utils.py             # Utilities (logging, validation)
├── static/                   # Web assets
│   └── css/
│       └── style.css        # Student interface styles
├── templates/                # HTML templates
│   ├── index.html           # Student quiz interface
│   └── error.html           # Error page
├── data/                     # Quiz data storage
│   └── *.json               # Quiz files (auto-created)
├── results/                  # Results storage
│   └── <quiz_name>/         # Per-quiz result folders
│       ├── *.json           # Individual submissions
│       └── *_results.csv    # Aggregated results
├── logs/                     # Application logs (auto-created)
├── build.py                  # PyInstaller build script
├── bootstrap.py              # Bootstrap installer
├── run_server.py             # Server launcher with ngrok
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Configuration

### Environment Variables

- `NGROK_AUTH_TOKEN`: Your ngrok authentication token (recommended)
  - Without this, ngrok has 2-hour session limits
  - Get free token at: https://dashboard.ngrok.com/get-started/your-authtoken

### Quiz File Format

Quizzes are stored as JSON in `data/<quiz_name>.json`:

```json
{
  "name": "math_quiz_2024",
  "title": "Math Quiz - Chapter 5",
  "require_full_name": true,
  "timer_minutes": 30,
  "start_message": "Welcome! Read all questions carefully.",
  "end_message": "Thank you for completing the quiz!",
  "shuffle_questions": false,
  "questions": [
    {
      "type": "multiple_choice_single",
      "text": "What is 2 + 2?",
      "weight": 1,
      "options": ["3", "4", "5", "6"],
      "correct_answer": "4"
    }
  ]
}
```

## Troubleshooting

### Server Won't Start
- Check if port 5000 is already in use
- Ensure Flask is installed: `pip install flask`
- Check logs in `logs/` directory

### Ngrok Not Working
- Verify ngrok token is set: `echo $env:NGROK_AUTH_TOKEN` (PowerShell)
- Check internet connection
- Without token, ngrok works but with limitations
- Alternative: Use local network IP for LAN-only access

### Results Not Saving
- Check `results/` directory exists and is writable
- Check disk space
- Review logs for error messages
- Ensure quiz name doesn't contain invalid characters

### Timer Not Syncing
- Check browser console for errors
- Ensure server is running
- Try refreshing page (but don't refresh after starting quiz - it will reset)

### Build Errors
- Ensure PyInstaller is installed: `pip install pyinstaller`
- Check Python version (3.8+)
- Try running from command line to see detailed errors

## Security Considerations

- **Local Use Only**: Designed for offline/local network use
- **No Authentication**: Quiz URLs are public - don't share sensitive data
- **Session Tracking**: Prevents same device from submitting twice
- **Server-Side Validation**: All validations enforced on server
- **No Data Collection**: All data stored locally on creator's machine

## Limitations

- Ngrok free tier has limitations (2-hour sessions without auth token)
- Maximum concurrent students depends on local network/server capacity
- No built-in user management or authentication
- Results only stored locally (no cloud sync)

## Future Enhancements

Potential improvements (not implemented):
- Cloud result storage
- Student authentication
- Quiz templates and sharing
- Advanced analytics dashboard
- Mobile app for quiz creation
- Offline mode for students

## License

This project is provided as-is for educational use. Modify and distribute freely.

## Support

For issues or questions:
1. Check logs in `logs/` directory
2. Review error messages in GUI/console
3. Verify all dependencies are installed
4. Ensure Python version is 3.8+

## Credits

Built with:
- Python 3
- Tkinter (GUI)
- Flask (Web server)
- ngrok (Tunneling)
- PyInstaller (Packaging)

---

**Designed for Educators, Built for Children**


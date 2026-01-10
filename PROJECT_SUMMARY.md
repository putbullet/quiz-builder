# Project Summary: Offline Quiz Builder + Live Timed Exam Server

## Overview

A complete, production-ready quiz builder and live exam delivery system designed for non-technical educators teaching young children. The system consists of two tightly integrated parts:

1. **Desktop GUI Application** (Tkinter) - For quiz creation and management
2. **Web Server** (Flask + ngrok) - For student quiz delivery

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    QUIZ BUILDER GUI                     │
│                  (Tkinter Desktop App)                  │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Quiz Manager │  │ Quiz Builder │  │ Question     │ │
│  │ (Data CRUD)  │  │ (UI Layer)   │  │ Editor       │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
                          │ Save Quiz
                          ▼
                  ┌───────────────┐
                  │ data/*.json   │
                  │ (Quiz Files)  │
                  └───────────────┘
                          │
                          │ Launch Quiz
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    FLASK SERVER                         │
│              (run_server.py + app.py)                   │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Quiz Loader  │  │ Session      │  │ Timer        │ │
│  │ Validator    │  │ Manager      │  │ Sync         │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
                          │ ngrok
                          ▼
              ┌───────────────────────┐
              │   Public URL (ngrok)  │
              │   https://xxx.ngrok.io│
              └───────────────────────┘
                          │
                          │ HTTP/HTTPS
                          ▼
┌─────────────────────────────────────────────────────────┐
│               STUDENT WEB INTERFACE                     │
│          (HTML/CSS/JS - Kid-Friendly UI)                │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Name Entry   │  │ Quiz Display │  │ Timer        │ │
│  │ Question UI  │  │ Auto-Submit  │  │ Results      │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
                          │ Submit Quiz
                          ▼
              ┌───────────────────────┐
              │   Score Calculator    │
              │   Results Exporter    │
              └───────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  RESULTS STORAGE                        │
│                                                         │
│  results/<quiz_name>/                                   │
│  ├── <student>_<timestamp>.json  (Detailed)            │
│  └── <quiz>_results.csv          (Aggregated)          │
└─────────────────────────────────────────────────────────┘
```

## Components

### 1. GUI Application (`gui/`)

- **quiz_manager.py**: Handles quiz CRUD operations
  - List quizzes
  - Load/save/delete quizzes
  - JSON file management
  
- **quiz_builder.py**: Main GUI application
  - Quiz properties editor
  - Question editor dialog
  - Quiz preview
  - Server launch integration
  
- **main.py**: Entry point for GUI

### 2. Server Application (`server/`)

- **app.py**: Flask web server
  - Quiz delivery routes
  - Session management
  - Score calculation
  - Results export (CSV/JSON)
  - Timer synchronization
  
- **utils.py**: Utilities
  - Logging configuration
  - Quiz data validation
  - Graceful shutdown handlers

### 3. Web Interface (`templates/`, `static/`)

- **index.html**: Main student quiz interface
  - Kid-friendly design
  - Responsive layout
  - Timer display
  - Auto-submit logic
  
- **style.css**: Visual styling
  - Colorful, engaging design
  - Animations and transitions
  - Mobile-responsive

### 4. Build & Deployment

- **build.py**: PyInstaller build script
  - Creates Windows .exe
  - Bundles all dependencies
  - Includes data directories
  
- **bootstrap.py**: Automated installer
  - Python check/install
  - Dependency installation
  - Ngrok configuration
  - Git repository setup
  
- **run_server.py**: Server launcher
  - Flask server startup
  - Ngrok tunnel creation
  - Public URL display

## Key Features

### Quiz Creation
✅ Visual quiz builder (no code)  
✅ Multiple question types  
✅ Per-question scoring weights  
✅ Question shuffling  
✅ Global timer configuration  
✅ Start/end messages  
✅ Quiz preview  

### Student Experience
✅ Kid-friendly UI  
✅ Server-side timer (authoritative)  
✅ Auto-submit on time expiry  
✅ Early submission option  
✅ Visual time warnings  
✅ Responsive design (mobile-friendly)  

### Security & Validation
✅ One submission per device/session  
✅ Server-side validation  
✅ Session ID tracking  
✅ Name requirement enforcement  
✅ No refresh/retake cheating  

### Results Management
✅ Automatic export (JSON + CSV)  
✅ Structured folder organization  
✅ Per-question answer tracking  
✅ Score calculation  
✅ Timestamp logging  
✅ Detailed analytics data  

### Technical Features
✅ Offline-first architecture  
✅ Automatic server launch  
✅ Ngrok integration  
✅ Graceful shutdown  
✅ Error handling & logging  
✅ Windows executable support  

## File Structure

```
quiz/
├── gui/                      # GUI application
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── quiz_builder.py      # Main GUI
│   └── quiz_manager.py      # Data management
├── server/                   # Flask server
│   ├── __init__.py
│   ├── app.py               # Main server
│   └── utils.py             # Utilities
├── templates/                # HTML templates
│   ├── index.html           # Student interface
│   └── error.html           # Error page
├── static/                   # Web assets
│   └── css/
│       └── style.css        # Styles
├── data/                     # Quiz storage (auto-created)
│   └── *.json               # Quiz files
├── results/                  # Results storage (auto-created)
│   └── <quiz_name>/         # Per-quiz folders
├── logs/                     # Application logs (auto-created)
├── build.py                  # Build script
├── bootstrap.py              # Installer
├── run_server.py             # Server launcher
├── main.py                   # Main entry point
├── requirements.txt          # Dependencies
├── README.md                 # Full documentation
├── QUICKSTART.md            # Quick start guide
├── LICENSE                  # MIT License
└── CONTRIBUTING.md          # Contribution guide
```

## Technology Stack

- **GUI**: Tkinter (Python standard library)
- **Web Server**: Flask 3.0.0
- **Tunneling**: pyngrok 6.0.0
- **Packaging**: PyInstaller 6.3.0
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Data Format**: JSON (quizzes), CSV (results)

## Usage Flow

1. **Educator**:
   - Opens Quiz Builder GUI
   - Creates/edits quiz
   - Adds questions
   - Saves quiz
   - Clicks "Launch Quiz"
   - Shares public URL with students

2. **Student**:
   - Opens shared URL in browser
   - Enters name
   - Starts quiz
   - Answers questions (timer visible)
   - Submits (or auto-submits on expiry)
   - Sees confirmation

3. **Results**:
   - Automatically saved on submission
   - Stored in `results/<quiz_name>/`
   - CSV for analysis, JSON for details
   - Educator opens CSV in Excel/Sheets

## Security Considerations

- ✅ Local data storage only
- ✅ No cloud/external services (except ngrok tunnel)
- ✅ Session-based tracking prevents resubmission
- ✅ Server-side validation
- ⚠️ Public URLs (ngrok) - don't share sensitive data
- ⚠️ No authentication - URLs are public access

## Limitations

- Ngrok free tier: 2-hour sessions (without auth token)
- Windows-focused (though code is cross-platform)
- Single quiz active at a time
- No built-in user management
- Results only stored locally

## Future Enhancements (Not Implemented)

- Cloud result storage
- Student authentication
- Quiz templates library
- Advanced analytics dashboard
- Mobile app for quiz creation
- Offline mode for students
- Multiple concurrent quizzes

## Testing Recommendations

1. **Create Test Quiz**:
   - All question types
   - Multiple questions
   - Different point weights

2. **Launch & Test**:
   - Verify server starts
   - Check ngrok URL accessible
   - Test from different devices

3. **Student Experience**:
   - Test timer countdown
   - Test auto-submit
   - Test early submission
   - Verify validation (name, resubmission)

4. **Results**:
   - Verify CSV export
   - Verify JSON export
   - Check data accuracy

## Dependencies

- Python 3.8+
- Flask 3.0.0
- pyngrok 6.0.0
- PyInstaller 6.3.0 (for building .exe)
- Tkinter (usually included with Python)

## Build & Distribution

```bash
# Install dependencies
pip install -r requirements.txt

# Build executable
python build.py

# Executable in dist/QuizBuilder.exe
```

## Documentation

- **README.md**: Complete documentation
- **QUICKSTART.md**: 5-minute getting started guide
- **CONTRIBUTING.md**: Contribution guidelines
- **This file**: Technical architecture summary

## Status

✅ **Complete and Production-Ready**

All requested features implemented:
- ✅ Desktop GUI with Tkinter
- ✅ Quiz builder (visual, no code)
- ✅ Multiple question types
- ✅ Flask web server
- ✅ Ngrok integration
- ✅ Kid-friendly web UI
- ✅ Server-side timer
- ✅ Auto-submit functionality
- ✅ Results export (CSV + JSON)
- ✅ Session management
- ✅ Error handling & logging
- ✅ Windows .exe build
- ✅ Bootstrap installer
- ✅ Comprehensive documentation

## Credits

Built with Python, Tkinter, Flask, and ngrok.
Designed for educators, built for children.

---

**Ready to use!** See QUICKSTART.md to get started.


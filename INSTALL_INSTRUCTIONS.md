# 🚀 Quiz Builder - Installation Instructions

## For Users (Non-Developers)

### Quick Install (Recommended)

1. **Download the Installer:**
   - Go to the GitHub repository
   - Download `install.bat` file only
   - Save it to your Desktop or any folder

2. **Run the Installer:**
   - Double-click `install.bat`
   - Enter the GitHub repository URL when prompted
   - Wait for automatic installation
   - Click 'Yes' to launch the app

3. **Daily Use:**
   - Open the created folder
   - Double-click `start_quiz_builder.bat`

### What the Installer Does Automatically:
✅ Checks if Git is installed  
✅ Checks if Python is installed  
✅ Clones the complete Quiz Builder from GitHub  
✅ Creates isolated virtual environment  
✅ Installs all required dependencies  
✅ Creates necessary folders  
✅ Launches the application  

---

## Alternative: Manual Installation

If you prefer to do it manually or `install.bat` doesn't work:

### Step 1: Download Everything
```bash
# Option A: Using Git (if you have it)
git clone https://github.com/YOUR_USERNAME/quiz-builder
cd quiz-builder

# Option B: Without Git
# Go to https://github.com/YOUR_USERNAME/quiz-builder
# Click "Code" → "Download ZIP"
# Extract the ZIP file
```

### Step 2: Setup
```bash
# Double-click setup.bat
# OR manually:
python -m venv venv_win
venv_win\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Launch
```bash
# Double-click start_quiz_builder.bat
# OR manually:
venv_win\Scripts\activate
python main.py
```

---

## Prerequisites

### For the Automatic Installer:
- **Git** - [Download here](https://git-scm.com/download/win)
- **Python 3.8+** - [Download here](https://www.python.org/downloads/)
  - ⚠️ Check "Add Python to PATH" during installation!

### For Manual Installation:
- **Python 3.8+** only (Git optional)

---

## System Requirements

- **OS:** Windows 10/11, macOS, Linux
- **Python:** 3.8 or higher
- **RAM:** 2GB minimum
- **Disk Space:** 200MB
- **Internet:** Required for initial setup only

---

## Troubleshooting

### "Git is not installed" Error
**Solution:** Install Git from https://git-scm.com/download/win

### "Python is not installed" Error
**Solution:** 
1. Install Python from https://www.python.org/downloads/
2. During installation, CHECK ☑️ "Add Python to PATH"
3. Restart your computer
4. Run installer again

### "Failed to clone repository" Error
**Possible causes:**
- Wrong repository URL
- No internet connection
- Private repository (need to login to git first)

**Solution:**
```bash
# Login to git (if private repo)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Installer doesn't start
**Solution:** Right-click `install.bat` → "Run as administrator"

### Permission Errors
**Solution:**
1. Close any antivirus temporarily
2. Right-click → "Run as administrator"
3. Choose a different installation folder (not Program Files)

---

## First Time Use

After installation:

1. **Launch the app:** Double-click `start_quiz_builder.bat`
2. **Create your first quiz:**
   - Click "Create New Quiz"
   - Enter quiz name
   - Add questions
   - Click "Save"
3. **Launch quiz for students:**
   - Select your quiz
   - Click "Launch Quiz"
   - Share the displayed URL with students

---

## Distribution Instructions

### For Repository Owners:

To share with others:

1. **Put `install.bat` in GitHub root** (already done ✅)
2. **Create a Release:**
   - Go to your GitHub repo
   - Click "Releases" → "Create a new release"
   - Tag: `v1.0.0`
   - Title: `Quiz Builder v1.0.0`
   - Attach `install.bat` as an asset
3. **Share the installer:**
   - Direct link to `install.bat` in the release
   - Or: Link to the raw file on GitHub

### Easy Sharing Link:
```
https://github.com/YOUR_USERNAME/quiz-builder/raw/main/install.bat
```

Users can:
1. Right-click the link
2. Save as `install.bat`
3. Run it

---

## Update Instructions

### To update an existing installation:

**Option 1: Using update_github.bat (for developers)**
```bash
cd quiz-builder
.\update_github.bat
```

**Option 2: Reinstall**
```bash
# Run install.bat again
# Choose 'Yes' to overwrite when prompted
```

**Option 3: Manual Git Pull**
```bash
cd quiz-builder
git pull origin main
venv_win\Scripts\activate
pip install -r requirements.txt --upgrade
```

---

## Uninstall

To remove Quiz Builder:

1. **Stop the application** if running
2. **Delete the folder:**
   - `quiz-builder` folder (the entire thing)
3. **That's it!** No registry entries or system files to clean

---

## Support

If you encounter issues:

1. Check [Troubleshooting](#troubleshooting) section above
2. Check [QUICK_START.md](QUICK_START.md) for usage help
3. Open an issue on GitHub with:
   - Error message
   - Python version (`python --version`)
   - Operating system

---

## Security Notes

- The installer requires internet connection only once
- All data stored locally (no cloud upload)
- Works completely offline after installation
- No personal data collected
- Safe to use on school/work computers

---

**Enjoy creating quizzes! 🎓**

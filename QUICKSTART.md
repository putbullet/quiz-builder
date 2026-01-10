# Quick Start Guide

Get up and running with Quiz Builder in 5 minutes!

## Installation

### Option 1: Bootstrap Installer (Recommended)

1. **Open PowerShell or Command Prompt** in the project directory

2. **Run Bootstrap Installer**:
   ```powershell
   python bootstrap.py
   ```
   
   This will automatically:
   - Check Python installation
   - Install dependencies
   - Set up ngrok (optional)
   - Build executable (optional)

### Option 2: Manual Installation

1. **Activate Virtual Environment** (if using venv):
   ```powershell
   # PowerShell
   ..\venv\Scripts\Activate.ps1
   
   # Or CMD
   ..\venv\Scripts\activate.bat
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Optional: Set Ngrok Token** (Recommended):
   ```powershell
   $env:NGROK_AUTH_TOKEN = "your_token_here"
   ```
   
   Get free token: https://dashboard.ngrok.com/get-started/your-authtoken

## Running the Application

### Run GUI Application

```bash
python main.py
```

Or if built as executable:
```
dist\QuizBuilder.exe
```

## Creating Your First Quiz

1. **Create New Quiz**:
   - Click "File" → "New Quiz" or click "New" button
   - Enter quiz name (e.g., "math_quiz_2024")

2. **Set Quiz Properties**:
   - Quiz Title: "Math Quiz - Chapter 5"
   - Timer: 30 minutes
   - Start Message: "Welcome! Good luck!"
   - End Message: "Thank you for completing the quiz!"

3. **Add Questions**:
   - Click "Add Question"
   - Select question type (Multiple Choice, True/False, etc.)
   - Enter question text
   - Add options (if multiple choice)
   - Set correct answer(s)
   - Set points/weight
   - Click "Save"

4. **Save Quiz**:
   - Click "Save Quiz" button
   - Quiz saved to `data/` folder

## Launching a Quiz

1. **Launch Quiz**:
   - Click "Launch Quiz" button
   - Wait 2-3 seconds for server to start
   - Copy the public URL from the dialog

2. **Share with Students**:
   - Share the URL (ngrok link) with students
   - Students can access on any device with a web browser
   - No installation needed for students

3. **Monitor Results**:
   - Results appear automatically in `results/<quiz_name>/` folder
   - CSV file: `<quiz_name>_results.csv`
   - JSON files: Individual student submissions

## Viewing Results

1. **Open Results Folder**:
   - Navigate to `results/<quiz_name>/`

2. **View CSV**:
   - Open `<quiz_name>_results.csv` in Excel or Google Sheets
   - See all submissions in tabular format

3. **View Individual Submissions**:
   - Open JSON files for detailed per-student data
   - Includes all answers, scores, and timestamps

## Tips

- **Test First**: Use preview feature before launching
- **Save Often**: Click "Save Quiz" regularly
- **Ngrok Token**: Set it once for unlimited tunnels
- **Timer Sync**: Server-side timer prevents cheating
- **Results**: Check `results/` folder after each quiz

## Troubleshooting

**Server won't start?**
- Check if port 5000 is in use
- Ensure Flask is installed: `pip install flask`

**Ngrok not working?**
- Verify token is set: `echo $env:NGROK_AUTH_TOKEN`
- Check internet connection

**Results not saving?**
- Check `results/` folder exists
- Check disk space
- Review logs in `logs/` folder

## Next Steps

- Read full [README.md](README.md) for detailed documentation
- Check [CONTRIBUTING.md](CONTRIBUTING.md) if contributing
- See example quiz structure in `data/` folder

## Support

- Check logs in `logs/` directory
- Review error messages in console/GUI
- Verify all dependencies are installed

---

**Happy Quiz Building!** 🎉


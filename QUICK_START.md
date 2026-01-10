# 📖 Quick Start Guide - Quiz Builder

## 🚀 Installation (First Time Only)

### Step 1: Install Python
1. Go to https://www.python.org/downloads/
2. Download Python (latest version)
3. **IMPORTANT**: Check ✓ "Add Python to PATH" during installation
4. Click "Install Now"
5. Restart your computer

### Step 2: Install Quiz Builder
1. Download the quiz-builder folder
2. Double-click **`setup.bat`**
3. Wait 2-3 minutes for installation
4. When you see "Installation Complete!", close the window

### Step 3: Setup Ngrok (Optional - for sharing quizzes online)
**Skip this if you only need local quizzes (same WiFi network)**

1. Sign up at: https://dashboard.ngrok.com/signup (FREE)
2. Copy your auth token from: https://dashboard.ngrok.com/get-started/your-authtoken
3. Right-click PowerShell icon → Run as Administrator
4. Paste this command (replace YOUR_TOKEN with your actual token):
   ```
   [System.Environment]::SetEnvironmentVariable('NGROK_AUTH_TOKEN', 'YOUR_TOKEN', 'User')
   ```
5. Press Enter
6. Close PowerShell

**Done! You're ready to create quizzes! 🎉**

---

## 🎯 Daily Use - Creating & Running Quizzes

### Starting the App
1. Double-click **`start_quiz_builder.bat`**
2. Quiz Builder window opens

### Creating a New Quiz

#### 1. Click "New" Button
- Enter a quiz name (e.g., "Math Test 1")
- Click OK

#### 2. Fill in Quiz Properties
- **Quiz Name**: Internal name (no spaces recommended)
- **Quiz Title**: What students see (e.g., "Math Quiz - Chapter 3")
- **Timer**: How many minutes students have
- **Start Message**: Instructions for students
- **End Message**: Thank you message

#### 3. Add Questions
1. Click **"Add Question"** button
2. Fill in the question form:
   - **Question Type**: Choose from dropdown
   - **Question Text**: Type your question
   - **Points**: How many points this question is worth
   - **Options**: (For multiple choice) Type one option per line
   - **Correct Answer**: 
     - For multiple choice: Type the EXACT correct option
     - For True/False: Select True or False
     - For short answer: Type the expected answer (leave empty to grade manually)
3. Click **"Save"**
4. Repeat for all questions

#### 4. Save Quiz
- Click **"Save Quiz"** button
- Your quiz is saved!

### Launching a Quiz

1. **Select your quiz** from the dropdown at the top
2. Click **"Launch Quiz"** button (green)
3. A popup shows the quiz URL:
   - **With Ngrok**: `https://xxxx.ngrok-free.app` (works anywhere)
   - **Without Ngrok**: `http://127.0.0.1:5000` (same WiFi only)
4. **Share this URL** with students (copy-paste, QR code, etc.)

### What Students Do
1. Open the URL you shared
2. Enter their full name
3. Click "Start Quiz"
4. Answer questions
5. Click "Submit Quiz" when done
6. They see a multi-language success message

### Viewing Results

1. **Select the quiz** from dropdown
2. Click **"Results"** button
3. A window shows all submissions:
   - Student names
   - Their answers
   - Correct answers
   - Timestamps
4. Results are automatically saved as a text file in the results folder
5. Click **"Open Results Folder"** to see all result files

### Managing Quizzes

#### Edit a Quiz
1. Select quiz from dropdown
2. Edit questions or settings
3. Click "Save Quiz"

#### Delete a Quiz
1. Select quiz from dropdown
2. Click "Delete"
3. Confirm deletion

#### Preview Quiz
1. Select quiz from dropdown
2. Click "Preview"
3. See how the quiz looks

---

## 📊 Results Location

All results are saved in: `results/[quiz_name]/`

Each submission creates:
- **JSON file**: `[student_name]_[timestamp].json` - Complete data
- **Text file**: `[quiz_name]_ALL_RESULTS.txt` - Human-readable summary

### Opening Results
- Double-click the text file to open in Notepad
- Or use the "Open Results Folder" button in the Results viewer

---

## ❓ Common Questions

### Q: Can students retake the quiz?
A: Each time a student opens the link, they get a fresh session. They can take it once per session.

### Q: What happens if time runs out?
A: The quiz auto-submits. Students can't continue answering.

### Q: Can I edit a quiz while it's running?
A: No. Launch a new quiz if you need to make changes.

### Q: How do I share quizzes with students not on my WiFi?
A: Set up Ngrok (see Step 3 in Installation). This gives you a public URL.

### Q: Can I use Arabic or other languages?
A: Yes! The app fully supports Unicode text including Arabic, Chinese, etc.

### Q: How do I grade essay questions?
A: View Results → Read the student's answer → Manually calculate their score

### Q: Can multiple students take the quiz at the same time?
A: Yes! Each student gets their own independent session and timer.

### Q: Where are my quizzes saved?
A: In the `data/` folder as JSON files. Back these up to keep your quizzes safe!

---

## 🆘 Troubleshooting

### "Python is not installed"
→ Install Python from python.org (see Installation Step 1)
→ Make sure you checked "Add Python to PATH"

### "Virtual environment not found"
→ Run `setup.bat` again

### Quiz doesn't launch
→ Make sure the quiz is saved first
→ Check the logs folder for errors
→ Try selecting the quiz from dropdown before clicking Launch

### Students see "Invalid session"
→ They may have submitted already
→ Ask them to open the link in a new browser/incognito window

### Can't see results
→ Make sure students have submitted
→ Check the results/[quiz_name] folder directly

---

## 💡 Tips for Teachers

### Before the Exam
1. **Test Your Quiz**: Preview it, or take it yourself
2. **Check Timer**: Add extra time for reading
3. **Clear Instructions**: Use the start message wisely
4. **Backup**: Copy the `data` folder regularly

### During the Exam
1. **Stay Available**: Monitor for technical issues
2. **Share URL Clearly**: Write it on board, send via email/SMS
3. **Time Warnings**: Tell students how much time is left

### After the Exam
1. **Review Results Immediately**: Click Results button
2. **Export if Needed**: Results auto-save to text files
3. **Grade Essays**: Review short answer questions manually
4. **Archive**: Move old results to a backup folder

---

## 📞 Need Help?

- Check the logs folder for error details
- Read the full README.md for technical details
- Open an issue on GitHub for bugs

---

**Happy Teaching! 🎓**

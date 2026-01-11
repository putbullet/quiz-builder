# 🎯 Building Single Executable File

## Quick Build

### Option 1: Using Batch File (Easiest)
```batch
build_exe.bat
```

### Option 2: Using Python Script
```bash
python build_single_exe.py
```

### Option 3: Manual PyInstaller
```bash
pip install pyinstaller
pyinstaller --clean QuizBuilder.spec
```

---

## What You Get

**Single File:** `QuizBuilder.exe` (approximately 40-60 MB)

**Features:**
- ✅ Complete standalone application
- ✅ No Python installation required
- ✅ No dependencies to install
- ✅ Portable - copy to any Windows PC
- ✅ Double-click to run
- ✅ Includes all templates, styles, and GUI
- ✅ Built-in web server

---

## Distribution

### For End Users:

**Simple Instructions:**
1. Download `QuizBuilder.exe`
2. Double-click to run
3. That's it!

**First Run:**
- May take 10-15 seconds to start (extracting files)
- Subsequent runs are faster
- No installation wizard needed

---

## Build Requirements

**On Build Machine:**
- Python 3.8+
- All dependencies from `requirements.txt`
- PyInstaller (auto-installed by build script)

**On Target Machine:**
- Windows 10/11
- No Python needed
- No dependencies needed

---

## What's Included in the EXE

The single executable contains:
- `main.py` - Entry point
- `gui/` - Tkinter GUI modules
- `server/` - Flask server
- `templates/` - HTML templates
- `static/` - CSS styles
- All Python dependencies (Flask, pyngrok, etc.)
- Python runtime

---

## File Structure After Build

```
quiz/
├── QuizBuilder.exe        ← Single executable (distribute this!)
├── build_exe.bat          ← Build script
├── build_single_exe.py    ← Python build script
├── QuizBuilder.spec       ← PyInstaller configuration
└── [source files...]      ← Keep for development
```

---

## Troubleshooting

### Build Fails
**Solution:**
```bash
# Install/upgrade PyInstaller
pip install --upgrade pyinstaller

# Clean and rebuild
rmdir /s /q build dist
python build_single_exe.py
```

### EXE Too Large
**Current size:** ~40-60 MB (includes Python runtime and all dependencies)

**To reduce size:**
- Use `--onefile` with `--upx-dir` for compression
- Exclude unused modules in `.spec` file
- Remove unnecessary dependencies from `requirements.txt`

### Antivirus Flags EXE
**Reason:** PyInstaller executables sometimes trigger false positives

**Solutions:**
1. Add exception in antivirus
2. Sign the executable with code signing certificate
3. Submit to antivirus vendors as false positive

### EXE Starts Slowly
**First run:** 10-15 seconds (normal - extracting files to temp)
**Subsequent runs:** 2-5 seconds

**Why:** PyInstaller extracts files to `%TEMP%` on first run

---

## Advanced: Customize Build

Edit `QuizBuilder.spec`:

### Add Icon
```python
exe = EXE(
    ...
    icon='icon.ico',  # Add your 256x256 icon
)
```

### Include Additional Files
```python
datas=[
    ('templates', 'templates'),
    ('static', 'static'),
    ('your_file.txt', '.'),  # Add more files
],
```

### Console vs GUI Mode
```python
exe = EXE(
    ...
    console=False,  # False = GUI only, True = show console
)
```

---

## Comparison: Installer vs Single EXE

| Feature | install.bat | QuizBuilder.exe |
|---------|-------------|-----------------|
| Size | ~5 KB | ~50 MB |
| Requires Internet | Yes (first time) | No |
| Requires Python | Auto-installs | No |
| Portable | No | Yes |
| Updates | git pull | Download new .exe |
| Best For | Developers | End Users |

---

## Distribution Checklist

- [ ] Build executable: `build_exe.bat`
- [ ] Test on clean Windows PC
- [ ] Verify no Python required
- [ ] Check antivirus doesn't block
- [ ] Test quiz creation
- [ ] Test quiz launching
- [ ] Test results saving
- [ ] Create download link
- [ ] Write simple instructions

---

## GitHub Release

To distribute via GitHub:

1. **Build the exe:**
   ```bash
   build_exe.bat
   ```

2. **Create GitHub Release:**
   - Go to your repo → Releases
   - Click "Create a new release"
   - Tag: `v1.0.0`
   - Upload `QuizBuilder.exe`

3. **Share direct link:**
   ```
   https://github.com/putbullet/quiz-builder/releases/download/v1.0.0/QuizBuilder.exe
   ```

---

## User Instructions (Copy-Paste)

```
🎓 Quiz Builder - Portable Version

Quick Start:
1. Download QuizBuilder.exe
2. Double-click to run
3. Wait 10 seconds on first launch
4. Start creating quizzes!

No installation required!
No Python needed!
Completely portable!

System Requirements:
- Windows 10/11
- 100 MB free space
- Internet (only for sharing quiz URLs)
```

---

**Happy Building! 🚀**

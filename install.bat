@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo Quiz Builder - Automatic Installer
echo ============================================================
echo.
echo This script will:
echo 1. Clone the Quiz Builder from GitHub
echo 2. Install all requirements
echo 3. Launch the application
echo.

:: Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo Then run this script again.
    echo.
    pause
    exit /b 1
)

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python 3.8 or higher from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

:: Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%

:: Get repository URL from user
echo.
set /p REPO_URL="Enter the GitHub repository URL (e.g., https://github.com/username/quiz-builder): "

if "%REPO_URL%"=="" (
    echo ERROR: Repository URL cannot be empty!
    pause
    exit /b 1
)

:: Extract repository name from URL
for %%a in ("%REPO_URL%") do set "REPO_NAME=%%~na"
if "%REPO_NAME%"=="" set "REPO_NAME=quiz-builder"

echo.
echo Repository: %REPO_NAME%
echo.

:: Check if directory already exists
if exist "%REPO_NAME%" (
    echo WARNING: Directory "%REPO_NAME%" already exists!
    set /p OVERWRITE="Do you want to delete it and reinstall? (y/n): "
    if /i "!OVERWRITE!"=="y" (
        echo Removing old directory...
        rmdir /s /q "%REPO_NAME%"
    ) else (
        echo Installation cancelled.
        pause
        exit /b 1
    )
)

:: Clone the repository
echo.
echo [1/5] Cloning repository from GitHub...
git clone "%REPO_URL%"
if errorlevel 1 (
    echo ERROR: Failed to clone repository!
    echo.
    echo Please check:
    echo - The repository URL is correct
    echo - You have internet connection
    echo - The repository is public (or you're logged into git)
    echo.
    pause
    exit /b 1
)
echo Repository cloned successfully!

:: Navigate to the cloned directory
cd "%REPO_NAME%"
if errorlevel 1 (
    echo ERROR: Failed to navigate to repository directory!
    pause
    exit /b 1
)

:: Create virtual environment
echo.
echo [2/5] Creating virtual environment...
python -m venv venv_win
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment!
    echo Make sure Python venv module is installed.
    pause
    exit /b 1
)
echo Virtual environment created!

:: Activate virtual environment
echo.
echo [3/5] Activating virtual environment...
call venv_win\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

:: Install requirements
echo.
echo [4/5] Installing requirements...
echo This may take a few minutes...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install requirements!
    pause
    exit /b 1
)
echo Requirements installed successfully!

:: Create necessary directories
echo.
echo [5/5] Creating necessary directories...
if not exist "data" mkdir data
if not exist "results" mkdir results
if not exist "logs" mkdir logs
echo Directories created!

:: Installation complete
echo.
echo ============================================================
echo Installation completed successfully!
echo ============================================================
echo.
echo The Quiz Builder is now installed in: %CD%
echo.
echo To launch the application:
echo 1. Navigate to: %CD%
echo 2. Run: start_quiz_builder.bat
echo.
echo Or simply double-click "start_quiz_builder.bat" in the folder.
echo.

:: Ask if user wants to launch now
set /p LAUNCH_NOW="Do you want to launch the Quiz Builder now? (y/n): "
if /i "%LAUNCH_NOW%"=="y" (
    echo.
    echo Launching Quiz Builder...
    start "" "%CD%\start_quiz_builder.bat"
    exit /b 0
)

echo.
echo You can launch the application anytime by running start_quiz_builder.bat
pause

@echo off
echo ============================================================
echo Quiz Builder - Setup and Installation
echo ============================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    pause
    exit /b 1
)

echo [1/4] Python found: 
python --version
echo.

:: Check if virtual environment exists
if exist venv_win (
    echo [2/4] Virtual environment already exists
) else (
    echo [2/4] Creating virtual environment...
    python -m venv venv_win
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
)
echo.

:: Activate virtual environment and install dependencies
echo [3/4] Installing required packages...
echo This may take a few minutes...
echo.
call venv_win\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

:: Create necessary directories
echo [4/4] Creating directories...
if not exist data mkdir data
if not exist results mkdir results
if not exist logs mkdir logs
if not exist templates (
    echo ERROR: templates folder missing!
    pause
    exit /b 1
)
if not exist static (
    echo ERROR: static folder missing!
    pause
    exit /b 1
)
echo.

echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo To start the Quiz Builder, run: start_quiz_builder.bat
echo.
pause

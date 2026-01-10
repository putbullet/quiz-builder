@echo off
setlocal enabledelayedexpansion

:: Self-elevate to run as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo ============================================================
echo Quiz Builder - Automatic Installer [ADMIN MODE]
echo ============================================================
echo.
echo This script will automatically:
echo 1. Install Git (if needed)
echo 2. Install Python (if needed)
echo 3. Clone the Quiz Builder from GitHub
echo 4. Install all requirements
echo 5. Launch the application
echo.
echo Please wait, this may take 5-10 minutes...
echo.

:: Check and install Git if needed
echo [STEP 1/7] Checking Git installation...
git --version >nul 2>&1
if errorlevel 1 (
    echo Git is not installed. Installing Git automatically...
    echo.
    
    :: Download Git installer
    echo Downloading Git installer (50MB)...
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe' -OutFile '%TEMP%\git-installer.exe'}"
    
    if not exist "%TEMP%\git-installer.exe" (
        echo ERROR: Failed to download Git installer!
        echo Please install Git manually from: https://git-scm.com/download/win
        pause
        exit /b 1
    )
    
    :: Install Git silently
    echo Installing Git (this takes 2-3 minutes)...
    "%TEMP%\git-installer.exe" /VERYSILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /COMPONENTS="icons,ext\reg\shellhere,assoc,assoc_sh"
    
    :: Wait for installation to complete
    timeout /t 10 /nobreak >nul
    
    :: Add Git to PATH for current session
    set "PATH=%PATH%;C:\Program Files\Git\cmd"
    
    :: Verify installation
    git --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Git installation failed!
        echo Please restart your computer and run this script again.
        pause
        exit /b 1
    )
    
    echo Git installed successfully!
    del "%TEMP%\git-installer.exe"
) else (
    echo Git is already installed.
)

echo.
echo [STEP 2/7] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Installing Python automatically...
    echo.
    
    :: Download Python installer
    echo Downloading Python 3.11 installer (25MB)...
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe' -OutFile '%TEMP%\python-installer.exe'}"
    
    if not exist "%TEMP%\python-installer.exe" (
        echo ERROR: Failed to download Python installer!
        echo Please install Python manually from: https://www.python.org/downloads/
        pause
        exit /b 1
    )
    
echo [STEP 3/7] Getting repository information...
echo.
set /p REPO_URL="Enter the GitHub repository URL: "

if "%REPO_URL%"=="" (
    echo ERROR: Repository URL cannot be empty!
    echo Example: https://github.com/username/quiz-builder
    :: Wait for installation to complete
    timeout /t 15 /nobreak >nul
    
    :: Refresh environment variables
    call refreshenv >nul 2>&1
    
    :: Add Python to PATH for current session
    for /f "tokens=*" %%a in ('where python 2^>nul') do set "PYTHON_PATH=%%a"
    if "%PYTHON_PATH%"=="" (
        set "PATH=%PATH%;C:\Program Files\Python311;C:\Program Files\Python311\Scripts"
        set "PATH=%PATH%;%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts"
    )
    
    :: Verify installation
    python --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python installation failed!
        echo Please restart your computer and run this script again.
        pause
        exit /b 1
    )
    
    echo Python installed successfully!
    del "%TEMP%\python-installer.exe"
) else (
    echo Python is already installed.
)

:: Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Using Python %PYTHON_VERSION%

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
STEP 4/7
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
echo [STEP 5/7] Creating virtual environment...
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
echo [STEP 6/7] Activating virtual environment...
call venv_win\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

:: Install requirements
echo.
echo [STEP 7/7] Installing requirements...
echo This may take a few minutes...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install requirements!
    pause
    exit /b 1
)
echo Requirements installed successfully!

:: Create necessary directories
echo.
echo Creating necessary directories...
if not exist "data" mkdir data
if not exist "results" mkdir results
if not exist "logs" mkdir logs

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
set utomatically launch the application
echo.
echo Launching Quiz Builder in 3 seconds...
timeout /t 3 /nobreak >nul
start "" "%CD%\start_quiz_builder.bat"
echo.
echo Quiz Builder is starting!
echo You can close this window.
timeout /t 2 /nobreak >nul
exit /b 0
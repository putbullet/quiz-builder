@echo off
setlocal enabledelayedexpansion

:: Self-elevate to run as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process cmd.exe -ArgumentList '/c cd /d %CD% && %~f0 && pause' -Verb RunAs"
    exit /b
)

cls
echo ============================================================
echo Quiz Builder - Automatic Installer [ADMIN MODE]
echo ============================================================
echo.
echo This script will automatically:
echo 1. Install Git (if needed)
echo 2. Install Python (if needed)
echo 3. Clone/Update Quiz Builder from GitHub
echo 4. Install all requirements
echo 5. Launch the application
echo.
echo Please wait, this may take 5-10 minutes...
echo.
pause

:: Check and install Git if needed
echo.
echo [STEP 1/7] Checking Git installation...
git --version >nul 2>&1
if errorlevel 1 (
    echo Git is not installed. Installing Git automatically...
    echo.
    
    :: Download Git installer
    echo Downloading Git installer (50MB)...
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe' -OutFile '%TEMP%\git-installer.exe'"
    
    if not exist "%TEMP%\git-installer.exe" (
        echo ERROR: Failed to download Git installer!
        echo.
        echo Please install Git manually from: https://git-scm.com/download/win
        echo Then run this script again.
        pause
        exit /b 1
    )
    
    :: Install Git silently
    echo Installing Git (this takes 2-3 minutes)...
    start /wait "" "%TEMP%\git-installer.exe" /VERYSILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /COMPONENTS="icons,ext\reg\shellhere,assoc,assoc_sh"
    
    :: Add Git to PATH for current session
    set "PATH=%PATH%;C:\Program Files\Git\cmd;C:\Program Files\Git\bin"
    
    :: Verify installation
    timeout /t 5 /nobreak >nul
    git --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Git installation failed!
        echo Please restart your computer and run this script again.
        pause
        exit /b 1
    )
    
    echo Git installed successfully!
    del "%TEMP%\git-installer.exe" 2>nul
) else (
    for /f "tokens=*" %%a in ('git --version') do echo %%a
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
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe' -OutFile '%TEMP%\python-installer.exe'"
    
    if not exist "%TEMP%\python-installer.exe" (
        echo ERROR: Failed to download Python installer!
        echo.
        echo Please install Python manually from: https://www.python.org/downloads/
        pause
        exit /b 1
    )
    
    :: Install Python silently with pip and add to PATH
    echo Installing Python (this takes 2-3 minutes)...
    start /wait "" "%TEMP%\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_pip=1
    
    :: Refresh PATH
    set "PATH=%PATH%;C:\Program Files\Python311;C:\Program Files\Python311\Scripts"
    set "PATH=%PATH%;%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts"
    
    :: Verify installation
    timeout /t 5 /nobreak >nul
    python --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python installation failed!
        echo Please restart your computer and run this script again.
        pause
        exit /b 1
    )
    
    echo Python installed successfully!
    del "%TEMP%\python-installer.exe" 2>nul
) else (
    for /f "tokens=*" %%a in ('python --version') do echo %%a
    echo Python is already installed.
)

:: Repository settings
set "REPO_URL=https://github.com/putbullet/quiz-builder.git"
set "REPO_NAME=quiz-builder"

echo.
echo [STEP 3/7] Checking repository...
echo Repository: %REPO_URL%
echo.

:: Check if directory already exists
if exist "%REPO_NAME%" (
    echo Directory "%REPO_NAME%" already exists.
    echo Checking for updates from GitHub...
    
    cd "%REPO_NAME%"
    
    :: Fetch latest changes
    git fetch origin main 2>nul
    
    :: Check if update is available
    git status -uno | find "Your branch is behind" >nul
    if not errorlevel 1 (
        echo New updates available! Pulling latest changes...
        git pull origin main
        if errorlevel 1 (
            echo WARNING: Failed to pull updates. Using existing version.
        ) else (
            echo Repository updated successfully!
        )
    ) else (
        echo Repository is already up to date.
    )
    
    cd ..
) else (
    :: Clone the repository
    echo.
    echo [STEP 4/7] Cloning repository from GitHub...
    git clone "%REPO_URL%"
    if errorlevel 1 (
        echo ERROR: Failed to clone repository!
        echo.
        echo Please check your internet connection and try again.
        pause
        exit /b 1
    )
    echo Repository cloned successfully!
)

:: Navigate to the cloned directory
echo.
echo [STEP 5/7] Setting up environment...
cd "%REPO_NAME%"
if errorlevel 1 (
    echo ERROR: Failed to navigate to repository directory!
    pause
    exit /b 1
)

:: Create or reuse virtual environment
if not exist "venv_win" (
    echo Creating virtual environment...
    python -m venv venv_win
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        echo Make sure Python venv module is installed.
        pause
        exit /b 1
    )
    echo Virtual environment created!
) else (
    echo Virtual environment already exists.
)

:: Activate virtual environment
echo.
echo [STEP 6/7] Activating virtual environment...
call venv_win\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)
echo Virtual environment activated!

:: Install requirements
echo.
echo [STEP 7/7] Installing/Updating requirements...
echo This may take a few minutes...
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt --upgrade
if errorlevel 1 (
    echo ERROR: Failed to install requirements!
    pause
    exit /b 1
)
echo Requirements installed successfully!

:: Create necessary directories
if not exist "data" mkdir data
if not exist "results" mkdir results
if not exist "logs" mkdir logs

:: Installation complete
echo.
echo ============================================================
echo Installation completed successfully!
echo ============================================================
echo.
echo Launching Quiz Builder...
echo.

:: Launch the application directly
python main.py

:: If main.py exits, keep window open to show errors
if errorlevel 1 (
    echo.
    echo ============================================================
    echo ERROR: Application exited with error code %errorlevel%
    echo ============================================================
    echo.
)

pause

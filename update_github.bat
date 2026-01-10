@echo off
echo ============================================================
echo Quiz Builder - Quick Update to GitHub
echo ============================================================
echo.

:: Check if git is initialized
if not exist .git (
    echo ERROR: Git repository not initialized!
    echo Please run push_to_github.ps1 first
    pause
    exit /b 1
)

:: Get commit message from user
set /p commit_msg="Enter a description of your changes: "

if "%commit_msg%"=="" (
    set commit_msg=Update quiz builder
)

echo.
echo Updating repository...
echo.

:: Add all changes
git add .
echo [1/3] Files added

:: Commit changes
git commit -m "%commit_msg%"
if errorlevel 1 (
    echo [2/3] No changes to commit
) else (
    echo [2/3] Changes committed
)

:: Push to GitHub
git push
if errorlevel 1 (
    echo [3/3] Failed to push to GitHub
    echo.
    echo Make sure you're connected to the internet
    pause
    exit /b 1
) else (
    echo [3/3] Pushed to GitHub successfully!
)

echo.
echo ============================================================
echo Repository updated!
echo ============================================================
echo.
pause

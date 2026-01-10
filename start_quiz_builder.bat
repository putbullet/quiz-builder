@echo off
title Quiz Builder - Offline Quiz System

:: Activate virtual environment
if exist venv_win\Scripts\activate.bat (
    call venv_win\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first to install the application.
    pause
    exit /b 1
)

:: Start the application
echo ============================================================
echo Starting Quiz Builder...
echo ============================================================
echo.
python main.py

:: Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start
    echo Check the error message above for details
    pause
)

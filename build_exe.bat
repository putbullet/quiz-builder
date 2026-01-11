@echo off
echo ============================================================
echo Quiz Builder - Build Single EXE File
echo ============================================================
echo.
echo This will create a single portable .exe file that includes:
echo - All Python code
echo - GUI interface
echo - Web server
echo - Templates and styles
echo - All dependencies
echo.
echo The .exe file will be completely portable - no installation needed!
echo.
pause

:: Check if PyInstaller is installed
echo Checking PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
)

:: Clean previous builds
echo.
echo Cleaning previous builds...
if exist "build\" rmdir /s /q "build\"
if exist "dist\" rmdir /s /q "dist\"
if exist "QuizBuilder.exe" del "QuizBuilder.exe"

:: Build the executable
echo.
echo Building single executable file...
echo This may take 3-5 minutes...
echo.
pyinstaller --clean QuizBuilder.spec

if errorlevel 1 (
    echo.
    echo ============================================================
    echo ERROR: Build failed!
    echo ============================================================
    pause
    exit /b 1
)

:: Move exe to root and clean up
echo.
echo Moving executable to root directory...
if exist "dist\QuizBuilder.exe" (
    move "dist\QuizBuilder.exe" "QuizBuilder.exe"
    echo.
    echo ============================================================
    echo Build successful!
    echo ============================================================
    echo.
    echo Created: QuizBuilder.exe
    echo Size: 
    for %%A in ("QuizBuilder.exe") do echo %%~zA bytes
    echo.
    echo This file is completely portable!
    echo You can copy it to any Windows PC and run it.
    echo No Python or dependencies needed on target PC.
    echo.
    echo Note: First run may take 10-15 seconds to extract files.
    echo.
) else (
    echo ERROR: Executable not found!
    pause
    exit /b 1
)

:: Clean up build artifacts
echo Cleaning up build artifacts...
rmdir /s /q "build\" 2>nul
rmdir /s /q "dist\" 2>nul

echo.
echo Done! You can now run QuizBuilder.exe
echo.
pause

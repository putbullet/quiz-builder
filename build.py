"""
Build script for creating Windows executable using PyInstaller
"""
import os
import sys
import subprocess
import shutil


def build_exe():
    """Build the quiz builder as a Windows executable"""
    
    print("Building Quiz Builder executable...")
    
    # Clean previous builds
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('QuizBuilder.spec'):
        os.remove('QuizBuilder.spec')
    
    # PyInstaller command
    # Note: Using main.py as entry point
    cmd = [
        'pyinstaller',
        '--name=QuizBuilder',
        '--onefile',
        '--windowed',  # No console window for GUI
        '--icon=NONE',  # Can add icon file later
        '--add-data=data;data',  # Include data directory
        '--add-data=results;results',  # Include results directory
        '--add-data=templates;templates',  # Include templates
        '--add-data=static;static',  # Include static files
        '--hidden-import=flask',
        '--hidden-import=pyngrok',
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=tkinter.simpledialog',
        '--hidden-import=server.app',
        '--hidden-import=server.utils',
        '--hidden-import=gui.quiz_builder',
        '--hidden-import=gui.quiz_manager',
        '--collect-all=pyngrok',  # Collect all pyngrok data files
        'main.py'  # Use main.py as entry point
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build successful!")
        print(f"Executable location: {os.path.abspath('dist/QuizBuilder.exe')}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Error: PyInstaller not found. Install it with: pip install pyinstaller")
        return False


if __name__ == '__main__':
    if build_exe():
        print("\n✓ Build completed successfully!")
        sys.exit(0)
    else:
        print("\n✗ Build failed!")
        sys.exit(1)


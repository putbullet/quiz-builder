"""
Build Script for Quiz Builder Executable
Creates a single portable .exe file using PyInstaller
"""

import subprocess
import sys
import os
import shutil

def check_pyinstaller():
    """Check if PyInstaller is installed, install if not"""
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
        return True
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed")
        return True

def clean_previous_builds():
    """Remove previous build artifacts"""
    print("\nCleaning previous builds...")
    directories = ["build", "dist", "__pycache__"]
    files = ["QuizBuilder.exe"]
    
    for dir_name in directories:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  Removed {dir_name}/")
    
    for file_name in files:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"  Removed {file_name}")

def build_executable():
    """Build the executable using PyInstaller"""
    print("\n" + "="*60)
    print("Building Quiz Builder executable...")
    print("="*60)
    print("\nThis may take 3-5 minutes...\n")
    
    try:
        # Run PyInstaller using Python module instead of command
        subprocess.check_call([
            sys.executable,
            "-m",
            "PyInstaller",
            "--clean",
            "QuizBuilder.spec"
        ])
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed with error: {e}")
        return False

def finalize_build():
    """Move exe to root and clean up"""
    print("\nFinalizing build...")
    
    exe_path = os.path.join("dist", "QuizBuilder.exe")
    
    if os.path.exists(exe_path):
        # Move to root
        shutil.move(exe_path, "QuizBuilder.exe")
        
        # Get file size
        size = os.path.getsize("QuizBuilder.exe")
        size_mb = size / (1024 * 1024)
        
        print("\n" + "="*60)
        print("Build successful!")
        print("="*60)
        print(f"\nCreated: QuizBuilder.exe")
        print(f"Size: {size_mb:.2f} MB")
        print("\nThis file is completely portable!")
        print("You can copy it to any Windows PC and run it.")
        print("No Python or dependencies needed on target PC.")
        print("\nNote: First run may take 10-15 seconds to extract files.")
        
        # Clean up
        print("\nCleaning up build artifacts...")
        shutil.rmtree("build", ignore_errors=True)
        shutil.rmtree("dist", ignore_errors=True)
        
        return True
    else:
        print("\n✗ ERROR: Executable not found!")
        return False

def main():
    """Main build process"""
    print("="*60)
    print("Quiz Builder - Build Single EXE File")
    print("="*60)
    print("\nThis will create a single portable .exe file that includes:")
    print("  • All Python code")
    print("  • GUI interface")
    print("  • Web server")
    print("  • Templates and styles")
    print("  • All dependencies")
    print("\nThe .exe file will be completely portable - no installation needed!")
    
    # Check/install PyInstaller
    if not check_pyinstaller():
        return False
    
    # Clean previous builds
    clean_previous_builds()
    
    # Build executable
    if not build_executable():
        return False
    
    # Finalize
    if not finalize_build():
        return False
    
    print("\n✓ Done! You can now run QuizBuilder.exe")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

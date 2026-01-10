"""
Bootstrap installer for Windows - One-click setup for educators
Automatically installs Python, dependencies, configures ngrok, and builds executable
"""
import os
import sys
import subprocess
import urllib.request
import json
import ctypes
from pathlib import Path


def is_admin():
    """Check if running as administrator"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def check_python():
    """Check if Python 3 is installed"""
    try:
        result = subprocess.run([sys.executable, '--version'], 
                              capture_output=True, text=True)
        version = result.stdout.strip()
        if '3.' in version:
            print(f"✓ Python found: {version}")
            return True
    except:
        pass
    
    print("✗ Python 3 not found")
    return False


def install_python():
    """Download and install Python 3"""
    print("\nDownloading Python 3 installer...")
    python_url = "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"
    installer_path = "python_installer.exe"
    
    try:
        urllib.request.urlretrieve(python_url, installer_path)
        print("Python installer downloaded. Please run it manually to install Python.")
        print("After installation, run this script again.")
        return False
    except Exception as e:
        print(f"Error downloading Python: {e}")
        print("Please download and install Python 3 from https://www.python.org/downloads/")
        return False


def install_dependencies():
    """Install required Python packages"""
    print("\nInstalling dependencies...")
    
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                      check=True)
        
        with open('requirements.txt', 'r') as f:
            packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        for package in packages:
            print(f"  Installing {package}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                         check=True, capture_output=True)
        
        print("✓ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        return False


def setup_ngrok():
    """Configure ngrok (get auth token from user)"""
    print("\n" + "="*60)
    print("NGROK SETUP")
    print("="*60)
    print("To use ngrok (for public quiz URLs), you need an auth token.")
    print("1. Visit: https://dashboard.ngrok.com/get-started/your-authtoken")
    print("2. Sign up for a free account")
    print("3. Copy your auth token")
    print("4. Enter it below (or press Enter to skip and set later)")
    print("="*60)
    
    token = input("\nEnter your ngrok auth token (or press Enter to skip): ").strip()
    
    if token:
        # Save to environment variable suggestion
        print("\nTo use this token, set it as an environment variable:")
        print(f"  setx NGROK_AUTH_TOKEN {token}")
        print("\nOr add it to your system environment variables manually.")
        
        # Try to set it for current session
        os.environ['NGROK_AUTH_TOKEN'] = token
        print("✓ Token set for current session")
        return True
    else:
        print("Skipping ngrok setup. You can set it later.")
        print("Without ngrok token, you'll have limited tunnel time (2 hours).")
        return False


def setup_git():
    """Initialize git repository and provide GitHub setup instructions"""
    print("\n" + "="*60)
    print("GIT SETUP")
    print("="*60)
    
    try:
        # Check if git is installed
        subprocess.run(['git', '--version'], check=True, capture_output=True)
        print("✓ Git found")
        
        # Check if already a git repo
        if os.path.exists('.git'):
            print("✓ Git repository already initialized")
        else:
            # Initialize git
            subprocess.run(['git', 'init'], check=True)
            subprocess.run(['git', 'add', '.'], check=True)
            subprocess.run(['git', 'commit', '-m', 'Initial commit: Quiz Builder application'], 
                         check=True)
            print("✓ Git repository initialized")
        
        print("\nTo push to GitHub:")
        print("1. Create a new repository on GitHub")
        print("2. Run: git remote add origin <your-repo-url>")
        print("3. Run: git push -u origin main")
        
        return True
    except FileNotFoundError:
        print("✗ Git not found. Install from: https://git-scm.com/download/win")
        print("  (Optional - you can skip this step)")
        return False
    except subprocess.CalledProcessError as e:
        print(f"✗ Git error: {e}")
        return False


def build_executable():
    """Build the executable using PyInstaller"""
    print("\n" + "="*60)
    print("BUILDING EXECUTABLE")
    print("="*60)
    
    response = input("Build executable now? (y/n): ").strip().lower()
    if response != 'y':
        print("Skipping build. You can build later with: python build.py")
        return False
    
    try:
        import PyInstaller.__main__
        
        # Import and run build script
        from build import build_exe
        return build_exe()
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], 
                      check=True)
        from build import build_exe
        return build_exe()
    except Exception as e:
        print(f"✗ Build error: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_directories():
    """Create necessary directories"""
    dirs = ['data', 'results', 'logs']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("✓ Directories created")


def main():
    """Main bootstrap process"""
    print("="*60)
    print("QUIZ BUILDER - BOOTSTRAP INSTALLER")
    print("="*60)
    print("\nThis script will:")
    print("1. Check Python installation")
    print("2. Install dependencies")
    print("3. Configure ngrok (optional)")
    print("4. Set up Git repository (optional)")
    print("5. Build executable (optional)")
    print("="*60)
    
    input("\nPress Enter to continue...")
    
    # Check Python
    if not check_python():
        if install_python():
            return
        else:
            print("\nPlease install Python 3 and run this script again.")
            return
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("\n✗ Failed to install dependencies. Please check errors above.")
        return
    
    # Setup ngrok
    setup_ngrok()
    
    # Setup git (optional)
    setup_git()
    
    # Build executable
    build_executable()
    
    print("\n" + "="*60)
    print("INSTALLATION COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("1. If executable was built, find it in: dist/QuizBuilder.exe")
    print("2. Or run the app directly with: python gui/main.py")
    print("3. Set NGROK_AUTH_TOKEN environment variable for unlimited tunnels")
    print("4. Create your first quiz!")
    print("\nDocumentation: See README.md for detailed usage instructions")
    print("="*60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


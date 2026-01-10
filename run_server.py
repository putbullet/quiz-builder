"""
Server launcher with ngrok integration for quiz delivery
"""
import os
import sys
import threading
import subprocess
import time
import webbrowser
import signal
import atexit

try:
    from flask import Flask
    from pyngrok import ngrok, conf
    from server.app import create_app
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please install dependencies: pip install -r requirements.txt")
    sys.exit(1)


def launch_quiz_server(quiz_file: str, parent_window=None):
    """
    Launch Flask server and ngrok tunnel for a quiz
    
    Args:
        quiz_file: Name of quiz JSON file (e.g., "my_quiz.json")
        parent_window: Optional Tkinter window to display URL
    """
    quiz_name = quiz_file.replace('.json', '')
    
    # Load quiz
    try:
        app = create_app(quiz_name)
    except Exception as e:
        raise ValueError(f"Failed to load quiz: {e}")
    
    # Start Flask server in a thread
    def run_server():
        app.run(host='127.0.0.1', port=5000, debug=False, threaded=True, use_reloader=False)
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(2)
    
    # Create ngrok tunnel (fallback to local-only if ngrok fails)
    public_url_str = None
    ngrok_error = None
    
    # Check if ngrok token is set before trying to connect
    ngrok_auth_token = os.environ.get('NGROK_AUTH_TOKEN', '')
    if not ngrok_auth_token:
        # Skip ngrok entirely if no token (cleaner output)
        print(f"\n{'='*60}")
        print(f"Quiz Server Started (Local Only)")
        print(f"{'='*60}")
        print(f"Local URL: http://127.0.0.1:5000")
        print(f"\n⚠️  Ngrok not configured (no auth token found)")
        print(f"   Server is running locally only.")
        print(f"   To enable public access, set NGROK_AUTH_TOKEN environment variable.")
        print(f"   See NGROK_SETUP.md for instructions.")
        print(f"{'='*60}\n")
        
        # Display local-only message in GUI
        if parent_window:
            try:
                from tkinter import messagebox
                messagebox.showinfo(
                    "Quiz Launched (Local Only)",
                    f"Quiz server started locally!\n\n"
                    f"Local URL: http://127.0.0.1:5000\n\n"
                    f"⚠️  Ngrok not configured - only local access available.\n\n"
                    f"To enable public URLs (share with students anywhere):\n"
                    f"1. Sign up at: https://dashboard.ngrok.com/signup\n"
                    f"2. Get your token from: https://dashboard.ngrok.com/get-started/your-authtoken\n"
                    f"3. Set environment variable: NGROK_AUTH_TOKEN\n\n"
                    f"See NGROK_SETUP.md for detailed instructions.\n\n"
                    f"Click OK to open quiz in browser.",
                    parent=parent_window
                )
                webbrowser.open("http://127.0.0.1:5000")
            except Exception as e:
                print(f"Error showing dialog: {e}")
        
        return "http://127.0.0.1:5000", server_thread
    
    # Try to connect ngrok (token is set)
    try:
        import sys
        import contextlib
        from io import StringIO
        
        # Suppress verbose ngrok error output temporarily
        error_buffer = StringIO()
        
        global _current_tunnel
        with contextlib.redirect_stderr(error_buffer):
            _current_tunnel = ngrok.connect(5000)
        
        public_url_str = str(_current_tunnel.public_url)
        print(f"\n{'='*60}")
        print(f"Quiz Server Started!")
        print(f"{'='*60}")
        print(f"Local URL: http://127.0.0.1:5000")
        print(f"Public URL: {public_url_str}")
        print(f"{'='*60}\n")
        
        # Display URL in GUI if window provided
        if parent_window:
            try:
                from tkinter import messagebox
                messagebox.showinfo(
                    "Quiz Launched!",
                    f"Quiz is now live!\n\n"
                    f"Public URL:\n{public_url_str}\n\n"
                    f"Share this URL with students.\n\n"
                    f"Click OK to open in browser.",
                    parent=parent_window
                )
                webbrowser.open(public_url_str)
            except Exception as e:
                print(f"Error showing dialog: {e}")
        
        return public_url_str, server_thread
        
    except Exception as e:
        # Ngrok connection failed (token might be invalid)
        ngrok_error = str(e)
        print(f"\n{'='*60}")
        print(f"Quiz Server Started (Local Only)")
        print(f"{'='*60}")
        print(f"Local URL: http://127.0.0.1:5000")
        print(f"\n⚠️  Ngrok connection failed")
        print(f"   Error: {ngrok_error[:150]}...")
        print(f"\n   Server is running locally. Students on the same network")
        print(f"   can access via: http://127.0.0.1:5000")
        print(f"   Or verify your NGROK_AUTH_TOKEN is correct.")
        print(f"{'='*60}\n")
        
        # Display local-only message in GUI
        if parent_window:
            try:
                from tkinter import messagebox
                messagebox.showwarning(
                    "Quiz Launched (Local Only)",
                    f"Quiz server started locally!\n\n"
                    f"Local URL: http://127.0.0.1:5000\n\n"
                    f"⚠️  Ngrok connection failed.\n"
                    f"   Your token might be invalid or expired.\n\n"
                    f"Server is running but only accessible locally.\n"
                    f"Verify your NGROK_AUTH_TOKEN or see NGROK_SETUP.md.\n\n"
                    f"Click OK to open quiz in browser.",
                    parent=parent_window
                )
                webbrowser.open("http://127.0.0.1:5000")
            except Exception as e:
                print(f"Error showing dialog: {e}")
        
        # Return local URL even if ngrok failed
        return "http://127.0.0.1:5000", server_thread


# Global variable to track ngrok tunnel
_current_tunnel = None

def stop_ngrok():
    """Stop all ngrok tunnels"""
    global _current_tunnel
    try:
        if _current_tunnel:
            ngrok.disconnect(_current_tunnel.public_url)
        ngrok.kill()
        _current_tunnel = None
    except Exception as e:
        print(f"Error stopping ngrok: {e}")


def cleanup():
    """Cleanup on exit"""
    stop_ngrok()


# Register cleanup on exit
atexit.register(cleanup)
signal.signal(signal.SIGINT, lambda s, f: (cleanup(), sys.exit(0)))
signal.signal(signal.SIGTERM, lambda s, f: (cleanup(), sys.exit(0)))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python run_server.py <quiz_name.json>")
        sys.exit(1)
    
    quiz_file = sys.argv[1]
    try:
        url, thread = launch_quiz_server(quiz_file)
        print(f"\nServer running. Press Ctrl+C to stop.\n")
        print(f"Public URL: {url}")
        print(f"Local URL: http://127.0.0.1:5000\n")
        
        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
                if not thread.is_alive():
                    print("Server thread stopped unexpectedly!")
                    break
        except KeyboardInterrupt:
            print("\nStopping server...")
            cleanup()
            sys.exit(0)
    except KeyboardInterrupt:
        print("\nStopping server...")
        cleanup()
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        cleanup()
        sys.exit(1)


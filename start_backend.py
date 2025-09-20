#!/usr/bin/env python3
"""
Start the Flask backend server
"""

import subprocess
import sys
import os

def start_backend():
    """Start the Flask backend server"""
    print("🚀 Starting Flask Backend Server...")
    
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    
    try:
        # Install requirements if needed
        print("📦 Installing Python dependencies...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      cwd=backend_dir, check=True)
        
        # Start the Flask app
        print("🌐 Starting Flask server on http://localhost:5000")
        subprocess.run([sys.executable, 'app.py'], cwd=backend_dir)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting backend: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
        return True

if __name__ == "__main__":
    start_backend()

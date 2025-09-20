#!/usr/bin/env python3
"""
Start both backend and frontend servers
"""

import subprocess
import sys
import os
import threading
import time

def start_backend():
    """Start the Flask backend server in a separate thread"""
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    
    try:
        print("🚀 Starting Flask Backend Server...")
        subprocess.run([sys.executable, 'app.py'], cwd=backend_dir)
    except KeyboardInterrupt:
        print("🛑 Backend server stopped")

def start_frontend():
    """Start the React frontend development server in a separate thread"""
    try:
        print("🚀 Starting React Frontend Server...")
        subprocess.run(['npm', 'start'])
    except KeyboardInterrupt:
        print("🛑 Frontend server stopped")

def main():
    """Start both servers"""
    print("🎯 Starting Interactive Prompt Responder")
    print("=" * 50)
    
    # Install dependencies
    print("📦 Installing dependencies...")
    
    # Install Python dependencies
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      cwd=backend_dir, check=True)
        print("✅ Python dependencies installed")
    except subprocess.CalledProcessError:
        print("⚠️  Could not install Python dependencies")
    
    # Install npm dependencies
    try:
        subprocess.run(['npm', 'install'], check=True)
        print("✅ npm dependencies installed")
    except subprocess.CalledProcessError:
        print("⚠️  Could not install npm dependencies")
    
    print("\n🌐 Starting servers...")
    print("Backend: http://localhost:5000")
    print("Frontend: http://localhost:3000")
    print("\nPress Ctrl+C to stop both servers")
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(2)
    
    # Start frontend in main thread
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Both servers stopped")

if __name__ == "__main__":
    main()

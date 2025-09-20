#!/usr/bin/env python3
"""
Start the React frontend development server
"""

import subprocess
import sys
import os

def start_frontend():
    """Start the React frontend development server"""
    print("🚀 Starting React Frontend Server...")
    
    try:
        # Install npm dependencies if needed
        print("📦 Installing npm dependencies...")
        subprocess.run(['npm', 'install'], check=True)
        
        # Start the development server
        print("🌐 Starting React development server on http://localhost:3000")
        subprocess.run(['npm', 'start'], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting frontend: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
        return True

if __name__ == "__main__":
    start_frontend()

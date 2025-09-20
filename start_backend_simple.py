#!/usr/bin/env python3
"""
Simple backend startup script
"""

import subprocess
import sys
import os
import time

def start_backend():
    """Start the Flask backend server"""
    print("🚀 Starting Flask Backend Server...")
    
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    
    try:
        print(f"📁 Backend directory: {backend_dir}")
        print("🌐 Starting Flask server on http://localhost:5000")
        print("📊 Database: lectures/week_10/SQLAgent/sql_agent_class.db")
        print("\n" + "="*50)
        print("✅ Backend server is running!")
        print("🔗 API endpoints:")
        print("   - Health: http://localhost:5000/api/health")
        print("   - Analyze: http://localhost:5000/api/analyze")
        print("   - Database Info: http://localhost:5000/api/database/info")
        print("="*50)
        print("\n💡 Keep this terminal open to keep the server running")
        print("🛑 Press Ctrl+C to stop the server")
        print("\n" + "="*50)
        
        # Start the Flask app
        subprocess.run([sys.executable, 'app.py'], cwd=backend_dir)
        
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
        return True
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return False

if __name__ == "__main__":
    start_backend()

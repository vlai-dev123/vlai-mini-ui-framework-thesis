#!/usr/bin/env python3
"""
Launcher script for the Thesis Framework Web Interface
Run this script from the project root to start the web interface
"""

import os
import sys
import subprocess
import webbrowser
import time

def main():
    print("🎓 Thesis Framework Web Interface Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('code/web-interface'):
        print("❌ Error: Web interface not found!")
        print("Please run this script from the project root directory.")
        return
    
    # Change to web interface directory
    os.chdir('code/web-interface')
    
    # Check if Flask is installed
    try:
        import flask
        print("✅ Flask is installed")
    except ImportError:
        print("❌ Flask is not installed. Installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask'])
        print("✅ Flask installed successfully")
    
    # Check if required Python modules are available
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'code', 'data-analysis'))
        sys.path.append(os.path.join(os.path.dirname(__file__), 'code', 'tools'))
        
        # Try to import analysis modules
        try:
            from main_analysis import ThesisDataAnalyzer
            from preprocess import DataPreprocessor
            print("✅ Data analysis modules available")
        except ImportError:
            print("⚠️  Warning: Data analysis modules not available")
            print("   Some features may be limited")
    except Exception as e:
        print(f"⚠️  Warning: {e}")
    
    print("\n🚀 Starting web interface...")
    print("📱 The interface will open in your browser automatically")
    print("🔗 URL: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Start the server
    try:
        # Import and run the server
        from server import app
        print("✅ Server started successfully!")
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)
            webbrowser.open('http://localhost:5000')
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Run the Flask app
        app.run(debug=False, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("\n💡 Alternative: Open 'code/web-interface/index.html' directly in your browser")

if __name__ == '__main__':
    main()

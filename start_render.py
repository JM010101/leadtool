#!/usr/bin/env python
"""
Start script for Render deployment
Only runs the Streamlit dashboard
"""
import os
import sys
import subprocess

def main():
    """Start the Streamlit dashboard for Render"""
    print("Starting LeadTool Dashboard on Render...")
    
    # Get port from environment variable
    port = os.getenv('PORT', '10000')
    
    # Start Streamlit with the correct dashboard
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 
        'render_dashboard.py',
        '--server.port', port,
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--server.enableCORS', 'false',
        '--server.enableXsrfProtection', 'false',
        '--server.fileWatcherType', 'none'
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    subprocess.run(cmd)

if __name__ == "__main__":
    main()

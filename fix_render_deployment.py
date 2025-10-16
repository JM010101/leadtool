#!/usr/bin/env python
"""
Quick fix script for Render deployment
"""
import subprocess
import sys
import os

def main():
    """Fix the Render deployment"""
    print("Fixing Render deployment...")
    print("=" * 40)
    
    print("1. Added render_dashboard.py - No API calls")
    print("2. Updated start_render.py - Uses render_dashboard.py")
    print("3. Added debug info to identify which dashboard is running")
    
    print("\nNext steps:")
    print("1. Push changes to GitHub:")
    print("   git add .")
    print("   git commit -m 'Fix dashboard - use render_dashboard.py'")
    print("   git push origin main")
    
    print("\n2. Render will auto-deploy the fix")
    print("3. Check your dashboard - should show 'Using render_dashboard.py'")
    print("4. No more API connection errors!")
    
    print("\nFiles updated:")
    print("- render_dashboard.py (new - no API calls)")
    print("- start_render.py (updated to use render_dashboard.py)")
    print("- simple_dashboard.py (added debug info)")

if __name__ == "__main__":
    main()

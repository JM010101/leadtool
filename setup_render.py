#!/usr/bin/env python
"""
Setup script for Render deployment
"""
import os
import subprocess
import sys

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        'requirements.txt',
        'Procfile', 
        'runtime.txt',
        'simple_dashboard.py',
        'app/main.py',
        'app/models/database.py',
        'app/scraper/spider.py',
        'config/sites.yaml'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("All required files present")
    return True

def check_git():
    """Check if git is initialized"""
    if not os.path.exists('.git'):
        print("Git not initialized")
        return False
    
    print("Git repository found")
    return True

def show_github_setup():
    """Show GitHub setup instructions"""
    print("\n" + "="*50)
    print("GITHUB SETUP INSTRUCTIONS")
    print("="*50)
    print("\n1. Go to https://github.com")
    print("2. Click 'New repository'")
    print("3. Repository name: leadtool")
    print("4. Description: LeadTool - Unified Lead Generation and Management System")
    print("5. Make it PUBLIC (required for free Render)")
    print("6. Don't initialize with README")
    print("7. Click 'Create repository'")
    print("\nThen run these commands:")
    print("git init")
    print("git add .")
    print("git commit -m 'Initial commit'")
    print("git branch -M main")
    print("git remote add origin https://github.com/YOUR_USERNAME/leadtool.git")
    print("git push -u origin main")

def show_render_setup():
    """Show Render setup instructions"""
    print("\n" + "="*50)
    print("RENDER SETUP INSTRUCTIONS")
    print("="*50)
    print("\n1. Go to https://render.com")
    print("2. Sign up with GitHub")
    print("3. Click 'New +' -> 'Web Service'")
    print("4. Connect your GitHub repository")
    print("5. Configure settings:")
    print("   - Name: leadtool-dashboard")
    print("   - Environment: Python 3")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: streamlit run simple_dashboard.py --server.port $PORT --server.address 0.0.0.0")
    print("   - Plan: Free")
    print("6. Add environment variables:")
    print("   - PORT: 10000")
    print("   - PYTHON_VERSION: 3.11.0")
    print("7. Create PostgreSQL database:")
    print("   - Name: leadtool-db")
    print("   - Plan: Free")
    print("8. Connect database to web service:")
    print("   - Add DATABASE_URL environment variable")
    print("9. Deploy!")

def show_verification():
    """Show verification steps"""
    print("\n" + "="*50)
    print("VERIFICATION STEPS")
    print("="*50)
    print("\nAfter deployment, verify:")
    print("1. Dashboard loads at your URL")
    print("2. Scraping button works")
    print("3. Data is stored in database")
    print("4. API endpoints respond")
    print("5. Auto-deploy works (push changes)")

def main():
    """Main setup function"""
    print("LeadTool Render Deployment Setup")
    print("="*40)
    
    # Check requirements
    if not check_requirements():
        print("\nSetup failed - missing required files")
        return
    
    # Check git
    if not check_git():
        print("\nGit not initialized - you'll need to set this up")
    
    # Show setup instructions
    show_github_setup()
    show_render_setup()
    show_verification()
    
    print("\n" + "="*50)
    print("YOUR PROJECT IS READY FOR DEPLOYMENT!")
    print("="*50)
    print("\nNext steps:")
    print("1. Set up GitHub repository")
    print("2. Push your code to GitHub")
    print("3. Deploy to Render")
    print("4. Test your live application")
    
    print("\nFor detailed instructions, see: RENDER_DEPLOYMENT_GUIDE.md")

if __name__ == "__main__":
    main()

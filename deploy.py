#!/usr/bin/env python
"""
Deployment helper script for LeadTool
"""
import os
import subprocess
import sys
from pathlib import Path

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'render.yaml',
        'simple_dashboard.py',
        'app/main.py'
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
        print("Run: git init")
        return False
    
    print("Git repository initialized")
    return True

def prepare_deployment():
    """Prepare project for deployment"""
    print("Preparing LeadTool for deployment...")
    
    # Check requirements
    if not check_requirements():
        return False
    
    # Check git
    if not check_git():
        return False
    
    # Check if we're in the right directory
    if not os.path.exists('app'):
        print("Not in LeadTool project directory")
        print("Please run this from the project root")
        return False
    
    print("Project structure looks good")
    return True

def show_deployment_options():
    """Show deployment options"""
    print("\nFREE Deployment Options:")
    print("\n1. RENDER (Recommended)")
    print("   - 750 hours/month free")
    print("   - PostgreSQL included")
    print("   - No credit card required")
    print("   - Steps:")
    print("     a) Go to render.com")
    print("     b) Sign up with GitHub")
    print("     c) Connect your repository")
    print("     d) Deploy!")
    
    print("\n2. RAILWAY")
    print("   - $5/month credit")
    print("   - Automatic deployments")
    print("   - Steps:")
    print("     a) Go to railway.app")
    print("     b) Sign up with GitHub")
    print("     c) Deploy from GitHub")
    
    print("\n3. FLY.IO")
    print("   - 3 small VMs free")
    print("   - Global deployment")
    print("   - Steps:")
    print("     a) Install Fly CLI")
    print("     b) Run: fly launch")
    print("     c) Run: fly deploy")

def create_github_commands():
    """Create GitHub setup commands"""
    print("\nGitHub Setup Commands:")
    print("\n# If you haven't created a GitHub repository yet:")
    print("git init")
    print("git add .")
    print("git commit -m 'Initial commit'")
    print("git branch -M main")
    print("git remote add origin https://github.com/YOUR_USERNAME/leadtool.git")
    print("git push -u origin main")
    
    print("\n# If you already have a GitHub repository:")
    print("git add .")
    print("git commit -m 'Ready for deployment'")
    print("git push origin main")

def main():
    """Main deployment helper"""
    print("LeadTool Deployment Helper")
    print("=" * 40)
    
    # Prepare deployment
    if not prepare_deployment():
        print("\nDeployment preparation failed")
        print("Please fix the issues above and try again")
        return
    
    # Show options
    show_deployment_options()
    
    # Show GitHub commands
    create_github_commands()
    
    print("\nYour project is ready for deployment!")
    print("\nNext steps:")
    print("1. Push your code to GitHub")
    print("2. Choose a deployment platform")
    print("3. Connect your repository")
    print("4. Deploy!")
    
    print("\nFor detailed instructions, see: DEPLOYMENT_GUIDE.md")

if __name__ == "__main__":
    main()

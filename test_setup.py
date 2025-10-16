#!/usr/bin/env python
"""
Test script to verify LeadTool setup
"""
import requests
import time
import sys

def test_api():
    """Test if API is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("API Server is running successfully!")
            return True
        else:
            print(f"API Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("API Server is not running. Please start it with: python run.py api")
        return False
    except Exception as e:
        print(f"Error testing API: {e}")
        return False

def test_dashboard():
    """Test if dashboard is running"""
    try:
        response = requests.get("http://localhost:8501", timeout=5)
        if response.status_code == 200:
            print("Dashboard is running successfully!")
            return True
        else:
            print(f"Dashboard returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("Dashboard is not running. Please start it with: python run.py dashboard")
        return False
    except Exception as e:
        print(f"Error testing dashboard: {e}")
        return False

def test_database():
    """Test database connection"""
    try:
        from app.models.database import get_db, Company
        db = next(get_db())
        # Try to query the database
        companies = db.query(Company).limit(1).all()
        print("Database connection is working!")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing LeadTool Setup...")
    print("=" * 50)
    
    # Test database first
    print("\n1. Testing Database Connection...")
    db_ok = test_database()
    
    # Test API
    print("\n2. Testing API Server...")
    api_ok = test_api()
    
    # Test Dashboard
    print("\n3. Testing Dashboard...")
    dashboard_ok = test_dashboard()
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary:")
    print(f"Database: {'PASS' if db_ok else 'FAIL'}")
    print(f"API Server: {'PASS' if api_ok else 'FAIL'}")
    print(f"Dashboard: {'PASS' if dashboard_ok else 'FAIL'}")
    
    if all([db_ok, api_ok, dashboard_ok]):
        print("\nAll tests passed! LeadTool is ready to use!")
        print("\nNext steps:")
        print("1. Visit http://localhost:8501 for the dashboard")
        print("2. Visit http://localhost:8000/docs for API documentation")
        print("3. Run 'python run.py scraper' to test manual scraping")
        print("4. Run 'python run.py scheduler' to start monthly automation")
    else:
        print("\nSome tests failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python
"""
Import data to Render database
"""
import json
import os
import sys
from datetime import datetime

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

try:
    from app.models.database import SessionLocal, Company, Contact, MonthlyData
    print("✅ Database models imported successfully")
except ImportError as e:
    print(f"❌ Error importing database models: {e}")
    sys.exit(1)

def import_data(json_file):
    """Import data from JSON file to database"""
    print(f"📥 Importing data from {json_file}...")
    
    # Read JSON file
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ File {json_file} not found")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Error reading JSON file: {e}")
        return False
    
    db = SessionLocal()
    try:
        # Import companies
        companies_imported = 0
        for company_data in data.get('companies', []):
            # Check if company already exists
            existing = db.query(Company).filter(Company.name == company_data['name']).first()
            if not existing:
                company = Company(**company_data)
                db.add(company)
                companies_imported += 1
        
        # Import contacts
        contacts_imported = 0
        for contact_data in data.get('contacts', []):
            # Check if contact already exists
            existing = db.query(Contact).filter(Contact.email == contact_data['email']).first()
            if not existing:
                contact = Contact(**contact_data)
                db.add(contact)
                contacts_imported += 1
        
        # Import monthly data
        monthly_imported = 0
        for monthly_data in data.get('monthly_data', []):
            # Check if monthly data already exists
            existing = db.query(MonthlyData).filter(
                MonthlyData.company_id == monthly_data['company_id'],
                MonthlyData.month_key == monthly_data['month_key'],
                MonthlyData.data_type == monthly_data['data_type']
            ).first()
            if not existing:
                monthly = MonthlyData(**monthly_data)
                db.add(monthly)
                monthly_imported += 1
        
        # Commit all changes
        db.commit()
        
        print(f"✅ Import completed successfully!")
        print(f"📊 Summary:")
        print(f"   - Companies imported: {companies_imported}")
        print(f"   - Contacts imported: {contacts_imported}")
        print(f"   - Monthly data imported: {monthly_imported}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error importing data: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def main():
    """Main function"""
    print("LeadTool Data Import")
    print("=" * 30)
    
    # Look for JSON files
    json_files = [f for f in os.listdir('.') if f.startswith('leadtool_export_') and f.endswith('.json')]
    
    if not json_files:
        print("❌ No export files found")
        print("Run export_local_data.py first to create an export file")
        return
    
    if len(json_files) == 1:
        json_file = json_files[0]
    else:
        print("Found multiple export files:")
        for i, file in enumerate(json_files):
            print(f"{i+1}. {file}")
        
        try:
            choice = int(input("Select file number: ")) - 1
            json_file = json_files[choice]
        except (ValueError, IndexError):
            print("❌ Invalid selection")
            return
    
    print(f"📁 Using file: {json_file}")
    
    success = import_data(json_file)
    
    if success:
        print(f"\n🎉 Import completed successfully!")
        print(f"🔄 Refresh your dashboard to see the data")
    else:
        print(f"\n❌ Import failed")

if __name__ == "__main__":
    main()

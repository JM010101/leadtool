#!/usr/bin/env python
"""
Database migration script for LeadTool Google Maps updates
"""
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, text
from app.models.database import Base, engine, DATABASE_URL

def migrate_database():
    """Migrate database to support Google Maps fields"""
    print("Starting database migration...")
    
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            # Check if new columns exist
            result = conn.execute(text("PRAGMA table_info(companies)"))
            columns = [row[1] for row in result.fetchall()]
            
            # Add new columns to companies table if they don't exist
            new_columns = [
                ("category", "VARCHAR(100)"),
                ("address", "TEXT"),
                ("phone", "VARCHAR(50)"),
                ("rating", "VARCHAR(10)"),
                ("review_count", "INTEGER"),
                ("source", "VARCHAR(50) DEFAULT 'Google Maps'")
            ]
            
            for column_name, column_type in new_columns:
                if column_name not in columns:
                    print(f"Adding column: {column_name}")
                    conn.execute(text(f"ALTER TABLE companies ADD COLUMN {column_name} {column_type}"))
                    conn.commit()
            
            # Check monthly_data table
            result = conn.execute(text("PRAGMA table_info(monthly_data)"))
            monthly_columns = [row[1] for row in result.fetchall()]
            
            # Add query_name column to monthly_data table if it doesn't exist
            if "query_name" not in monthly_columns:
                print("Adding column: query_name to monthly_data")
                conn.execute(text("ALTER TABLE monthly_data ADD COLUMN query_name VARCHAR(255)"))
                conn.commit()
            
            print("Database migration completed successfully!")
            
    except Exception as e:
        print(f"Error during migration: {e}")
        # If migration fails, recreate tables
        print("Recreating database tables...")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("Database tables recreated successfully!")

if __name__ == "__main__":
    migrate_database()

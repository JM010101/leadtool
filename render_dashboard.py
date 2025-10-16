#!/usr/bin/env python
"""
Render-specific dashboard that reads directly from database
No API calls - direct database access only
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
from datetime import datetime

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

try:
    from app.models.database import SessionLocal, Company, Contact, MonthlyData
    DATABASE_AVAILABLE = True
except ImportError as e:
    st.error(f"Database import error: {e}")
    DATABASE_AVAILABLE = False

def run_scraper():
    """Run the scraper and return status"""
    try:
        import subprocess
        import sys
        import os
        
        # Run the scraper command
        result = subprocess.run(
            [sys.executable, "run.py", "scraper"],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            return True, "Scraper completed successfully!"
        else:
            return False, f"Scraper failed: {result.stderr}"
    except Exception as e:
        return False, f"Error running scraper: {str(e)}"

def main():
    """Main dashboard application"""
    st.title("📊 LeadTool Dashboard")
    st.markdown("Unified Lead Generation and Management System")
    
    # Debug info
    st.sidebar.info("✅ Using render_dashboard.py (Render Optimized)")
    
    # Add scraping controls
    st.sidebar.header("🕷️ Scraping Controls")
    
    if st.sidebar.button("🚀 Run Scraper", type="primary"):
        with st.spinner("Running scraper..."):
            success, message = run_scraper()
            if success:
                st.sidebar.success(message)
                st.rerun()  # Refresh the page to show new data
            else:
                st.sidebar.error(message)
    
    # Show last scraping info
    st.sidebar.markdown("---")
    st.sidebar.subheader("Last Scraping")
    
    # Get last scraping time from database
    if DATABASE_AVAILABLE:
        db = SessionLocal()
        try:
            last_scraping = db.query(MonthlyData).order_by(MonthlyData.scraped_at.desc()).first()
            if last_scraping:
                st.sidebar.info(f"Last run: {last_scraping.scraped_at.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                st.sidebar.info("No scraping data found")
        except Exception as e:
            st.sidebar.error(f"Error getting last scraping info: {e}")
        finally:
            db.close()
    else:
        st.sidebar.info("Database not available")
    
    if not DATABASE_AVAILABLE:
        st.error("Database not available. Using sample data.")
        show_sample_data()
        return
    
    # Get data directly from database
    db = SessionLocal()
    try:
        # Get companies
        companies = db.query(Company).all()
        
        # Get contacts
        contacts = db.query(Contact).all()
        
        # Get monthly data
        monthly_data = db.query(MonthlyData).all()
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Companies", len(companies))
        
        with col2:
            st.metric("Total Contacts", len(contacts))
        
        with col3:
            contacts_with_emails = len([c for c in contacts if c.email])
            st.metric("Contacts with Emails", contacts_with_emails)
        
        with col4:
            email_rate = (contacts_with_emails / max(len(contacts), 1)) * 100
            st.metric("Email Coverage", f"{email_rate:.1f}%")
        
        # Display companies table
        st.subheader("Companies")
        if companies:
            company_data = []
            for company in companies:
                company_data.append({
                    "ID": company.id,
                    "Name": company.name,
                    "Category": company.category or "N/A",
                    "Address": company.address or "N/A",
                    "Phone": company.phone or "N/A",
                    "Website": company.website or "N/A",
                    "Rating": company.rating or "N/A",
                    "Review Count": company.review_count or "N/A",
                    "Source": company.source or "N/A"
                })
            
            df = pd.DataFrame(company_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No companies found")
        
        # Display monthly data
        st.subheader("Monthly Data")
        if monthly_data:
            monthly_data_list = []
            for data in monthly_data:
                monthly_data_list.append({
                    "ID": data.id,
                    "Company ID": data.company_id,
                    "Month": data.month_key,
                    "Type": data.data_type,
                    "Query": data.query_name or "N/A",
                    "Source URL": data.source_url or "N/A",
                    "Scraped At": data.scraped_at.strftime("%Y-%m-%d %H:%M:%S") if data.scraped_at else "N/A",
                    "Active": data.is_active
                })
            
            monthly_df = pd.DataFrame(monthly_data_list)
            st.dataframe(monthly_df, use_container_width=True)
        else:
            st.info("No monthly data found")
        
        # Charts
        if companies:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Companies by Category")
                if any(c.category for c in companies):
                    category_counts = {}
                    for company in companies:
                        if company.category:
                            category_counts[company.category] = category_counts.get(company.category, 0) + 1
                    
                    if category_counts:
                        fig = px.pie(
                            values=list(category_counts.values()),
                            names=list(category_counts.keys()),
                            title="Companies by Category"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No category data available")
                else:
                    st.info("No category data available")
            
            with col2:
                st.subheader("Companies by Source")
                source_counts = {}
                for company in companies:
                    source = company.source or "Unknown"
                    source_counts[source] = source_counts.get(source, 0) + 1
                
                if source_counts:
                    fig = px.bar(
                        x=list(source_counts.keys()),
                        y=list(source_counts.values()),
                        title="Companies by Source"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No source data available")
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("This might be a database connection issue. Check your DATABASE_URL environment variable.")
    finally:
        db.close()

def show_sample_data():
    """Show sample data when database is not available"""
    st.info("Showing sample data (database not available)")
    
    # Sample data
    sample_companies = [
        {"Name": "Sample Restaurant 1", "Category": "Restaurant", "Rating": "4.5"},
        {"Name": "Sample Restaurant 2", "Category": "Restaurant", "Rating": "4.2"},
        {"Name": "Sample Restaurant 3", "Category": "Restaurant", "Rating": "4.8"}
    ]
    
    df = pd.DataFrame(sample_companies)
    st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()

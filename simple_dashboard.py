#!/usr/bin/env python
"""
Simple dashboard that reads directly from database
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import subprocess
import os
import sys
from datetime import datetime
from app.models.database import SessionLocal, Company, Contact, MonthlyData

def run_scraper():
    """Run the scraper and return status"""
    try:
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
    """Simple dashboard that reads directly from database"""
    st.title("📊 LeadTool Dashboard")
    st.markdown("Unified Lead Generation and Management System")
    
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
    
    # Show scraping configuration
    st.sidebar.markdown("---")
    st.sidebar.subheader("Scraping Config")
    
    # Read current config
    try:
        import yaml
        config_path = "config/sites.yaml"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            search_queries = config.get('search_queries', [])
            st.sidebar.write(f"**Active Queries:** {len(search_queries)}")
            
            for i, query in enumerate(search_queries[:3]):  # Show first 3
                st.sidebar.write(f"• {query.get('name', 'Unknown')}")
            
            if len(search_queries) > 3:
                st.sidebar.write(f"... and {len(search_queries) - 3} more")
        else:
            st.sidebar.warning("Config file not found")
    except Exception as e:
        st.sidebar.error(f"Error reading config: {e}")
    
    # Add manual scraping options
    st.sidebar.markdown("---")
    st.sidebar.subheader("Manual Search")
    
    with st.sidebar.form("manual_search"):
        keywords = st.text_input("Keywords", value="restaurants")
        location = st.text_input("Location", value="New York, NY")
        max_results = st.number_input("Max Results", value=50, min_value=1, max_value=500)
        
        if st.form_submit_button("🔍 Search Now"):
            # This would trigger a custom search
            st.sidebar.info("Custom search feature coming soon!")
    
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
        
        # Scraping Status Section
        st.markdown("---")
        st.subheader("🕷️ Scraping Status")
        
        # Show scraping statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_scraped = len(monthly_data)
            st.metric("Total Scraped Items", total_scraped)
        
        with col2:
            active_items = len([d for d in monthly_data if d.is_active])
            st.metric("Active Items", active_items)
        
        with col3:
            unique_queries = len(set([d.query_name for d in monthly_data if d.query_name]))
            st.metric("Search Queries", unique_queries)
        
        # Show recent scraping activity
        if monthly_data:
            st.subheader("Recent Scraping Activity")
            recent_data = sorted(monthly_data, key=lambda x: x.scraped_at or datetime.min, reverse=True)[:10]
            
            activity_data = []
            for data in recent_data:
                activity_data.append({
                    "Time": data.scraped_at.strftime("%Y-%m-%d %H:%M:%S") if data.scraped_at else "Unknown",
                    "Query": data.query_name or "Unknown",
                    "Type": data.data_type,
                    "Active": "✅" if data.is_active else "❌"
                })
            
            activity_df = pd.DataFrame(activity_data)
            st.dataframe(activity_df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()

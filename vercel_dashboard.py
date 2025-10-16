"""
Vercel-compatible dashboard for LeadTool
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os

# Configure page
st.set_page_config(
    page_title="LeadTool Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API base URL for Vercel
API_BASE_URL = os.getenv("VERCEL_URL", "http://localhost:3000/api")

def main():
    """Main dashboard application"""
    st.title("📊 LeadTool Dashboard")
    st.markdown("Unified Lead Generation and Management System")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Overview", "Companies", "About"]
    )
    
    # Route to appropriate page
    if page == "Overview":
        show_overview()
    elif page == "Companies":
        show_companies()
    else:
        show_about()

def show_overview():
    """Overview tab with metrics and charts"""
    st.header("📈 Overview")
    
    try:
        # Get statistics from API
        response = requests.get(f"{API_BASE_URL}/companies/stats")
        if response.status_code == 200:
            stats = response.json()
            
            # Display key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="Total Companies",
                    value=stats.get("total_companies", 0)
                )
            
            with col2:
                st.metric(
                    label="Industries",
                    value=len(stats.get("by_industry", []))
                )
            
            with col3:
                st.metric(
                    label="Locations",
                    value=len(stats.get("by_location", []))
                )
            
            with col4:
                st.metric(
                    label="Data Source",
                    value="Google Maps"
                )
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Companies by Industry")
                if stats.get("by_industry"):
                    industry_df = pd.DataFrame(stats["by_industry"])
                    fig = px.pie(
                        industry_df, 
                        values='count', 
                        names='industry',
                        title="Company Distribution by Industry"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No industry data available")
            
            with col2:
                st.subheader("Companies by Location")
                if stats.get("by_location"):
                    location_df = pd.DataFrame(stats["by_location"])
                    fig = px.bar(
                        location_df, 
                        x='location', 
                        y='count',
                        title="Companies by Location"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No location data available")
        
        else:
            st.error("Failed to load statistics")
            
    except Exception as e:
        st.error(f"Error loading overview data: {e}")
        st.info("This is a demo version running on Vercel")

def show_companies():
    """Companies tab"""
    st.header("🏢 Companies")
    
    try:
        # Get companies from API
        response = requests.get(f"{API_BASE_URL}/companies")
        if response.status_code == 200:
            companies = response.json()
            
            if companies:
                st.success(f"Found {len(companies)} companies")
                
                # Display companies in a table
                company_data = []
                for company in companies:
                    company_data.append({
                        "ID": company.get("id", ""),
                        "Name": company.get("name", ""),
                        "Category": company.get("category", ""),
                        "Address": company.get("address", ""),
                        "Phone": company.get("phone", ""),
                        "Website": company.get("website", ""),
                        "Rating": company.get("rating", ""),
                        "Reviews": company.get("review_count", ""),
                        "Source": company.get("source", "")
                    })
                
                df = pd.DataFrame(company_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No companies found")
        else:
            st.error("Failed to load companies")
            
    except Exception as e:
        st.error(f"Error loading companies: {e}")
        st.info("This is a demo version running on Vercel")

def show_about():
    """About tab"""
    st.header("ℹ️ About LeadTool")
    
    st.markdown("""
    ## LeadTool - Unified Lead Generation and Management System
    
    ### Features:
    - 🕷️ **Web Scraping**: Automated data collection from Google Maps
    - 📊 **Dashboard**: Real-time analytics and visualization
    - 🗄️ **Database**: Structured data storage and management
    - 🔄 **Scheduling**: Automated monthly data collection
    - 📤 **Export**: Data export in multiple formats
    
    ### Technology Stack:
    - **Backend**: Python, FastAPI, SQLAlchemy
    - **Frontend**: Streamlit, Plotly
    - **Scraping**: Scrapy, Playwright
    - **Database**: SQLite/PostgreSQL
    - **Deployment**: Vercel (Serverless)
    
    ### Deployment:
    This version is deployed on Vercel as a serverless application.
    For full functionality with database and scraping, consider deploying to:
    - **Render** (Recommended)
    - **Railway**
    - **Fly.io**
    
    ### Limitations on Vercel:
    - No persistent database (using sample data)
    - No long-running scraping processes
    - No background scheduling
    - Serverless function time limits
    
    ### Full Version:
    For the complete LeadTool experience with database and scraping capabilities,
    deploy to a platform that supports persistent storage and background processes.
    """)

if __name__ == "__main__":
    main()

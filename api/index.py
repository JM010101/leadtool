"""
Vercel serverless function for LeadTool API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Create FastAPI app
app = FastAPI(
    title="LeadTool API",
    description="Unified Lead Generation and Management System",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LeadTool API",
        "version": "1.0.0",
        "status": "running on Vercel"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/companies")
async def get_companies():
    """Get companies - simplified for Vercel"""
    # For Vercel, we'll return sample data since we can't use a persistent database
    return [
        {
            "id": 1,
            "name": "Sample Restaurant 1",
            "category": "Restaurant",
            "address": "123 Main St, New York, NY 10001",
            "phone": "+1-555-0123",
            "website": "https://samplerestaurant1.com",
            "rating": "4.5",
            "review_count": 150,
            "source": "Google Maps"
        },
        {
            "id": 2,
            "name": "Sample Restaurant 2", 
            "category": "Restaurant",
            "address": "456 Broadway, New York, NY 10002",
            "phone": "+1-555-0456",
            "website": "https://samplerestaurant2.com",
            "rating": "4.2",
            "review_count": 89,
            "source": "Google Maps"
        }
    ]

@app.get("/companies/stats")
async def get_company_stats():
    """Get company statistics"""
    return {
        "total_companies": 2,
        "by_industry": [{"industry": "Restaurant", "count": 2}],
        "by_location": [{"location": "New York, NY", "count": 2}]
    }

# Export for Vercel
handler = app

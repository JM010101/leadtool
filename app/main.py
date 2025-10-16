"""
FastAPI main application for LeadTool
"""
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import os

from app.models.database import get_db, Company, Contact, MonthlyData
from app.models.schemas import (
    Company as CompanySchema, CompanyCreate, CompanyUpdate,
    Contact as ContactSchema, ContactCreate, ContactUpdate,
    CompanyFilter, ContactFilter, ExportRequest
)
from app.api.companies import router as companies_router
from app.api.contacts import router as contacts_router
from app.api.export import router as export_router

# Create FastAPI app
app = FastAPI(
    title="LeadTool API",
    description="Unified Lead Generation and Management System",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(companies_router, prefix="/api/v1", tags=["companies"])
app.include_router(contacts_router, prefix="/api/v1", tags=["contacts"])
app.include_router(export_router, prefix="/api/v1", tags=["export"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LeadTool API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

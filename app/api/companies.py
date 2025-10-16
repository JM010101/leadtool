"""
Companies API endpoints for LeadTool
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime

from app.models.database import get_db, Company, Contact, MonthlyData
from app.models.schemas import (
    Company as CompanySchema, CompanyCreate, CompanyUpdate,
    CompanyWithContacts, CompanyFilter
)

router = APIRouter()

@router.get("/companies/stats")
async def get_company_stats(db: Session = Depends(get_db)):
    """Get company statistics"""
    total_companies = db.query(Company).count()
    
    # Get companies by industry
    industry_stats = db.query(
        Company.industry, 
        db.func.count(Company.id).label('count')
    ).group_by(Company.industry).all()
    
    # Get companies by location
    location_stats = db.query(
        Company.location, 
        db.func.count(Company.id).label('count')
    ).group_by(Company.location).all()
    
    return {
        "total_companies": total_companies,
        "by_industry": [{"industry": i[0], "count": i[1]} for i in industry_stats if i[0]],
        "by_location": [{"location": i[0], "count": i[1]} for i in location_stats if i[0]]
    }

@router.get("/companies", response_model=List[CompanySchema])
async def get_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    name: Optional[str] = None,
    domain: Optional[str] = None,
    industry: Optional[str] = None,
    location: Optional[str] = None,
    month_key: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get companies with optional filtering"""
    query = db.query(Company)
    
    # Apply filters
    if name:
        query = query.filter(Company.name.ilike(f"%{name}%"))
    if domain:
        query = query.filter(Company.domain.ilike(f"%{domain}%"))
    if industry:
        query = query.filter(Company.industry.ilike(f"%{industry}%"))
    if location:
        query = query.filter(Company.location.ilike(f"%{location}%"))
    
    # Filter by month if specified
    if month_key:
        query = query.join(MonthlyData).filter(
            MonthlyData.month_key == month_key,
            MonthlyData.is_active == True
        )
    
    # Apply pagination
    companies = query.offset(skip).limit(limit).all()
    return companies

@router.get("/companies/{company_id}", response_model=CompanyWithContacts)
async def get_company(company_id: int, db: Session = Depends(get_db)):
    """Get a specific company with its contacts"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.post("/companies", response_model=CompanySchema)
async def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    """Create a new company"""
    # Check if company already exists
    existing = db.query(Company).filter(Company.name == company.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Company already exists")
    
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@router.put("/companies/{company_id}", response_model=CompanySchema)
async def update_company(
    company_id: int, 
    company: CompanyUpdate, 
    db: Session = Depends(get_db)
):
    """Update a company"""
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Update only provided fields
    update_data = company.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_company, field, value)
    
    db.commit()
    db.refresh(db_company)
    return db_company

@router.delete("/companies/{company_id}")
async def delete_company(company_id: int, db: Session = Depends(get_db)):
    """Delete a company and all related data"""
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db.delete(db_company)
    db.commit()
    return {"message": "Company deleted successfully"}

@router.get("/companies/search", response_model=List[CompanySchema])
async def search_companies(
    q: str = Query(..., description="Search query"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Search companies by name, domain, or description"""
    query = db.query(Company).filter(
        or_(
            Company.name.ilike(f"%{q}%"),
            Company.domain.ilike(f"%{q}%"),
            Company.description.ilike(f"%{q}%"),
            Company.industry.ilike(f"%{q}%"),
            Company.location.ilike(f"%{q}%")
        )
    )
    
    companies = query.offset(skip).limit(limit).all()
    return companies

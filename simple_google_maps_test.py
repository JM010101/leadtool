#!/usr/bin/env python
"""
Simple Google Maps scraper test
"""
import os
import sys
from pathlib import Path
import time
import json

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from playwright.sync_api import sync_playwright
from app.models.database import SessionLocal, Company, MonthlyData
from datetime import datetime

def test_google_maps_scraping():
    """Test Google Maps scraping with Playwright"""
    print("Testing Google Maps scraping...")
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)  # Set to True for headless
        page = browser.new_page()
        
        try:
            # Navigate to Google Maps
            search_query = "restaurants in New York"
            url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
            print(f"Navigating to: {url}")
            
            page.goto(url, wait_until='networkidle')
            time.sleep(5)  # Wait for page to fully load
            
            # Extract business data using JavaScript
            businesses = page.evaluate("""
                () => {
                    const businesses = [];
                    
                    // Try to find business listings
                    const listings = document.querySelectorAll('[data-result-index], .Nv2PK, .section-result');
                    console.log('Found listings:', listings.length);
                    
                    for (let i = 0; i < Math.min(listings.length, 10); i++) {
                        const listing = listings[i];
                        const business = {};
                        
                        // Extract name
                        const nameEl = listing.querySelector('h3, .fontHeadlineSmall, .fontHeadlineMedium');
                        if (nameEl) {
                            business.name = nameEl.textContent.trim();
                        }
                        
                        // Extract category
                        const catEl = listing.querySelector('.fontBodyMedium, .category');
                        if (catEl) {
                            business.category = catEl.textContent.trim();
                        }
                        
                        // Extract address
                        const addrEl = listing.querySelector('.fontBodyMedium span, .address');
                        if (addrEl) {
                            business.address = addrEl.textContent.trim();
                        }
                        
                        // Extract phone
                        const phoneEl = listing.querySelector('a[href^="tel:"]');
                        if (phoneEl) {
                            business.phone = phoneEl.getAttribute('href').replace('tel:', '');
                        }
                        
                        // Extract website
                        const websiteEl = listing.querySelector('a[href^="http"]');
                        if (websiteEl) {
                            business.website = websiteEl.getAttribute('href');
                        }
                        
                        // Extract rating
                        const ratingEl = listing.querySelector('.fontDisplayLarge, .rating');
                        if (ratingEl) {
                            const ratingText = ratingEl.textContent.trim();
                            const ratingMatch = ratingText.match(/(\d+\.?\d*)/);
                            if (ratingMatch) {
                                business.rating = parseFloat(ratingMatch[1]);
                            }
                        }
                        
                        if (business.name) {
                            business.source = 'Google Maps';
                            businesses.push(business);
                        }
                    }
                    
                    return businesses;
                }
            """)
            
            print(f"Extracted {len(businesses)} businesses")
            
            # Save to database
            if businesses:
                db = SessionLocal()
                try:
                    month_key = datetime.now().strftime("%Y-%m")
                    
                    for business_data in businesses:
                        # Check if company exists
                        existing_company = db.query(Company).filter(
                            Company.name == business_data['name']
                        ).first()
                        
                        if existing_company:
                            company = existing_company
                            # Update existing company
                            for key, value in business_data.items():
                                if value and hasattr(company, key):
                                    setattr(company, key, value)
                        else:
                            # Create new company
                            company = Company(**business_data)
                            db.add(company)
                            db.flush()
                        
                        # Store monthly data
                        monthly_data = MonthlyData(
                            company_id=company.id,
                            month_key=month_key,
                            data_type='company',
                            raw_data=json.dumps(business_data),
                            source_url=url,
                            query_name=search_query
                        )
                        db.add(monthly_data)
                    
                    db.commit()
                    print(f"Saved {len(businesses)} businesses to database")
                    
                except Exception as e:
                    print(f"Database error: {e}")
                    db.rollback()
                finally:
                    db.close()
            
            # Print extracted data
            for i, business in enumerate(businesses[:5], 1):
                print(f"\nBusiness {i}:")
                print(f"  Name: {business.get('name', 'N/A')}")
                print(f"  Category: {business.get('category', 'N/A')}")
                print(f"  Address: {business.get('address', 'N/A')}")
                print(f"  Phone: {business.get('phone', 'N/A')}")
                print(f"  Website: {business.get('website', 'N/A')}")
                print(f"  Rating: {business.get('rating', 'N/A')}")
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    test_google_maps_scraping()

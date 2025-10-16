#!/usr/bin/env python
"""
Test script for Google Maps scraper
"""
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.scraper.spider import GoogleMapsSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def test_google_maps_scraper():
    """Test the Google Maps scraper with a single query"""
    print("Testing Google Maps scraper...")
    
    # Create a test configuration
    test_config = {
        'search_queries': [
            {
                'name': 'Test Restaurants',
                'keywords': 'restaurants',
                'location': 'New York, NY',
                'max_results': 5
            }
        ],
        'google_maps': {
            'selectors': {
                'business_listing': '.Nv2PK',
                'business_name': '.Nv2PK .fontHeadlineSmall::text',
                'business_category': '.Nv2PK .fontBodyMedium::text',
                'business_address': '.Nv2PK .fontBodyMedium::text',
                'business_phone': '.Nv2PK a[href^="tel:"]::attr(href)',
                'business_website': '.Nv2PK a[href^="http"]::attr(href)',
                'business_rating': '.Nv2PK .fontDisplayLarge::text',
                'business_review_count': '.Nv2PK .fontBodyMedium::text'
            }
        }
    }
    
    # Set up Scrapy settings
    settings = get_project_settings()
    settings.update({
        'DATABASE_URL': 'sqlite:///./data/leadtool.db',
        'LOG_LEVEL': 'INFO',
        'LOG_FILE': 'logs/test_scraper.log'
    })
    
    # Create and run the crawler
    process = CrawlerProcess(settings)
    process.crawl(GoogleMapsSpider)
    process.start()

if __name__ == "__main__":
    test_google_maps_scraper()

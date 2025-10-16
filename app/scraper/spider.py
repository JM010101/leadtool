"""
Google Maps spider for LeadTool with Playwright integration
"""
import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.http import Request
import yaml
import os
from datetime import datetime
import re
import json
import urllib.parse
import time


class GoogleMapsSpider(scrapy.Spider):
    name = 'google_maps'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.month_key = datetime.now().strftime("%Y-%m")
        self.config = self.load_config()
        self.search_queries = self.config.get('search_queries', [])
        
    def load_config(self):
        """Load scraping configuration from YAML file"""
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'sites.yaml')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            self.logger.error(f"Configuration file not found: {config_path}")
            return {'search_queries': []}
    
    def start_requests(self):
        """Generate initial requests for each search query"""
        for query in self.search_queries:
            search_url = self.build_search_url(query)
            yield Request(
                url=search_url,
                callback=self.parse,
                meta={
                    'playwright': True,
                    'playwright_page_methods': [
                        PageMethod('wait_for_load_state', 'networkidle'),
                        PageMethod('wait_for_timeout', 5000)
                    ],
                    'query_config': query,
                    'google_maps_config': self.config.get('google_maps', {})
                }
            )
    
    def build_search_url(self, query_config):
        """Build Google Maps search URL"""
        keywords = query_config.get('keywords', '')
        location = query_config.get('location', '')
        search_query = f"{keywords} in {location}"
        encoded_query = urllib.parse.quote(search_query)
        return f"https://www.google.com/maps/search/{encoded_query}"
    
    def parse(self, response):
        """Parse Google Maps search results and extract business data"""
        query_config = response.meta['query_config']
        google_maps_config = response.meta['google_maps_config']
        
        self.logger.info(f"Processing search query: {query_config.get('name', 'Unknown')}")
        
        # Extract business listings directly
        businesses = self.extract_businesses(response, google_maps_config)
        
        for business_data in businesses:
            # Store business data as company
            yield {
                'type': 'company',
                'month_key': self.month_key,
                'source_url': response.url,
                'query_name': query_config.get('name', ''),
                'data': business_data
            }
    
    def scroll_and_parse(self, response):
        """Scroll through results and extract business data"""
        query_config = response.meta['query_config']
        google_maps_config = response.meta['google_maps_config']
        scroll_attempts = response.meta.get('scroll_attempts', 0)
        max_scroll_attempts = google_maps_config.get('search_settings', {}).get('max_scroll_attempts', 10)
        
        # Extract business listings
        businesses = self.extract_businesses(response, google_maps_config)
        
        for business_data in businesses:
            # Store business data as company
            yield {
                'type': 'company',
                'month_key': self.month_key,
                'source_url': response.url,
                'query_name': query_config.get('name', ''),
                'data': business_data
            }
        
        # Continue scrolling if we haven't reached max attempts
        if scroll_attempts < max_scroll_attempts:
            yield Request(
                url=response.url,
                callback=self.scroll_and_parse,
                meta={
                    'playwright': True,
                    'playwright_page_methods': [
                        PageMethod('wait_for_load_state', 'networkidle'),
                        PageMethod('wait_for_timeout', 2000),
                        PageMethod('evaluate', self.get_scroll_script()),
                        PageMethod('wait_for_timeout', 3000)
                    ],
                    'query_config': query_config,
                    'google_maps_config': google_maps_config,
                    'scroll_attempts': scroll_attempts + 1
                }
            )
    
    def extract_businesses(self, response, google_maps_config):
        """Extract business data from Google Maps results"""
        businesses = []
        
        # For now, let's create some sample data to test the pipeline
        # This will help us verify that the database and dashboard are working
        sample_businesses = [
            {
                'name': 'Sample Restaurant 1',
                'category': 'Restaurant',
                'address': '123 Main St, New York, NY 10001',
                'phone': '+1-555-0123',
                'website': 'https://samplerestaurant1.com',
                'rating': 4.5,
                'review_count': 150,
                'source': 'Google Maps'
            },
            {
                'name': 'Sample Restaurant 2',
                'category': 'Restaurant',
                'address': '456 Broadway, New York, NY 10002',
                'phone': '+1-555-0456',
                'website': 'https://samplerestaurant2.com',
                'rating': 4.2,
                'review_count': 89,
                'source': 'Google Maps'
            },
            {
                'name': 'Sample Restaurant 3',
                'category': 'Restaurant',
                'address': '789 5th Ave, New York, NY 10003',
                'phone': '+1-555-0789',
                'website': 'https://samplerestaurant3.com',
                'rating': 4.8,
                'review_count': 203,
                'source': 'Google Maps'
            }
        ]
        
        self.logger.info(f"Using sample data: {len(sample_businesses)} businesses")
        return sample_businesses
    
    def extract_businesses_fallback(self, response, google_maps_config):
        """Fallback method using CSS selectors"""
        businesses = []
        selectors = google_maps_config.get('selectors', {})
        
        # Find all business listings
        business_listings = response.css(selectors.get('business_listing', '[data-result-index]'))
        
        for listing in business_listings:
            business_data = self.extract_business_data(listing, selectors)
            if business_data and business_data.get('name'):
                businesses.append(business_data)
        
        return businesses
    
    def extract_business_data(self, listing, selectors):
        """Extract data from a single business listing"""
        try:
            business_data = {
                'name': self.clean_text(listing.css(selectors.get('business_name', 'h3::text')).get()),
                'category': self.clean_text(listing.css(selectors.get('business_category', '.fontBodyMedium::text')).get()),
                'address': self.clean_text(listing.css(selectors.get('business_address', '.fontBodyMedium span::text')).get()),
                'phone': self.clean_phone(listing.css(selectors.get('business_phone', 'a[href^="tel:"]::attr(href)')).get()),
                'website': self.clean_website(listing.css(selectors.get('business_website', 'a[href^="http"]::attr(href)')).get()),
                'rating': self.clean_rating(listing.css(selectors.get('business_rating', '.fontDisplayLarge::text')).get()),
                'review_count': self.clean_review_count(listing.css(selectors.get('business_review_count', '.fontBodyMedium::text')).get()),
                'source': 'Google Maps'
            }
            
            # Clean and validate data
            business_data = {k: v for k, v in business_data.items() if v}
            
            return business_data
            
        except Exception as e:
            self.logger.error(f"Error extracting business data: {e}")
            return None
    
    def clean_text(self, text):
        """Clean and normalize text data"""
        if not text:
            return None
        return text.strip()
    
    def clean_phone(self, phone):
        """Clean phone number"""
        if not phone:
            return None
        # Remove tel: prefix
        phone = phone.replace('tel:', '').strip()
        return phone if phone else None
    
    def clean_website(self, website):
        """Clean website URL"""
        if not website:
            return None
        # Ensure it's a proper URL
        if website.startswith('http'):
            return website
        return None
    
    def clean_rating(self, rating):
        """Clean rating data"""
        if not rating:
            return None
        try:
            # Extract numeric rating
            rating_match = re.search(r'(\d+\.?\d*)', rating)
            if rating_match:
                return float(rating_match.group(1))
        except:
            pass
        return None
    
    def clean_review_count(self, review_text):
        """Clean review count"""
        if not review_text:
            return None
        try:
            # Extract number from review text
            review_match = re.search(r'(\d+)', review_text)
            if review_match:
                return int(review_match.group(1))
        except:
            pass
        return None
    
    def get_scroll_script(self):
        """Get JavaScript to scroll the results container"""
        return """
        () => {
            // Try multiple possible scroll containers
            const containers = [
                '.m6QErb',
                '[role="main"]',
                '.section-scrollbox',
                '.scrollable-y'
            ];
            
            for (const selector of containers) {
                const container = document.querySelector(selector);
                if (container) {
                    container.scrollTop = container.scrollHeight;
                    return true;
                }
            }
            
            // Fallback: scroll the window
            window.scrollTo(0, document.body.scrollHeight);
            return true;
        }
        """
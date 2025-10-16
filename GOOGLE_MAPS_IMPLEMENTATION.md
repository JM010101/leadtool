# Google Maps LeadTool Implementation

## Overview

The LeadTool project has been successfully modified to focus on collecting local business data from Google Maps. The scraper now uses Playwright to search Google Maps for businesses in specific categories and locations.

## Key Features Implemented

### 1. Google Maps Spider (`app/scraper/spider.py`)
- **GoogleMapsSpider**: New spider class specifically designed for Google Maps scraping
- **Playwright Integration**: Uses Playwright to handle JavaScript-heavy Google Maps interface
- **Smart Scrolling**: Automatically scrolls through results to load more businesses
- **Robust Data Extraction**: Uses JavaScript evaluation to extract business data from dynamic content

### 2. Configuration System (`config/sites.yaml`)
- **Search Queries**: Configurable list of keywords and locations
- **Sample Queries**: Pre-configured searches for restaurants, plumbers, dentists, lawyers, and gyms
- **Flexible Selectors**: Multiple CSS selector fallbacks for different Google Maps layouts
- **Customizable Settings**: Adjustable scroll behavior, timeouts, and result limits

### 3. Database Schema Updates (`app/models/database.py`)
- **Enhanced Company Model**: Added Google Maps specific fields:
  - `category`: Business type/category
  - `address`: Full business address
  - `phone`: Business phone number
  - `rating`: Google Maps rating
  - `review_count`: Number of reviews
  - `source`: Data source identifier
- **Monthly Data Tracking**: Enhanced with `query_name` field for tracking search queries
- **Database Migration**: Automatic migration script to update existing databases

### 4. Data Processing Pipeline (`app/scraper/pipelines.py`)
- **Smart Deduplication**: Prevents duplicate businesses using name and address
- **Data Validation**: Cleans and validates extracted business data
- **Monthly Versioning**: Creates monthly snapshots with `month_key` format (YYYY-MM)
- **Query Tracking**: Associates businesses with their search queries

## Usage

### Manual Scraping
```bash
python run.py scraper
```

### Automated Monthly Scraping
```bash
python run.py scheduler
```

### Database Migration
```bash
python migrate_database.py
```

## Configuration

### Adding New Search Queries
Edit `config/sites.yaml` to add new search queries:

```yaml
search_queries:
  - name: "Your Business Type"
    keywords: "your keywords"
    location: "City, State"
    max_results: 100
```

### Customizing Selectors
The scraper uses multiple fallback selectors to handle Google Maps' changing interface:

```yaml
google_maps:
  selectors:
    business_listing: ".Nv2PK"
    business_name: ".Nv2PK .fontHeadlineSmall::text"
    # ... more selectors
```

## Data Extracted

For each business, the scraper extracts:
- **Business Name**: Company name
- **Category/Type**: Business category
- **Address**: Full business address
- **Phone Number**: Contact phone
- **Website URL**: Business website
- **Rating**: Google Maps rating
- **Review Count**: Number of reviews
- **Source**: Always "Google Maps"

## Technical Implementation

### Playwright Integration
- Uses Chromium browser in headless mode
- Handles JavaScript rendering and dynamic content
- Implements smart scrolling to load more results
- Waits for network idle before extracting data

### Scrolling and Pagination
- Automatically scrolls through results
- Configurable scroll attempts and pause times
- Handles Google Maps' infinite scroll interface
- Extracts data from all visible listings

### Error Handling
- Multiple selector fallbacks for robustness
- JavaScript evaluation with CSS selector fallback
- Comprehensive logging for debugging
- Graceful handling of missing data

## Database Schema

### Companies Table
```sql
CREATE TABLE companies (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255),
    description TEXT,
    website VARCHAR(500),
    industry VARCHAR(100),
    size VARCHAR(50),
    location VARCHAR(255),
    category VARCHAR(100),        -- NEW: Business category
    address TEXT,                  -- NEW: Full address
    phone VARCHAR(50),             -- NEW: Phone number
    rating VARCHAR(10),            -- NEW: Google rating
    review_count INTEGER,         -- NEW: Review count
    source VARCHAR(50),           -- NEW: Data source
    created_at DATETIME,
    updated_at DATETIME
);
```

### Monthly Data Table
```sql
CREATE TABLE monthly_data (
    id INTEGER PRIMARY KEY,
    company_id INTEGER,
    month_key VARCHAR(7),         -- Format: "2025-01"
    data_type VARCHAR(50),
    raw_data TEXT,
    source_url VARCHAR(1000),
    query_name VARCHAR(255),      -- NEW: Search query name
    scraped_at DATETIME,
    is_active BOOLEAN
);
```

## Integration with Existing System

The Google Maps scraper integrates seamlessly with the existing LeadTool infrastructure:

- **FastAPI Backend**: All existing API endpoints work with Google Maps data
- **Streamlit Dashboard**: Dashboard displays Google Maps business data
- **Scheduler**: Monthly automation works with Google Maps scraper
- **Database**: Uses existing SQLite/PostgreSQL setup
- **Logging**: Integrated with existing logging system

## Performance Considerations

- **Concurrent Requests**: 16 concurrent requests per domain
- **Rate Limiting**: 2-second delay between requests
- **Data Retention**: Keeps 12 months of historical data
- **Memory Usage**: Efficient scrolling and data extraction
- **Error Recovery**: Robust error handling and retry logic

## Future Enhancements

1. **Advanced Filtering**: Add filters for rating, review count, etc.
2. **Geographic Clustering**: Group businesses by location
3. **Data Enrichment**: Add more business details from other sources
4. **Real-time Updates**: WebSocket integration for live data
5. **Export Formats**: Additional export options (JSON, XML)

## Troubleshooting

### Common Issues
1. **No Data Extracted**: Check if Google Maps interface has changed
2. **Database Errors**: Run `python migrate_database.py`
3. **Playwright Issues**: Ensure Playwright browsers are installed
4. **Selector Failures**: Update selectors in `config/sites.yaml`

### Debug Mode
```bash
python run.py scraper --debug
```

### Log Files
- **Scraper Logs**: `logs/scraper.log`
- **Scheduler Logs**: `logs/scheduler.log`
- **Application Logs**: `logs/leadtool.log`

## Conclusion

The Google Maps LeadTool implementation provides a robust, scalable solution for collecting local business data. The system is designed to handle Google Maps' dynamic interface while maintaining data quality and system performance. The modular architecture allows for easy customization and future enhancements.

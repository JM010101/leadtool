"""
Manual scraping utilities for LeadTool
"""
import os
import sys
import logging
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.scheduler.cron import LeadToolScheduler

def run_manual_scraping():
    """Run scraping manually"""
    print("Starting manual scraping...")
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize scheduler
    scheduler = LeadToolScheduler()
    
    try:
        # Run manual scraping
        scheduler.run_manual_scraping()
        print("Manual scraping completed successfully!")
        
    except Exception as e:
        print(f"Error during manual scraping: {e}")
        logging.error(f"Error during manual scraping: {e}")

if __name__ == "__main__":
    run_manual_scraping()

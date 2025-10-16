"""
Monthly automation scheduler for LeadTool
"""
import os
import sys
import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import subprocess
import yaml

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.models.database import get_db, Company, MonthlyData
from app.scraper.spider import GoogleMapsSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LeadToolScheduler:
    """Monthly automation scheduler for LeadTool"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.setup_scheduler()
    
    def setup_scheduler(self):
        """Setup the monthly scraping schedule"""
        # Schedule to run on the 1st of every month at 2 AM
        self.scheduler.add_job(
            func=self.run_monthly_scraping,
            trigger=CronTrigger(day=1, hour=2, minute=0),
            id='monthly_scraping',
            name='Monthly Lead Scraping',
            replace_existing=True
        )
        
        # Schedule to run on the 15th of every month at 2 AM (backup run)
        self.scheduler.add_job(
            func=self.run_monthly_scraping,
            trigger=CronTrigger(day=15, hour=2, minute=0),
            id='monthly_scraping_backup',
            name='Monthly Lead Scraping (Backup)',
            replace_existing=True
        )
        
        logger.info("Scheduler configured for monthly scraping")
    
    def run_monthly_scraping(self):
        """Run the monthly scraping process"""
        try:
            logger.info("Starting monthly scraping process")
            
            # Get current month key
            month_key = datetime.now().strftime("%Y-%m")
            logger.info(f"Processing month: {month_key}")
            
            # Deactivate previous month's data
            self.deactivate_previous_data(month_key)
            
            # Run the scraper
            self.run_scraper()
            
            # Clean up old data (keep last 12 months)
            self.cleanup_old_data()
            
            logger.info("Monthly scraping process completed successfully")
            
        except Exception as e:
            logger.error(f"Error in monthly scraping process: {e}")
            # Send notification email or alert here if needed
    
    def deactivate_previous_data(self, current_month_key):
        """Deactivate data from previous months"""
        try:
            db = next(get_db())
            
            # Deactivate all active monthly data
            db.query(MonthlyData).filter(
                MonthlyData.is_active == True
            ).update({"is_active": False})
            
            db.commit()
            logger.info("Deactivated previous month's data")
            
        except Exception as e:
            logger.error(f"Error deactivating previous data: {e}")
        finally:
            db.close()
    
    def run_scraper(self):
        """Run the Scrapy spider"""
        try:
            # Set up Scrapy settings
            settings = get_project_settings()
            settings.update({
                'DATABASE_URL': os.getenv('DATABASE_URL', 'sqlite:///./data/leadtool.db'),
                'LOG_LEVEL': 'INFO',
                'LOG_FILE': 'logs/scraper.log',
                'ITEM_PIPELINES': {
                    'app.scraper.pipelines.DatabasePipeline': 300,
                }
            })
            
            # Create and run the crawler
            process = CrawlerProcess(settings)
            process.crawl(GoogleMapsSpider)
            process.start()
            
            logger.info("Scraper completed successfully")
            
        except Exception as e:
            logger.error(f"Error running scraper: {e}")
            raise
    
    def cleanup_old_data(self):
        """Clean up data older than 12 months"""
        try:
            db = next(get_db())
            
            # Calculate cutoff date (12 months ago)
            cutoff_date = datetime.now() - timedelta(days=365)
            cutoff_month = cutoff_date.strftime("%Y-%m")
            
            # Delete old monthly data
            old_data = db.query(MonthlyData).filter(
                MonthlyData.month_key < cutoff_month
            ).all()
            
            for data in old_data:
                db.delete(data)
            
            db.commit()
            logger.info(f"Cleaned up data older than {cutoff_month}")
            
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
        finally:
            db.close()
    
    def start(self):
        """Start the scheduler"""
        try:
            self.scheduler.start()
            logger.info("Scheduler started successfully")
        except Exception as e:
            logger.error(f"Error starting scheduler: {e}")
    
    def stop(self):
        """Stop the scheduler"""
        try:
            self.scheduler.shutdown()
            logger.info("Scheduler stopped")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {e}")
    
    def run_manual_scraping(self):
        """Run scraping manually (for testing)"""
        logger.info("Running manual scraping")
        self.run_monthly_scraping()

def main():
    """Main function to run the scheduler"""
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Initialize and start scheduler
    scheduler = LeadToolScheduler()
    
    try:
        scheduler.start()
        logger.info("LeadTool Scheduler is running. Press Ctrl+C to stop.")
        
        # Keep the script running
        import time
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")
        scheduler.stop()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        scheduler.stop()

if __name__ == "__main__":
    main()

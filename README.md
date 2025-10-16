# LeadTool - Unified Lead Generation and Management System

A complete Python project that automatically gathers company-level data each month and makes it easy for a small internal team to work with the results.

## 🚀 Features

- **Automated Web Scraping**: Uses Scrapy + Playwright for dynamic sites
- **Monthly Data Collection**: Automated monthly scraping with data versioning
- **FastAPI Backend**: RESTful API with comprehensive endpoints
- **Streamlit Dashboard**: Interactive web interface for data visualization
- **Database Support**: SQLite for development, PostgreSQL for production
- **Export Functionality**: CSV and Excel export capabilities
- **YAML Configuration**: Easy site and settings management

## 📁 Project Structure

```
LeadTool/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py         # SQLAlchemy models
│   │   └── schemas.py          # Pydantic schemas
│   ├── api/
│   │   ├── __init__.py
│   │   ├── companies.py        # Company endpoints
│   │   ├── contacts.py         # Contact endpoints
│   │   └── export.py           # Export endpoints
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── spider.py           # Main Scrapy spider
│   │   ├── pipelines.py        # Data processing
│   │   └── settings.py         # Scrapy settings
│   ├── scheduler/
│   │   ├── __init__.py
│   │   ├── cron.py             # Monthly automation
│   │   └── manual.py           # Manual scraping
│   └── dashboard/
│       ├── __init__.py
│       ├── main.py             # Streamlit app
│       └── pages/
│           ├── __init__.py
│           ├── overview.py
│           ├── search.py
│           └── export.py
├── config/
│   ├── sites.yaml              # Target websites config
│   ├── database.yaml           # Database config
│   └── settings.yaml           # App settings
├── data/
│   └── leadtool.db             # SQLite database
├── logs/                       # Log files
├── requirements.txt
├── README.md
└── run.py                      # Main entry point
```

## 🛠️ Installation

### Prerequisites

- Python 3.11+ (recommended)
- Node.js (for Playwright)
- PostgreSQL (for production)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd LeadTool
   ```

2. **Create virtual environment**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install
   ```

5. **Create necessary directories**
   ```bash
   mkdir -p data logs
   ```

## 🚀 Quick Start

### 1. Start the API Server

```bash
# Development
python3.11 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
python3.11 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 2. Start the Dashboard

```bash
# In a new terminal
streamlit run app/dashboard/main.py --server.port 8501
```

### 3. Run Manual Scraping

```bash
# Run scraper manually
python3.11 app/scheduler/manual.py
```

### 4. Start the Scheduler

```bash
# Start monthly automation
python3.11 app/scheduler/cron.py
```

## 📊 Usage

### API Endpoints

- **Companies**: `GET /api/v1/companies`
- **Contacts**: `GET /api/v1/contacts`
- **Export**: `GET /api/v1/export/companies`
- **Search**: `GET /api/v1/companies/search?q=query`

### Dashboard

Access the dashboard at `http://localhost:8501` with three main tabs:

1. **Overview**: Metrics and charts
2. **Search & Filter**: Find companies and contacts
3. **Export**: Download data in CSV/Excel format

### Configuration

Edit `config/sites.yaml` to add new target websites:

```yaml
sites:
  - name: "Your Site"
    url: "https://example.com"
    selectors:
      company:
        name: ".company-name::text"
        domain: ".company-domain::text"
        # ... more selectors
```

## 🔧 Configuration

### Database Settings

Edit `config/database.yaml`:

```yaml
production:
  type: "postgresql"
  url: "postgresql://user:pass@localhost:5432/leadtool"
```

### Scraping Settings

Edit `config/sites.yaml` to configure target sites and selectors.

### Application Settings

Edit `config/settings.yaml` for app configuration.

## 📅 Scheduling

### Monthly Automation

The system automatically runs on:
- **1st of every month at 2 AM**: Primary scraping
- **15th of every month at 2 AM**: Backup scraping

### Manual Scraping

```bash
# Run immediately
python3.11 app/scheduler/manual.py

# Run scheduler
python3.11 app/scheduler/cron.py
```

### Cron Job Setup

Add to your crontab:

```bash
# Monthly scraping
0 2 1 * * cd /path/to/LeadTool && python3.11 app/scheduler/cron.py

# Daily scheduler
0 0 * * * cd /path/to/LeadTool && python3.11 app/scheduler/cron.py
```

## 🐳 Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN playwright install

CMD ["python3.11", "app/main.py"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  leadtool:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/leadtool
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: leadtool
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 🔍 Monitoring

### Logs

- **Application**: `logs/leadtool.log`
- **Scheduler**: `logs/scheduler.log`
- **Scraper**: `logs/scraper.log`

### Health Checks

- **API**: `GET /health`
- **Database**: Check connection status
- **Scheduler**: Check job status

## 🚀 Production Deployment

### Environment Variables

```bash
export DATABASE_URL="postgresql://user:pass@localhost:5432/leadtool"
export API_BASE_URL="https://your-api.com/api/v1"
export DEBUG=false
```

### Database Migration

```bash
# Create tables
python3.11 -c "from app.models.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### Process Management

Use supervisor or systemd to manage processes:

```ini
[program:leadtool-api]
command=python3.11 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
directory=/path/to/LeadTool
autostart=true
autorestart=true
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:

1. Check the logs in the `logs/` directory
2. Verify your configuration files
3. Ensure all dependencies are installed
4. Check that the database is accessible

## 🔄 Data Flow

1. **Scheduler** triggers monthly scraping
2. **Spider** extracts data from configured sites
3. **Pipeline** processes and stores data in database
4. **API** serves data to dashboard
5. **Dashboard** provides visualization and export

## 📈 Performance

- **Concurrent Requests**: 16 per domain
- **Data Retention**: 12 months
- **Export Limit**: 10,000 rows
- **API Timeout**: 30 seconds

## 🔒 Security

- CORS enabled for cross-origin requests
- Rate limiting available
- API key authentication (optional)
- Input validation on all endpoints

---

**LeadTool** - Automate your lead generation and management process! 🚀

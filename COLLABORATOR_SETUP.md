# Setup Guide for Collaborators

## Prerequisites
- **Python 3.8+** installed
- **Git** installed
- **Google Chrome** (for Selenium scraping)

## Initial Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Anuj-Bhusal/ElectionScrapper.git
cd ElectionScrapper
```

### 2. Install Dependencies
```bash
pip install -r governance_weekly/requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the `governance_weekly/` directory:

```env
# Scraping Configuration
MAX_ARTICLES_PER_SITE=100
RATE_LIMIT_SEC=1.0
USER_AGENT=GovernanceWeeklyBot/1.0

# Translation Backend (google, gemini, or marian)
TRANSLATION_BACKEND=google

# Google Cloud Translation API (Optional - for better translation)
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json

# Gemini API (Alternative translation - get from Google AI Studio)
GEMINI_API_KEY=your_gemini_api_key_here

# Google Drive Upload (Optional)
DRIVE_FOLDER_ID=your_google_drive_folder_id

# Filtering Configuration
RELEVANCE_THRESHOLD=1
MAX_ARTICLES_IN_REPORT=40
MIN_IMPACT_SCORE=10.0

# Browser Configuration
USE_SELENIUM=True
SELENIUM_HEADLESS=True

# Skip robots.txt check (for personal/research use)
SKIP_ROBOTS_CHECK=True
```

### 4. API Keys You May Need

#### Option A: Google Cloud Translate (Recommended for quality)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "Cloud Translation API"
4. Create a Service Account and download JSON credentials
5. Place the JSON file in `governance_weekly/` folder
6. Update `.env` with the path: `GOOGLE_APPLICATION_CREDENTIALS=credentials.json`

#### Option B: Gemini API (Free alternative)
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Add to `.env`: `GEMINI_API_KEY=your_key_here`
4. Set `TRANSLATION_BACKEND=gemini`

#### Option C: MarianMT (Local, no API needed)
- Set `TRANSLATION_BACKEND=marian` in `.env`
- First run will download ~300MB model
- Slower but completely offline

### 5. (Optional) Google Drive Upload Setup
1. Enable Google Drive API in Google Cloud Console
2. Create OAuth 2.0 credentials
3. Download `credentials.json` to `governance_weekly/` folder
4. First run will prompt browser authentication
5. Add your Drive folder ID to `.env`

## Running the Project

### Standard Weekly Run
```bash
cd governance_weekly
python ../start_governance_weekly.py
```

This will:
1. Scrape articles from **previous Friday to today**
2. Translate Nepali → English
3. Filter using weighted scoring (5-point threshold)
4. Generate PDF report in `output/` folder

### Advanced Options
```bash
# Test specific scraper
python main.py --mode collect --scraper kathmandu

# Only generate report from existing DB data
python main.py --mode summarize

# Force complete pipeline (clear DB + scrape + report)
python main.py --mode force
```

## Project Configuration

### Current Focus
- **Target**: Nepal Election - March 5, 2026
- **Categories**: Election & Governance ONLY
- **Date Range**: Always scrapes from previous Friday to today
- **Expected Articles**: 5-10 high-quality articles per week

### Weighted Scoring Model
Articles need **5+ points** to pass:
- **Tier 1** (5 pts): Direct election terms (Election Commission, March 5, polling, ballot)
- **Tier 2** (3 pts): Political parties (एमाले, कांग्रेस, माओवादी) + strategic terms (गठबन्धन, भागबण्डा, उम्मेदवार)
- **Tier 3** (1 pt): General political context

### What Gets Blocked
Exclusion list filters out:
- Stock market (NEPSE)
- Beauty pageants
- Tourism
- Foreign affairs (Trump, Venezuela, etc.)
- Sports, literature, crime, weather

## News Sources (10 Sites)
1. Ekantipur
2. Kathmandu Post
3. My Republica
4. Setopati
5. Nayapatrika
6. Annapurna Post
7. Annapurna Express
8. Online Khabar
9. Ratopati
10. Ukaalo

## Troubleshooting

### Issue: Translation timeouts
- **Solution**: Switch to Gemini or MarianMT in `.env`

### Issue: No articles in PDF
- **Solution**: Check date range - ensure articles exist from last Friday
- Run `python check_db.py` to verify database

### Issue: Chrome driver errors
- **Solution**: Update Chrome browser to latest version
- Selenium auto-manages ChromeDriver

### Issue: Robots.txt blocking sites
- **Solution**: Already handled - `SKIP_ROBOTS_CHECK=True` is default

## File Structure
```
governance_weekly/
├── scrapers/          # Site-specific scrapers
├── classifier/        # Keyword-based filtering
├── translator/        # Translation engines
├── reporting/         # PDF generation
├── database/          # SQLite storage
├── utils/             # Helper utilities
├── data/              # SQLite database
└── output/            # Generated PDFs
```

## Modifying Keywords
Edit these files to adjust filtering:
- **Keywords**: `governance_weekly/classifier/keywords.py`
- **Scoring logic**: `governance_weekly/classifier/classifier.py`
- **Exclusion list**: `governance_weekly/classifier/keywords.py`

## Questions?
Check these files for details:
- `README.md` - Project overview
- `FILTERING_SYSTEM.md` - Detailed filtering logic
- `governance_weekly/config.py` - All configuration options

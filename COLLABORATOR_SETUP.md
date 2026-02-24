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

**CRITICAL: You MUST configure translation or the pipeline will fail!**

```env
# ============================================================
# TRANSLATION SETUP (REQUIRED - Choose ONE option below)
# ============================================================

# OPTION 1 (RECOMMENDED): Gemini API - Free & Reliable
# Get key from: https://makersuite.google.com/app/apikey
TRANSLATION_BACKEND=gemini
GEMINI_API_KEY=your_gemini_api_key_here

# OPTION 2: Googletrans (Free but unreliable, often blocked)
# TRANSLATION_BACKEND=googletrans
# No API key needed, but may show "[Translation Failed]"

# OPTION 3: Google Cloud Translate (Best quality, requires billing)
# TRANSLATION_BACKEND=google
# GOOGLE_APPLICATION_CREDENTIALS=credentials.json

# OPTION 4: MarianMT (Local/offline, ~300MB download, slower)
# TRANSLATION_BACKEND=marian
# pip install transformers torch

# ============================================================
# Other Configuration
# ============================================================

# Scraping Configuration
MAX_ARTICLES_PER_SITE=100
RATE_LIMIT_SEC=1.0
USER_AGENT=GovernanceWeeklyBot/1.0

# Google Drive Upload (Optional)
DRIVE_FOLDER_ID=

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

### 4. Setup Translation API (REQUIRED)

**⚠️ CRITICAL: Pipeline will fail with "[Translation Failed]" errors if this is not configured!**

Choose **ONE** of these options:

#### Option A: Gemini API (✅ RECOMMENDED - Free & Reliable)
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key
5. Add to `.env`:
   ```env
   TRANSLATION_BACKEND=gemini
   GEMINI_API_KEY=your_actual_key_here
   ```

#### Option B: Googletrans (Free but Unreliable)
- No API key needed
- Often fails with "[Translation Failed]" due to Google blocking
- Use only for testing
- Add to `.env`: `TRANSLATION_BACKEND=googletrans`

#### Option C: Google Cloud Translate (Best Quality, Requires Billing)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project
3. Enable "Cloud Translation API"
4. Create Service Account → download JSON
5. Place JSON in `governance_weekly/` folder
6. Add to `.env`:
   ```env
   TRANSLATION_BACKEND=google
   GOOGLE_APPLICATION_CREDENTIALS=credentials.json
   ```

#### Option D: MarianMT (Local/Offline)
1. Install dependencies: `pip install transformers torch`
2. First run downloads ~300MB model
3. Slower but completely offline
4. Add to `.env`: `TRANSLATION_BACKEND=marian`

### 5. (Optional) Google Drive Upload Setup
1. Enable Google Drive API in Google Cloud Console
2. Create OAuth 2.0 credentials
3. Download `credentials.json` to `governance_weekly/` folder
4. First run will prompt browser authentication
5. Add your Drive folder ID to `.env`

## Running the Project

### Validate Setup First (Recommended)
Before running the full pipeline, validate your setup:
```bash
cd governance_weekly
python validate_setup.py
```

This will check:
- ✓ .env file exists
- ✓ Translation API is configured
- ✓ All dependencies installed
- ✓ Directories created

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

### Issue: "[Translation Failed]" in PDF with black squares (█)
**Symptoms:**
- PDF shows `[Translation Failed]` in article titles
- Black squares or garbled text in article content
- Logs show translation errors

**Cause:** No working translation backend configured

**Solution:**
1. Check your `.env` file exists in `governance_weekly/` folder
2. Set up Gemini API (recommended):
   ```env
   TRANSLATION_BACKEND=gemini
   GEMINI_API_KEY=your_actual_key_here
   ```
3. Run pipeline again - should now translate properly

### Issue: Translation timeouts
**Solution:** Switch to Gemini or MarianMT in `.env`:
```env
TRANSLATION_BACKEND=gemini
GEMINI_API_KEY=your_key
```

### Issue: No articles in PDF
**Solution:** 
- Check date range - ensure articles exist from last Friday
- Run: `cd governance_weekly; python debug_db.py`
- Verify scrapers aren't blocked by checking logs

### Issue: Chrome driver errors
**Solution:** 
- Update Chrome browser to latest version
- Selenium auto-manages ChromeDriver

### Issue: Robots.txt blocking sites
**Solution:** Already handled - `SKIP_ROBOTS_CHECK=True` is default

### Issue: "No module named 'googletrans'"
**Solution:**
```bash
pip install googletrans==4.0.0rc1
```
Or switch to Gemini backend (recommended)

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

# Nepal Election Weekly — Automated Scrape → Translate → PDF Pipeline

## Overview
Automated pipeline focused on **Nepal March 5, 2026 Election** coverage. Scrapes 10 Nepali news sites, extracts **Election and Governance** news only, translates to English, and generates a weekly PDF report.

## Features
- Scrapes 10+ configured news sources.
- Extracts article content using readability heuristics.
- Translates Nepali content to English using Google Cloud Translate (or fallbacks).
- Classifies articles into **Election** and **Governance** categories ONLY.
- Filters out all non-election/governance content.
- Generates a weekly PDF report with summaries.
- Uploads report to Google Drive.

## Election Focus
This system is specifically configured for:
- **Target Event**: Nepal Election - March 5, 2026
- **Categories**: Election, Governance
- **Keywords**: 180+ election and governance specific keywords
- **Excluded**: Sports, entertainment, health, disasters, migration, etc.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Helper for Playwright/Selenium (if needed):
   - Ensure Chrome/Chromedriver is installed.
3. Configure environment:
   - Copy `.env.example` to `.env`
   - Fill in API keys and configuration.

## Usage
- **Collect** (runs scraper): `python main.py --mode collect`
- **Summarize** (generates report): `python main.py --mode summarize`
- **Force Run** (all steps): `python main.py --mode force`

## Directory Structure
- `scrapers/`: Domain-specific scraper logic.
- `extractor/`: Content extraction implementation.
- `translator/`: Translation adapters.
- `classifier/`: Keyword-based classification (Election & Governance only).
- `reporting/`: PDF generation and uploading.
- `database/`: SQLite storage models.

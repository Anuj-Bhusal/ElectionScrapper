# Governance Weekly — Automated Scrape → Translate → PDF Pipeline

## Overview
Automated pipeline to scrape 10 Nepali news sites (and occasional reputable international coverage), extract governance-relevant items, translate them to English, and export a weekly PDF report.

## Features
- Scrapes 10+ configured news sources.
- Extracts article content using readability heuristics.
- Translates Nepali content to English using Google Cloud Translate (or falbacks).
- Classifies articles into Governance, Corruption, Health, Election, etc.
- Generates a weekly PDF report with summaries.
- Uploads report to Google Drive.

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
- `classifier/`: Keyword-based classification.
- `reporting/`: PDF generation and uploading.
- `database/`: SQLite storage models.

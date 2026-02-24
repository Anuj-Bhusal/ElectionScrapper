# Translation Issue - Fix Guide

## What Happened

Your collaborator's PDF showed `[Translation Failed]` with black squares (█) because:

**Root Cause:** No translation API was configured in their `.env` file.

## The Problem Breakdown

1. **Default backend was "google"** - Requires Google Cloud credentials ($$)
2. **Fell back to "googletrans"** - Free library but frequently blocked by Google
3. **No Gemini API key** - The recommended free alternative wasn't set up
4. **MarianMT not installed** - The offline fallback wasn't available
5. **Result:** Translation returned original Nepali text → PDF showed garbled characters

## What I Fixed

### 1. Changed Default Backend
- **Before:** `TRANSLATION_BACKEND=google` (requires paid Google Cloud)
- **After:** `TRANSLATION_BACKEND=googletrans` (free, works for light usage)

### 2. Improved .env.example
- Added **CRITICAL** warnings about translation setup
- Made Gemini the **RECOMMENDED** option (free API, reliable)
- Added clear step-by-step instructions for each backend

### 3. Added Startup Validation
- Translator now shows **CRITICAL WARNING** if no backend is working
- Prevents silent failures
- Logs helpful setup instructions

### 4. Created validate_setup.py Script
Collaborators can now run:
```bash
cd governance_weekly
python validate_setup.py
```

This checks:
- ✓ .env file exists
- ✓ Translation API configured
- ✓ Dependencies installed
- ✗ Shows specific errors to fix

### 5. Enhanced Troubleshooting Guide
Added specific section for "[Translation Failed]" error with screenshots

## Tell Your Collaborator

Share this quick fix guide:

---

### Quick Fix (2 minutes)

1. **Get Gemini API Key** (FREE):
   - Go to: https://makersuite.google.com/app/apikey
   - Sign in → Click "Create API Key"
   - Copy the key

2. **Update .env file**:
   ```bash
   cd governance_weekly
   notepad .env  # or use any text editor
   ```
   
   Add these lines:
   ```env
   TRANSLATION_BACKEND=gemini
   GEMINI_API_KEY=paste_your_key_here
   ```

3. **Validate Setup**:
   ```bash
   python validate_setup.py
   ```
   
   Should show: ✅ SETUP COMPLETE

4. **Run Pipeline**:
   ```bash
   python ../start_governance_weekly.py
   ```

### Why This Works

- **Gemini is free** (generous quota)
- **More reliable** than googletrans
- **Better translation quality**
- **No billing account needed** (unlike Google Cloud Translate)

---

## Alternative Solutions

If Gemini doesn't work for some reason:

### Option B: Use Googletrans (Less Reliable)
```env
TRANSLATION_BACKEND=googletrans
```
- No API key needed
- May fail occasionally
- Free but rate-limited

### Option C: Use MarianMT (Offline)
```bash
pip install transformers torch
```
```env
TRANSLATION_BACKEND=marian
```
- Completely offline
- Downloads ~300MB model on first run
- Slower but works without internet

## Files Updated in Repo

All fixes pushed to GitHub:
- ✅ `config.py` - Changed default backend
- ✅ `.env.example` - Added critical warnings and instructions
- ✅ `translator.py` - Added startup validation
- ✅ `requirements.txt` - Added correct package versions
- ✅ `COLLABORATOR_SETUP.md` - Enhanced setup guide
- ✅ `validate_setup.py` - NEW validation script

Your collaborator should:
1. `git pull` to get latest changes
2. Run `validate_setup.py`
3. Fix any errors it reports
4. Run the pipeline

## Prevention

The new validation warnings will catch this immediately on startup:
```
===============================================================================
NO TRANSLATION BACKEND AVAILABLE!
Translation will fail. Please configure one of these:
1. GEMINI_API_KEY (recommended - free from https://makersuite.google.com)
2. GOOGLE_APPLICATION_CREDENTIALS (Google Cloud Translate)
3. Install googletrans: pip install googletrans==4.0.0rc1
4. Install MarianMT: pip install transformers torch
===============================================================================
```

This makes it impossible to miss the setup requirement!

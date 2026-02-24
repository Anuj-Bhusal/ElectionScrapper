"""
Setup Validation Script
Run this before starting the pipeline to check if everything is configured correctly
"""

import sys
import os

print("=" * 80)
print("SETUP VALIDATION")
print("=" * 80)

errors = []
warnings = []
success = []

# Check 1: .env file exists
print("\n1. Checking for .env file...")
if os.path.exists('.env'):
    success.append("✓ .env file found")
else:
    errors.append("✗ .env file NOT FOUND - Create it from .env.example")

# Check 2: Import config
print("2. Checking configuration...")
try:
    from config import Config
    success.append("✓ Config module loaded")
except Exception as e:
    errors.append(f"✗ Failed to load config: {e}")

# Check 3: Translation backend
print("3. Checking translation backend...")
try:
    from config import Config
    backend = Config.TRANSLATION_BACKEND
    print(f"   Backend: {backend}")
    
    if backend == "gemini":
        api_key = Config.GEMINI_API_KEY if hasattr(Config, 'GEMINI_API_KEY') else None
        if api_key and api_key.strip() and api_key != "your_gemini_api_key_here":
            success.append("✓ Gemini API key configured")
        else:
            errors.append("✗ GEMINI_API_KEY not set or is placeholder")
            errors.append("  Get key from: https://makersuite.google.com/app/apikey")
    
    elif backend == "google":
        creds = Config.GOOGLE_APPLICATION_CREDENTIALS
        if creds and os.path.exists(creds):
            success.append("✓ Google Cloud credentials file found")
        else:
            errors.append(f"✗ Google Cloud credentials not found: {creds}")
    
    elif backend == "googletrans":
        warnings.append("⚠ Using googletrans (free but unreliable)")
        warnings.append("  Consider switching to Gemini for better reliability")
    
    elif backend == "marian":
        warnings.append("⚠ Using MarianMT (local/offline)")
        warnings.append("  First run will download ~300MB model")
    
except Exception as e:
    errors.append(f"✗ Translation config error: {e}")

# Check 4: Try initializing translator
print("4. Testing translator initialization...")
try:
    from translator.translator import Translator
    t = Translator()
    if t.backend == "none":
        errors.append("✗ NO WORKING TRANSLATION BACKEND")
        errors.append("  Translation will fail!")
    else:
        success.append(f"✓ Translator initialized with backend: {t.backend}")
except Exception as e:
    errors.append(f"✗ Failed to initialize translator: {e}")

# Check 5: Database directory
print("5. Checking database directory...")
if os.path.exists('data'):
    success.append("✓ data/ directory exists")
else:
    os.makedirs('data', exist_ok=True)
    success.append("✓ Created data/ directory")

# Check 6: Output directory
print("6. Checking output directory...")
if os.path.exists('output'):
    success.append("✓ output/ directory exists")
else:
    os.makedirs('output', exist_ok=True)
    success.append("✓ Created output/ directory")

# Check 7: Required packages
print("7. Checking required packages...")
required = {
    'requests': 'requests',
    'bs4': 'beautifulsoup4',
    'selenium': 'selenium',
    'readability': 'readability-lxml',
    'reportlab': 'reportlab',
    'dotenv': 'python-dotenv'
}

missing_packages = []
for module, package in required.items():
    try:
        __import__(module)
    except ImportError:
        missing_packages.append(package)

if missing_packages:
    errors.append(f"✗ Missing packages: {', '.join(missing_packages)}")
    errors.append("  Run: pip install -r requirements.txt")
else:
    success.append("✓ All required packages installed")

# Print results
print("\n" + "=" * 80)
print("RESULTS")
print("=" * 80)

if success:
    print("\n✓ SUCCESS:")
    for msg in success:
        print(f"  {msg}")

if warnings:
    print("\n⚠ WARNINGS:")
    for msg in warnings:
        print(f"  {msg}")

if errors:
    print("\n✗ ERRORS:")
    for msg in errors:
        print(f"  {msg}")
    print("\n" + "=" * 80)
    print("❌ SETUP INCOMPLETE - Fix errors above before running pipeline")
    print("=" * 80)
    sys.exit(1)
else:
    print("\n" + "=" * 80)
    print("✅ SETUP COMPLETE - Ready to run pipeline!")
    print("=" * 80)
    print("\nRun: python ../start_governance_weekly.py")
    sys.exit(0)

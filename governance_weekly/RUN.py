# ONE-COMMAND GOVERNANCE WEEKLY PIPELINE
# Just run: python RUN.py

import os
import sqlite3
import glob
import subprocess
from datetime import datetime

print("\n" + "="*60)
print("🏛️  GOVERNANCE WEEKLY - COMPLETE PIPELINE")
print("="*60 + "\n")

# Step 1: Clear old data
print("🗑️  Clearing old data...")
try:
    conn = sqlite3.connect('data/gov_weekly.db')
    conn.execute('DELETE FROM articles')
    conn.commit()
    conn.close()
    print("   ✓ Database cleared")
except Exception as e:
    print(f"   ⚠️  Database: {e}")

for pdf in glob.glob('output/*.pdf'):
    try:
        os.remove(pdf)
    except:
        pass
print("   ✓ Old PDFs deleted\n")

# Step 2: Collect articles
print("="*60)
print("📰 STEP 1: COLLECTING ARTICLES")
print("="*60)
result = os.system("python main.py --mode collect")
if result != 0:
    print("\n❌ Collection failed!")
    exit(1)

# Step 3: Generate PDF
print("\n" + "="*60)
print("📄 STEP 2: GENERATING PDF REPORT")
print("="*60)
result = os.system("python main.py --mode summarize")
if result != 0:
    print("\n❌ Report generation failed!")
    exit(1)

# Step 4: Open PDF
print("\n" + "="*60)
print("📋 STEP 3: OPENING PDF")
print("="*60)
pdfs = list(glob.glob('output/GovernanceWeekly_*.pdf'))
if pdfs:
    pdf_path = pdfs[0]
    print(f"   Opening: {pdf_path}")
    subprocess.run(['powershell', '-Command', f'Invoke-Item "{pdf_path}"'], shell=True)
else:
    print("   ⚠️  No PDF found!")

print("\n" + "="*60)
print("✅ PIPELINE COMPLETE!")
print("="*60 + "\n")

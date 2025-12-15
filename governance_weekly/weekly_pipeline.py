"""
Complete Weekly Governance Report Pipeline
This script runs the full workflow from scratch:
1. Clears old data (optional)
2. Collects articles from all sources
3. Translates Nepali content to English
4. Classifies and scores articles
5. Generates English summaries
6. Filters top 40 most impactful articles
7. Generates PDF with clickable links
8. Uploads to Google Drive (if configured)

Usage:
  python weekly_pipeline.py --fresh-start    # Delete all data and start fresh
  python weekly_pipeline.py                  # Keep existing data, add new articles
"""

import argparse
import sqlite3
import os
import sys
from datetime import datetime

def clear_database():
    """Clear all articles from database and delete old PDFs"""
    print("🗑️  Clearing database and old outputs...")
    
    # Clear database
    if os.path.exists('data/gov_weekly.db'):
        conn = sqlite3.connect('data/gov_weekly.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM articles")
        conn.commit()
        count = cursor.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
        conn.close()
        print(f"   Database cleared. Remaining articles: {count}")
    else:
        print("   Database file not found. Will be created during collection.")
    
    # Delete old PDFs
    if os.path.exists('output'):
        import glob
        pdfs = glob.glob('output/*.pdf')
        for pdf in pdfs:
            try:
                os.remove(pdf)
                print(f"   Deleted: {pdf}")
            except:
                pass
        print(f"   Cleared {len(pdfs)} old PDF(s)")

def run_collection():
    """Run article collection from all sources"""
    print("\n📰 Step 1: Collecting articles from news sources...")
    print("   This will:")
    print("   - Scrape 10 news websites")
    print("   - Translate Nepali content to English")
    print("   - Classify articles into 13 categories")
    print("   - Generate English summaries")
    print("   - Store everything in database")
    print()
    
    result = os.system("python main.py --mode collect")
    
    if result == 0:
        print("✅ Collection complete!")
    else:
        print("❌ Collection failed! Check errors above.")
        sys.exit(1)
    
    # Show statistics
    conn = sqlite3.connect('data/gov_weekly.db')
    cursor = conn.cursor()
    
    total = cursor.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
    categorized = cursor.execute("SELECT COUNT(*) FROM articles WHERE categories IS NOT NULL AND categories != '[]'").fetchone()[0]
    translated = cursor.execute("SELECT COUNT(*) FROM articles WHERE title_translated IS NOT NULL").fetchone()[0]
    
    print(f"\n📊 Collection Statistics:")
    print(f"   Total articles: {total}")
    print(f"   Categorized: {categorized}")
    print(f"   Translated: {translated}")
    
    conn.close()

def run_reporting():
    """Generate PDF report"""
    print("\n📄 Step 2: Generating PDF report...")
    print("   This will:")
    print("   - Filter top 40 most impactful articles")
    print("   - Remove duplicates (90% similarity threshold)")
    print("   - Create PDF with clickable links")
    print("   - Upload to Google Drive (if configured)")
    print()
    
    result = os.system("python main.py --mode summarize")
    
    if result == 0:
        print("✅ Report generated!")
        
        # Show PDF location
        pdf_name = f"GovernanceWeekly_{datetime.now().strftime('%Y%m%d')}.pdf"
        pdf_path = os.path.join('output', pdf_name)
        
        if os.path.exists(pdf_path):
            print(f"\n📋 PDF Report: {pdf_path}")
            print(f"   Opening PDF...")
            # Use PowerShell to open PDF on Windows
            import subprocess
            subprocess.run(['powershell', '-Command', f'Invoke-Item "{pdf_path}"'], shell=True)
        else:
            print(f"\n⚠️  PDF file not found at: {pdf_path}")
    else:
        print("❌ Report generation failed! Check errors above.")
        sys.exit(1)

def show_summary():
    """Show final summary of the pipeline"""
    print("\n" + "="*60)
    print("📊 WEEKLY GOVERNANCE REPORT - PIPELINE COMPLETE")
    print("="*60)
    
    conn = sqlite3.connect('data/gov_weekly.db')
    cursor = conn.cursor()
    
    # Get statistics
    total = cursor.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
    categorized = cursor.execute("SELECT COUNT(*) FROM articles WHERE categories IS NOT NULL AND categories != '[]'").fetchone()[0]
    
    # Get category breakdown
    cursor.execute("""
        SELECT categories FROM articles 
        WHERE categories IS NOT NULL AND categories != '[]'
    """)
    
    import json
    category_counts = {}
    for row in cursor.fetchall():
        try:
            cats = json.loads(row[0])
            for cat in cats:
                category_counts[cat] = category_counts.get(cat, 0) + 1
        except:
            pass
    
    print(f"\n📈 Final Statistics:")
    print(f"   Total Articles Collected: {total}")
    print(f"   Governance-Related: {categorized}")
    print(f"   Articles in PDF Report: 40 (top impact)")
    
    print(f"\n📂 Category Distribution (all articles):")
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {cat}: {count}")
    
    print(f"\n🎯 Report Features:")
    print(f"   ✅ All content in English (translated from Nepali)")
    print(f"   ✅ Clickable source URLs in PDF")
    print(f"   ✅ Duplicate detection (85% similarity)")
    print(f"   ✅ Smart filtering by impact score")
    print(f"   ✅ Comprehensive 5-6 line summaries")
    print(f"   ✅ 13 governance categories tracked")
    
    conn.close()
    
    print("\n" + "="*60)
    print("✨ Pipeline completed successfully!")
    print("="*60 + "\n")

def main():
    parser = argparse.ArgumentParser(
        description="Weekly Governance Report Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fresh start (delete all data and start over)
  python weekly_pipeline.py --fresh-start
  
  # Regular weekly run (keep existing data, add new articles)
  python weekly_pipeline.py
        """
    )
    parser.add_argument(
        "--fresh-start", 
        action="store_true",
        help="Delete all existing data before starting collection"
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("🏛️  GOVERNANCE WEEKLY - AUTOMATED PIPELINE")
    print("="*60)
    
    if args.fresh_start:
        confirm = input("\n⚠️  This will DELETE all existing articles. Continue? (yes/no): ")
        if confirm.lower() == 'yes':
            clear_database()
        else:
            print("❌ Cancelled.")
            sys.exit(0)
    
    # Run the pipeline
    run_collection()
    run_reporting()
    show_summary()

if __name__ == "__main__":
    main()

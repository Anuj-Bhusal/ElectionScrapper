# GOVERNANCE WEEKLY - COMPLETE SETUP AND RUN SCRIPT
# Place this in: C:\Users\ACER\OneDrive\Desktop\Scrap\
# Just run: python start_governance_weekly.py

import os
import sys
import subprocess
import platform

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n▶️  {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
    if result.returncode != 0:
        print(f"❌ Failed: {description}")
        return False
    print(f"✅ {description}")
    return True

print("\n" + "="*70)
print("🏛️  GOVERNANCE WEEKLY - AUTOMATED SETUP & RUN")
print("="*70 + "\n")

# Step 1: Navigate to governance_weekly directory
project_dir = os.path.join(os.path.dirname(__file__), 'governance_weekly')
if not os.path.exists(project_dir):
    print(f"❌ Directory not found: {project_dir}")
    sys.exit(1)

os.chdir(project_dir)
print(f"📁 Working directory: {os.getcwd()}\n")

# Step 2: Check if venv exists, create if not
venv_dir = 'venv'
venv_python = os.path.join(venv_dir, 'Scripts', 'python.exe') if platform.system() == 'Windows' else os.path.join(venv_dir, 'bin', 'python')
venv_pip = os.path.join(venv_dir, 'Scripts', 'pip.exe') if platform.system() == 'Windows' else os.path.join(venv_dir, 'bin', 'pip')

if not os.path.exists(venv_dir):
    print("📦 Virtual environment not found. Creating...")
    if not run_command(f'python -m venv {venv_dir}', "Create virtual environment"):
        sys.exit(1)
else:
    print("✅ Virtual environment exists")

# Step 3: Check if requirements are installed
print("\n📋 Checking dependencies...")
requirements_file = 'requirements.txt'
needs_install = False

if os.path.exists(requirements_file):
    # Check if packages are installed by trying to import key packages
    try:
        result = subprocess.run(
            f'{venv_python} -c "import googletrans, reportlab, selenium, bs4"',
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            needs_install = True
            print("⚠️  Some packages missing")
    except:
        needs_install = True
        print("⚠️  Dependencies need to be installed")
else:
    print("⚠️  requirements.txt not found")

# Install requirements if needed
if needs_install and os.path.exists(requirements_file):
    print("\n📥 Installing requirements...")
    if not run_command(f'{venv_pip} install -r {requirements_file}', "Install dependencies"):
        print("⚠️  Some packages may have failed to install, continuing anyway...")
else:
    print("✅ All dependencies installed")

# Step 4: Run the scraping pipeline
print("\n" + "="*70)
print("🚀 STARTING GOVERNANCE WEEKLY PIPELINE")
print("="*70 + "\n")

print("This will:")
print("  1. Clear old data and PDFs")
print("  2. Scrape 10 news sources")
print("  3. Translate Nepali → English")
print("  4. Classify and filter articles")
print("  5. Generate PDF report")
print("  6. Open the PDF")
print()

# Run the pipeline with activated venv
if platform.system() == 'Windows':
    # Windows: Activate venv and run RUN.py
    activate_script = os.path.join(venv_dir, 'Scripts', 'activate.bat')
    cmd = f'call {activate_script} && python RUN.py'
    result = subprocess.run(cmd, shell=True)
else:
    # Linux/Mac: Source venv and run RUN.py
    activate_script = os.path.join(venv_dir, 'bin', 'activate')
    cmd = f'source {activate_script} && python RUN.py'
    result = subprocess.run(cmd, shell=True, executable='/bin/bash')

if result.returncode == 0:
    print("\n" + "="*70)
    print("🎉 SUCCESS! Pipeline completed.")
    print("="*70 + "\n")
else:
    print("\n" + "="*70)
    print("❌ Pipeline failed. Check errors above.")
    print("="*70 + "\n")
    sys.exit(1)

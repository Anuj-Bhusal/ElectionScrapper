@echo off
REM Complete Governance Weekly Pipeline - Windows Batch Script
REM Run this to execute the full weekly workflow

cd /d "%~dp0"
echo.
echo ============================================================
echo    GOVERNANCE WEEKLY - ONE-COMMAND PIPELINE
echo ============================================================
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Delete all old data
echo Deleting old database and PDFs...
if exist data\gov_weekly.db (
    python -c "import sqlite3; conn = sqlite3.connect('data/gov_weekly.db'); conn.execute('DELETE FROM articles'); conn.commit(); conn.close(); print('Database cleared')"
)

if exist output\*.pdf (
    del /Q output\*.pdf
    echo Old PDFs deleted
)

echo.
echo ============================================================
echo STEP 1: COLLECTING ARTICLES (10 sources)
echo ============================================================
python main.py --mode collect

echo.
echo ============================================================
echo STEP 2: GENERATING PDF REPORT
echo ============================================================
python main.py --mode summarize

echo.
echo ============================================================
echo STEP 3: OPENING PDF
echo ============================================================
for %%f in (output\GovernanceWeekly_*.pdf) do (
    echo Opening: %%f
    start "" "%%f"
)

echo.
echo ============================================================
echo    PIPELINE COMPLETE!
echo ============================================================
echo.
pause

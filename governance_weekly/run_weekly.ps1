# Complete Governance Weekly Pipeline - PowerShell Script
# Run this to execute the full weekly workflow

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   GOVERNANCE WEEKLY - ONE-COMMAND PIPELINE" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Delete old database
Write-Host "Deleting old database and PDFs..." -ForegroundColor Yellow
if (Test-Path "data\gov_weekly.db") {
    python -c "import sqlite3; conn = sqlite3.connect('data/gov_weekly.db'); conn.execute('DELETE FROM articles'); conn.commit(); conn.close(); print('✓ Database cleared')"
}

# Delete old PDFs
if (Test-Path "output\*.pdf") {
    Remove-Item "output\*.pdf" -Force
    Write-Host "✓ Old PDFs deleted" -ForegroundColor Green
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "STEP 1: COLLECTING ARTICLES (10 sources)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
python main.py --mode collect

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Collection failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "STEP 2: GENERATING PDF REPORT" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
python main.py --mode summarize

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Report generation failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "STEP 3: OPENING PDF" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$pdf = Get-ChildItem "output\GovernanceWeekly_*.pdf" | Select-Object -First 1
if ($pdf) {
    Write-Host "Opening: $($pdf.Name)" -ForegroundColor Green
    Invoke-Item $pdf.FullName
} else {
    Write-Host "⚠️  No PDF found!" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "   ✅ PIPELINE COMPLETE!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

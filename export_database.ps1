# PowerShell script for PlayStation Store Crawler Database Export
# Run this script with: .\export_database.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PlayStation Store Crawler Database Export" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python and try again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if mysqldump is available
try {
    $mysqldumpVersion = mysqldump --version 2>&1
    Write-Host "✅ mysqldump found: $mysqldumpVersion" -ForegroundColor Green
    Write-Host "Using standard export method..." -ForegroundColor Green
    Write-Host ""
    
    # Run the standard export script
    try {
        python export_database.py
        Write-Host ""
        Write-Host "✅ Export process completed!" -ForegroundColor Green
        Write-Host "Check the Export folder for the generated files." -ForegroundColor White
    } catch {
        Write-Host "❌ Error during export: $_" -ForegroundColor Red
    }
} catch {
    Write-Host "⚠️  WARNING: mysqldump is not found in PATH" -ForegroundColor Yellow
    Write-Host "Using Python-based export instead..." -ForegroundColor Green
    Write-Host ""
    
    # Run the Python-based export script
    try {
        python export_database_python.py
        Write-Host ""
        Write-Host "✅ Export process completed!" -ForegroundColor Green
        Write-Host "Check the Export folder for the generated files." -ForegroundColor White
    } catch {
        Write-Host "❌ Error during export: $_" -ForegroundColor Red
    }
}

Write-Host ""
Read-Host "Press Enter to exit" 
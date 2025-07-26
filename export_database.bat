@echo off
echo ========================================
echo PlayStation Store Crawler Database Export
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if mysqldump is available
mysqldump --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: mysqldump is not found in PATH
    echo Using Python-based export instead...
    echo.
    python export_database_python.py
) else (
    echo mysqldump found, using standard export...
    echo.
    python export_database.py
)

echo.
echo Export process completed!
echo Check the Export folder for the generated files.
echo.
pause 
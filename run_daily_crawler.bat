@echo off
REM PlayStation Store Crawler - Daily Automation Script
REM This file runs the PlayStation Store crawler automatically

echo Starting PlayStation Store Crawler at %date% %time%

REM Change to the script directory (where this batch file is located)
cd /d "%~dp0"

REM Run the Python crawler
python main_crawler.py

REM Check if the script ran successfully
if %ERRORLEVEL% EQU 0 (
    echo Crawler completed successfully at %date% %time%
) else (
    echo Crawler failed with error code %ERRORLEVEL% at %date% %time%
)

REM Optional: Uncomment the line below if you want to see the output when testing
REM pause 
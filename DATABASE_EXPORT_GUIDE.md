# Database Export Guide

## Overview

This guide explains how to export your MySQL database to a `.sql` file for sharing with teammates. The PlayStation Store Crawler includes multiple export methods to accommodate different system configurations.

## Quick Start

### For Windows Users (Recommended)
1. **Double-click** `export_database.bat` 
2. **Or run** `.\export_database.ps1` in PowerShell
3. Check the `Export/` folder for your `.sql` file

### For Command Line Users
```bash
# Test your setup first
python test_export.py

# Export full database
python export_database_python.py

# Export only structure (no data)
python export_database_python.py --schema-only
```

## Export Methods

### Method 1: Standard Export (requires mysqldump)
- **File**: `export_database.py`
- **Requirements**: MySQL tools installed with `mysqldump` in PATH
- **Pros**: Faster, more efficient, industry standard
- **Cons**: Requires MySQL installation

### Method 2: Pure Python Export (recommended)
- **File**: `export_database_python.py`
- **Requirements**: Only Python + MySQL connector
- **Pros**: No additional tools needed, works everywhere
- **Cons**: Slower for very large datasets

## What Gets Exported

✅ **Complete database structure**
- Tables, indexes, constraints
- Character sets and collations
- Foreign key relationships

✅ **All data**
- 1,241+ records from `preorder_games` table
- Historical PlayStation Store data
- Region-specific game information

✅ **Import instructions**
- Step-by-step import guide
- Multiple import methods
- Troubleshooting tips

## File Structure

After export, you'll find these files in the `Export/` folder:

```
Export/
├── playstation_crawler_export_python_YYYYMMDD_HHMMSS.sql  # Main export file
├── IMPORT_INSTRUCTIONS_PYTHON.md                          # Import guide
└── [previous exports...]                                  # Historical exports
```

## Sharing with Teammates

### Step 1: Export
```bash
# Windows
.\export_database.bat

# Command line
python export_database_python.py
```

### Step 2: Share Files
- Send the `.sql` file to your teammates
- Include the `IMPORT_INSTRUCTIONS_PYTHON.md` file
- File size: ~8.25 MB (with 1,241 records)

### Step 3: Teammates Import
Your teammates can import using:
- **MySQL Workbench** (GUI)
- **Command line** (mysql client)
- **phpMyAdmin** (web interface)

## Import Instructions for Teammates

### Prerequisites
- MySQL Server installed
- MySQL command line client available
- Sufficient permissions

### Quick Import
```bash
# 1. Create database
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS playstation_crawler CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 2. Import data
mysql -u root -p playstation_crawler < playstation_crawler_export_python_YYYYMMDD_HHMMSS.sql
```

### Verify Import
```sql
USE playstation_crawler;
SHOW TABLES;
SELECT COUNT(*) FROM preorder_games;
```

## Troubleshooting

### Common Issues

**"Database connection failed"**
- Check MySQL server is running
- Verify credentials in `config.py`
- Ensure database exists

**"mysqldump not found"**
- Use `export_database_python.py` instead
- Or install MySQL tools and add to PATH

**"Permission denied"**
- Run as administrator (Windows)
- Check file write permissions
- Ensure Export folder is writable

**"Import fails"**
- Check MySQL version compatibility (5.7+)
- Increase `max_allowed_packet` if file is large
- Verify character set settings

### Testing Your Setup
```bash
python test_export.py
```

This will test:
- Database connection
- mysqldump availability
- Export directory permissions

## Advanced Usage

### Export Only Schema
```bash
python export_database_python.py --schema-only
```
Creates a small file with just table structure (no data).

### Custom Export Directory
Edit the export scripts to change the output directory:
```python
export_dir = "CustomExport"  # Change this line
```

### Automated Exports
Add to your daily automation:
```bash
# Add to your batch file or cron job
python export_database_python.py
```

## File Formats

### SQL Export Format
- **Encoding**: UTF-8
- **Character Set**: utf8mb4
- **Format**: Standard MySQL dump
- **Compatibility**: MySQL 5.7+, MariaDB 10.2+

### File Naming Convention
```
playstation_crawler_export_python_YYYYMMDD_HHMMSS.sql
```
- `YYYYMMDD`: Date (20250723)
- `HHMMSS`: Time (093035)
- Timestamped to avoid conflicts

## Security Considerations

- Export files contain database credentials (in comments)
- Share files securely (encrypted transfer)
- Consider removing sensitive data before sharing
- Use schema-only export for sensitive environments

## Support

If you encounter issues:
1. Run `python test_export.py` to diagnose problems
2. Check the log files for detailed error messages
3. Verify your MySQL installation and permissions
4. Ensure all Python dependencies are installed

## Examples

### Successful Export Output
```
Exporting database 'playstation_crawler' to Export\playstation_crawler_export_python_20250723_093035.sql...
Database host: localhost:3306
Database user: root
Exporting table structure...
Exporting data from table 'preorder_games'...
  Exported 1000 of 1241 rows...
  Exported 1241 of 1241 rows...
✅ Database export completed successfully!
📁 Export file: Export\playstation_crawler_export_python_20250723_093035.sql
📊 File size: 8.25 MB
📝 Import instructions created: Export\IMPORT_INSTRUCTIONS_PYTHON.md
```

This guide covers all aspects of database export functionality. The system automatically chooses the best export method based on your system configuration. 
#!/usr/bin/env python3
"""
Database Export Script for PlayStation Store Crawler
Exports the MySQL database to a .sql file for sharing with teammates
"""

import os
import subprocess
import sys
from datetime import datetime
from config import get_db_config

def export_database():
    """
    Export the MySQL database to a .sql file
    """
    # Get database configuration
    db_config = get_db_config()
    
    # Create export directory if it doesn't exist
    export_dir = "Export"
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"playstation_crawler_export_{timestamp}.sql"
    filepath = os.path.join(export_dir, filename)
    
    # Build mysqldump command
    mysqldump_cmd = [
        "mysqldump",
        f"--host={db_config['host']}",
        f"--user={db_config['user']}",
        f"--password={db_config['password']}",
        f"--port={db_config['port']}",
        "--single-transaction",  # Consistent backup
        "--routines",           # Include stored procedures
        "--triggers",           # Include triggers
        "--events",             # Include events
        "--add-drop-database",  # Add DROP DATABASE statement
        "--add-drop-table",     # Add DROP TABLE statements
        "--create-options",     # Include all MySQL-specific table options
        "--complete-insert",    # Use complete INSERT statements
        "--extended-insert",    # Use multiple-row INSERT syntax
        "--set-charset",        # Add SET NAMES statements
        "--default-character-set=utf8mb4",
        db_config['database']
    ]
    
    try:
        print(f"Exporting database '{db_config['database']}' to {filepath}...")
        print(f"Database host: {db_config['host']}:{db_config['port']}")
        print(f"Database user: {db_config['user']}")
        
        # Execute mysqldump command
        with open(filepath, 'w', encoding='utf-8') as output_file:
            result = subprocess.run(
                mysqldump_cmd,
                stdout=output_file,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
        
        # Check file size
        file_size = os.path.getsize(filepath)
        file_size_mb = file_size / (1024 * 1024)
        
        print(f"✅ Database export completed successfully!")
        print(f"📁 Export file: {filepath}")
        print(f"📊 File size: {file_size_mb:.2f} MB")
        
        # Create a README file with import instructions
        create_import_instructions(export_dir, filename, db_config)
        
        return filepath
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during database export: {e}")
        print(f"Error details: {e.stderr}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def create_import_instructions(export_dir, filename, db_config):
    """
    Create a README file with instructions for importing the database
    """
    readme_content = f"""# Database Import Instructions

## File Information
- **Export Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Database Name**: {db_config['database']}
- **Export File**: {filename}

## Prerequisites
1. MySQL Server installed on your system
2. MySQL command line client (mysql) available
3. Sufficient permissions to create databases

## Import Steps

### Method 1: Command Line Import
```bash
# 1. Create the database (if it doesn't exist)
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS {db_config['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 2. Import the database
mysql -u root -p {db_config['database']} < {filename}
```

### Method 2: Using MySQL Workbench
1. Open MySQL Workbench
2. Connect to your MySQL server
3. Go to Server → Data Import
4. Select "Import from Self-Contained File"
5. Browse and select the {filename} file
6. Select the target schema (create new if needed)
7. Click "Start Import"

### Method 3: Using phpMyAdmin
1. Access phpMyAdmin
2. Create a new database named "{db_config['database']}"
3. Select the database
4. Go to Import tab
5. Choose the {filename} file
6. Click "Go" to import

## Database Structure
The exported database contains the following tables:
- `preorder_games`: Stores PlayStation Store preorder game data by region and date

## Verification
After import, you can verify the data by running:
```sql
USE {db_config['database']};
SHOW TABLES;
SELECT COUNT(*) FROM preorder_games;
```

## Troubleshooting
- If you get permission errors, ensure your MySQL user has CREATE and INSERT privileges
- If the import fails, check that the MySQL version is compatible (5.7+ recommended)
- For large files, you may need to increase max_allowed_packet in MySQL configuration

## Support
If you encounter issues, please contact the database administrator.
"""
    
    readme_path = os.path.join(export_dir, "IMPORT_INSTRUCTIONS.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"📝 Import instructions created: {readme_path}")

def export_schema_only():
    """
    Export only the database schema (structure) without data
    """
    db_config = get_db_config()
    
    export_dir = "Export"
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"playstation_crawler_schema_{timestamp}.sql"
    filepath = os.path.join(export_dir, filename)
    
    mysqldump_cmd = [
        "mysqldump",
        f"--host={db_config['host']}",
        f"--user={db_config['user']}",
        f"--password={db_config['password']}",
        f"--port={db_config['port']}",
        "--no-data",           # Only structure, no data
        "--routines",          # Include stored procedures
        "--triggers",          # Include triggers
        "--events",            # Include events
        "--add-drop-database",
        "--add-drop-table",
        "--create-options",
        "--set-charset",
        "--default-character-set=utf8mb4",
        db_config['database']
    ]
    
    try:
        print(f"Exporting database schema to {filepath}...")
        
        with open(filepath, 'w', encoding='utf-8') as output_file:
            result = subprocess.run(
                mysqldump_cmd,
                stdout=output_file,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
        
        file_size = os.path.getsize(filepath)
        file_size_kb = file_size / 1024
        
        print(f"✅ Schema export completed successfully!")
        print(f"📁 Schema file: {filepath}")
        print(f"📊 File size: {file_size_kb:.2f} KB")
        
        return filepath
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during schema export: {e}")
        print(f"Error details: {e.stderr}")
        return None

def main():
    """
    Main function to handle command line arguments
    """
    if len(sys.argv) > 1:
        if sys.argv[1] == "--schema-only":
            export_schema_only()
        elif sys.argv[1] == "--help":
            print("""
Database Export Script Usage:
    python export_database.py              # Export full database with data
    python export_database.py --schema-only # Export only database structure
    python export_database.py --help       # Show this help message
            """)
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Use --help for usage information")
    else:
        export_database()

if __name__ == "__main__":
    main() 
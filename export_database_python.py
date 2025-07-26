#!/usr/bin/env python3
"""
Pure Python Database Export Script for PlayStation Store Crawler
Exports the MySQL database to a .sql file without requiring mysqldump
"""

import os
import sys
from datetime import datetime
from config import get_db_config
from database_utils import DatabaseManager

def export_database_python():
    """
    Export the MySQL database to a .sql file using pure Python
    """
    # Get database configuration
    db_config = get_db_config()
    
    # Create export directory if it doesn't exist
    export_dir = "Export"
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"playstation_crawler_export_python_{timestamp}.sql"
    filepath = os.path.join(export_dir, filename)
    
    # Connect to database
    db_manager = DatabaseManager()
    if not db_manager.connect():
        print("❌ Failed to connect to database")
        return None
    
    try:
        print(f"Exporting database '{db_config['database']}' to {filepath}...")
        print(f"Database host: {db_config['host']}:{db_config['port']}")
        print(f"Database user: {db_config['user']}")
        
        with open(filepath, 'w', encoding='utf-8') as sql_file:
            # Write header
            sql_file.write(f"-- PlayStation Store Crawler Database Export\n")
            sql_file.write(f"-- Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            sql_file.write(f"-- Database: {db_config['database']}\n")
            sql_file.write(f"-- Host: {db_config['host']}:{db_config['port']}\n")
            sql_file.write(f"-- User: {db_config['user']}\n")
            sql_file.write(f"--\n\n")
            
            # Set character set
            sql_file.write("SET NAMES utf8mb4;\n")
            sql_file.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")
            
            # Create database
            sql_file.write(f"DROP DATABASE IF EXISTS `{db_config['database']}`;\n")
            sql_file.write(f"CREATE DATABASE `{db_config['database']}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\n")
            sql_file.write(f"USE `{db_config['database']}`;\n\n")
            
            # Get table structure
            print("Exporting table structure...")
            db_manager.cursor.execute("SHOW TABLES")
            tables = db_manager.cursor.fetchall()
            
            for (table_name,) in tables:
                sql_file.write(f"-- Table structure for table `{table_name}`\n")
                sql_file.write(f"DROP TABLE IF EXISTS `{table_name}`;\n")
                
                # Get CREATE TABLE statement
                db_manager.cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
                create_table_result = db_manager.cursor.fetchone()
                if create_table_result:
                    create_table_sql = create_table_result[1]
                    sql_file.write(f"{create_table_sql};\n\n")
                
                # Export data
                print(f"Exporting data from table '{table_name}'...")
                db_manager.cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                row_count = db_manager.cursor.fetchone()[0]
                
                if row_count > 0:
                    sql_file.write(f"-- Data for table `{table_name}`\n")
                    
                    # Get column names
                    db_manager.cursor.execute(f"DESCRIBE `{table_name}`")
                    columns = [column[0] for column in db_manager.cursor.fetchall()]
                    
                    # Get data in batches to avoid memory issues
                    batch_size = 1000
                    offset = 0
                    
                    while offset < row_count:
                        db_manager.cursor.execute(f"SELECT * FROM `{table_name}` LIMIT {batch_size} OFFSET {offset}")
                        rows = db_manager.cursor.fetchall()
                        
                        if rows:
                            # Write INSERT statement
                            sql_file.write(f"INSERT INTO `{table_name}` (`{'`, `'.join(columns)}`) VALUES\n")
                            
                            values_list = []
                            for row in rows:
                                # Escape and format values
                                formatted_values = []
                                for value in row:
                                    if value is None:
                                        formatted_values.append("NULL")
                                    elif isinstance(value, (int, float)):
                                        formatted_values.append(str(value))
                                    else:
                                        # Escape single quotes and format as string
                                        escaped_value = str(value).replace("'", "''")
                                        formatted_values.append(f"'{escaped_value}'")
                                
                                values_list.append(f"({', '.join(formatted_values)})")
                            
                            sql_file.write(',\n'.join(values_list))
                            sql_file.write(";\n\n")
                        
                        offset += batch_size
                        print(f"  Exported {min(offset, row_count)} of {row_count} rows...")
                
                else:
                    sql_file.write(f"-- No data in table `{table_name}`\n\n")
            
            # Restore foreign key checks
            sql_file.write("SET FOREIGN_KEY_CHECKS = 1;\n")
        
        # Check file size
        file_size = os.path.getsize(filepath)
        file_size_mb = file_size / (1024 * 1024)
        
        print(f"✅ Database export completed successfully!")
        print(f"📁 Export file: {filepath}")
        print(f"📊 File size: {file_size_mb:.2f} MB")
        
        # Create import instructions
        create_import_instructions_python(export_dir, filename, db_config)
        
        return filepath
        
    except Exception as e:
        print(f"❌ Error during database export: {e}")
        return None
    finally:
        db_manager.disconnect()

def create_import_instructions_python(export_dir, filename, db_config):
    """
    Create a README file with instructions for importing the database
    """
    readme_content = f"""# Database Import Instructions (Python Export)

## File Information
- **Export Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Database Name**: {db_config['database']}
- **Export File**: {filename}
- **Export Method**: Pure Python (no mysqldump required)

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
    
    readme_path = os.path.join(export_dir, "IMPORT_INSTRUCTIONS_PYTHON.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"📝 Import instructions created: {readme_path}")

def export_schema_only_python():
    """
    Export only the database schema (structure) without data
    """
    db_config = get_db_config()
    
    export_dir = "Export"
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"playstation_crawler_schema_python_{timestamp}.sql"
    filepath = os.path.join(export_dir, filename)
    
    # Connect to database
    db_manager = DatabaseManager()
    if not db_manager.connect():
        print("❌ Failed to connect to database")
        return None
    
    try:
        print(f"Exporting database schema to {filepath}...")
        
        with open(filepath, 'w', encoding='utf-8') as sql_file:
            # Write header
            sql_file.write(f"-- PlayStation Store Crawler Database Schema Export\n")
            sql_file.write(f"-- Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            sql_file.write(f"-- Database: {db_config['database']}\n")
            sql_file.write(f"-- Export Type: Schema Only (No Data)\n")
            sql_file.write(f"--\n\n")
            
            # Set character set
            sql_file.write("SET NAMES utf8mb4;\n")
            sql_file.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")
            
            # Create database
            sql_file.write(f"DROP DATABASE IF EXISTS `{db_config['database']}`;\n")
            sql_file.write(f"CREATE DATABASE `{db_config['database']}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\n")
            sql_file.write(f"USE `{db_config['database']}`;\n\n")
            
            # Get table structure
            db_manager.cursor.execute("SHOW TABLES")
            tables = db_manager.cursor.fetchall()
            
            for (table_name,) in tables:
                sql_file.write(f"-- Table structure for table `{table_name}`\n")
                sql_file.write(f"DROP TABLE IF EXISTS `{table_name}`;\n")
                
                # Get CREATE TABLE statement
                db_manager.cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
                create_table_result = db_manager.cursor.fetchone()
                if create_table_result:
                    create_table_sql = create_table_result[1]
                    sql_file.write(f"{create_table_sql};\n\n")
            
            # Restore foreign key checks
            sql_file.write("SET FOREIGN_KEY_CHECKS = 1;\n")
        
        # Check file size
        file_size = os.path.getsize(filepath)
        file_size_kb = file_size / 1024
        
        print(f"✅ Schema export completed successfully!")
        print(f"📁 Schema file: {filepath}")
        print(f"📊 File size: {file_size_kb:.2f} KB")
        
        return filepath
        
    except Exception as e:
        print(f"❌ Error during schema export: {e}")
        return None
    finally:
        db_manager.disconnect()

def main():
    """
    Main function to handle command line arguments
    """
    if len(sys.argv) > 1:
        if sys.argv[1] == "--schema-only":
            export_schema_only_python()
        elif sys.argv[1] == "--help":
            print("""
Pure Python Database Export Script Usage:
    python export_database_python.py              # Export full database with data
    python export_database_python.py --schema-only # Export only database structure
    python export_database_python.py --help       # Show this help message

Note: This script does not require mysqldump to be installed.
            """)
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Use --help for usage information")
    else:
        export_database_python()

if __name__ == "__main__":
    main() 
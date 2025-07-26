#!/usr/bin/env python3
"""
Script to export MySQL preorder_games table to SQLite database file
PRESERVING THE ORIGINAL TABLE STRUCTURE
"""

import sqlite3
import mysql.connector
from mysql.connector import Error
import os
import json
from datetime import datetime
from config import get_db_config

def export_to_sqlite_original():
    """
    Export preorder_games table from MySQL to SQLite database file
    PRESERVING THE ORIGINAL STRUCTURE WITH game_info JSON COLUMN
    """
    # Get MySQL configuration
    mysql_config = get_db_config()
    
    # SQLite file path (save to desktop)
    desktop_path = os.path.expanduser("~/Desktop")
    sqlite_file = os.path.join(desktop_path, "preorderGames_original.db")
    
    print(f"🔄 Starting export from MySQL to SQLite (ORIGINAL STRUCTURE)...")
    print(f"📁 SQLite file will be saved to: {sqlite_file}")
    print(f"🗄️  MySQL Database: {mysql_config['database']}")
    print(f"📊 Table: preorder_games (with game_info JSON column)")
    
    # Connect to MySQL
    try:
        mysql_conn = mysql.connector.connect(**mysql_config)
        mysql_cursor = mysql_conn.cursor()
        print("✅ Connected to MySQL database")
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return False
    
    # Connect to SQLite (this will create the file if it doesn't exist)
    try:
        sqlite_conn = sqlite3.connect(sqlite_file)
        sqlite_cursor = sqlite_conn.cursor()
        print("✅ Connected to SQLite database")
    except Error as e:
        print(f"❌ Error creating SQLite database: {e}")
        mysql_conn.close()
        return False
    
    try:
        # Create the preorder_games table in SQLite with ORIGINAL structure
        print("📋 Creating table structure in SQLite (ORIGINAL FORMAT)...")
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS preorder_games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crawl_date DATE NOT NULL,
            region VARCHAR(10) NOT NULL,
            game_info TEXT NOT NULL
        )
        """
        sqlite_cursor.execute(create_table_sql)
        
        # Create indexes for better performance
        sqlite_cursor.execute("CREATE INDEX IF NOT EXISTS idx_crawl_date ON preorder_games(crawl_date)")
        sqlite_cursor.execute("CREATE INDEX IF NOT EXISTS idx_region ON preorder_games(region)")
        
        # Get all data from MySQL with ORIGINAL structure
        print("📥 Fetching data from MySQL...")
        mysql_cursor.execute("SELECT id, crawl_date, region, game_info FROM preorder_games ORDER BY id")
        rows = mysql_cursor.fetchall()
        
        if not rows:
            print("⚠️  No data found in MySQL preorder_games table")
            return False
        
        print(f"📊 Found {len(rows)} records to export")
        
        # Insert data into SQLite (keeping original structure)
        print("📤 Inserting data into SQLite...")
        insert_sql = """
        INSERT INTO preorder_games (id, crawl_date, region, game_info)
        VALUES (?, ?, ?, ?)
        """
        
        # Use executemany for better performance
        sqlite_cursor.executemany(insert_sql, rows)
        
        # Commit the changes
        sqlite_conn.commit()
        
        # Verify the export
        sqlite_cursor.execute("SELECT COUNT(*) FROM preorder_games")
        sqlite_count = sqlite_cursor.fetchone()[0]
        
        print(f"✅ Export completed successfully!")
        print(f"📊 Records exported: {sqlite_count}")
        print(f"💾 SQLite file: {sqlite_file}")
        
        # Show some sample data
        print("\n📋 Sample data from SQLite (ORIGINAL FORMAT):")
        sqlite_cursor.execute("SELECT id, crawl_date, region, game_info FROM preorder_games LIMIT 3")
        sample_rows = sqlite_cursor.fetchall()
        for row in sample_rows:
            id_val, crawl_date, region, game_info = row
            try:
                games = json.loads(game_info)
                print(f"  ID: {id_val}, Date: {crawl_date}, Region: {region}")
                print(f"    Games in JSON: {len(games)} games")
                if games:
                    print(f"    First game: {games[0].get('game_name', 'N/A')} (Rank: {games[0].get('display_rank', 'N/A')})")
                print()
            except json.JSONDecodeError:
                print(f"  ID: {id_val}, Date: {crawl_date}, Region: {region}")
                print(f"    JSON data: {game_info[:100]}...")
                print()
        
        return True
        
    except Error as e:
        print(f"❌ Error during export: {e}")
        return False
    finally:
        # Close connections
        mysql_cursor.close()
        mysql_conn.close()
        sqlite_cursor.close()
        sqlite_conn.close()
        print("🔒 Database connections closed")

def test_sqlite_file_original():
    """
    Test the exported SQLite file to ensure it's working correctly
    """
    desktop_path = os.path.expanduser("~/Desktop")
    sqlite_file = os.path.join(desktop_path, "preorderGames_original.db")
    
    if not os.path.exists(sqlite_file):
        print("❌ SQLite file not found. Please run the export first.")
        return False
    
    try:
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()
        
        # Test basic queries
        cursor.execute("SELECT COUNT(*) FROM preorder_games")
        count = cursor.fetchone()[0]
        print(f"✅ SQLite file test successful! Found {count} records")
        
        # Test JSON data
        cursor.execute("SELECT game_info FROM preorder_games LIMIT 1")
        result = cursor.fetchone()
        if result:
            try:
                games = json.loads(result[0])
                print(f"✅ JSON data is valid! Sample record contains {len(games)} games")
                print(f"🌍 Sample regions: {[r[0] for r in cursor.execute('SELECT DISTINCT region FROM preorder_games ORDER BY region LIMIT 5').fetchall()]}")
            except json.JSONDecodeError:
                print("❌ JSON data is not valid")
                return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error testing SQLite file: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🎮 PlayStation Store Crawler - MySQL to SQLite Export (ORIGINAL)")
    print("=" * 60)
    
    # Run the export
    success = export_to_sqlite_original()
    
    if success:
        print("\n" + "=" * 60)
        print("🧪 Testing exported SQLite file...")
        print("=" * 60)
        test_sqlite_file_original()
        
        print("\n" + "=" * 60)
        print("🎉 Export completed successfully!")
        print("📁 Your SQLite file is ready on your Desktop: preorderGames_original.db")
        print("🔧 This preserves your ORIGINAL table structure with game_info JSON column")
        print("=" * 60)
    else:
        print("\n❌ Export failed. Please check the error messages above.") 
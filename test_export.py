#!/usr/bin/env python3
"""
Test script to verify database connection and export functionality
"""

from database_utils import DatabaseManager
from config import get_db_config
import os

def test_database_connection():
    """Test if we can connect to the database"""
    print("Testing database connection...")
    
    db_manager = DatabaseManager()
    if db_manager.connect():
        print("✅ Database connection successful!")
        
        # Test if we can query the database
        try:
            db_manager.cursor.execute("SHOW TABLES")
            tables = db_manager.cursor.fetchall()
            print(f"✅ Found {len(tables)} tables in database")
            
            # Check if preorder_games table exists
            table_names = [table[0] for table in tables]
            if 'preorder_games' in table_names:
                print("✅ preorder_games table found")
                
                # Check table structure
                db_manager.cursor.execute("DESCRIBE preorder_games")
                columns = db_manager.cursor.fetchall()
                print(f"✅ Table has {len(columns)} columns")
                
                # Check data count
                db_manager.cursor.execute("SELECT COUNT(*) FROM preorder_games")
                count = db_manager.cursor.fetchone()[0]
                print(f"✅ Table contains {count} records")
                
            else:
                print("❌ preorder_games table not found")
                
        except Exception as e:
            print(f"❌ Error querying database: {e}")
            
        db_manager.disconnect()
        return True
    else:
        print("❌ Database connection failed!")
        return False

def test_mysqldump_availability():
    """Test if mysqldump is available"""
    print("\nTesting mysqldump availability...")
    
    try:
        import subprocess
        result = subprocess.run(['mysqldump', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ mysqldump is available")
            print(f"   Version: {result.stdout.strip()}")
            return True
        else:
            print("❌ mysqldump command failed")
            return False
    except FileNotFoundError:
        print("❌ mysqldump not found in PATH")
        print("   Please ensure MySQL is installed and mysqldump is in your PATH")
        return False
    except Exception as e:
        print(f"❌ Error testing mysqldump: {e}")
        return False

def test_export_directory():
    """Test if export directory can be created"""
    print("\nTesting export directory...")
    
    export_dir = "Export"
    try:
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
            print(f"✅ Created export directory: {export_dir}")
        else:
            print(f"✅ Export directory exists: {export_dir}")
        return True
    except Exception as e:
        print(f"❌ Error creating export directory: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Database Export Test Suite")
    print("=" * 50)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("mysqldump Availability", test_mysqldump_availability),
        ("Export Directory", test_export_directory)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! You can run the export script.")
        print("\nTo export your database, run:")
        print("  python export_database.py")
        print("  # or")
        print("  export_database.bat (Windows)")
    else:
        print("❌ Some tests failed. Please fix the issues before exporting.")
        print("\nCommon solutions:")
        print("1. Ensure MySQL server is running")
        print("2. Check database credentials in config.py")
        print("3. Install MySQL and add mysqldump to PATH")
        print("4. Ensure you have write permissions in the project directory")

if __name__ == "__main__":
    main() 
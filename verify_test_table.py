#!/usr/bin/env python3
"""
Script to verify that the test table was created successfully
"""

import mysql.connector
from config import LOCAL_DB_CONFIG

def verify_test_table():
    """Verify that the test table exists and has the correct structure"""
    try:
        # Connect to the database
        connection = mysql.connector.connect(**LOCAL_DB_CONFIG)
        cursor = connection.cursor()
        
        # Check if the test table exists
        cursor.execute("SHOW TABLES LIKE 'preorder_games_test'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("✅ Test table 'preorder_games_test' exists!")
            
            # Get table structure
            cursor.execute("DESCRIBE preorder_games_test")
            columns = cursor.fetchall()
            
            print("\n📋 Table structure:")
            print("-" * 50)
            for column in columns:
                print(f"  {column[0]:<15} {column[1]:<20} {column[2]:<10} {column[3]:<10} {column[4]:<10}")
            
            # Check indexes
            cursor.execute("SHOW INDEX FROM preorder_games_test")
            indexes = cursor.fetchall()
            
            print("\n🔍 Indexes:")
            print("-" * 30)
            for index in indexes:
                print(f"  {index[2]:<20} {index[4]:<15} {index[5]:<10}")
                
            print(f"\n✅ Test table is ready for use!")
            return True
            
        else:
            print("❌ Test table 'preorder_games_test' does not exist!")
            return False
            
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    verify_test_table() 
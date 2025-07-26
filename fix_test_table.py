#!/usr/bin/env python3
"""
Script to fix the test table structure to match the original table
"""

import mysql.connector
from mysql.connector import Error
from config import LOCAL_DB_CONFIG

def fix_test_table():
    """Fix the test table structure to match the original table"""
    try:
        # Connect to the database
        connection = mysql.connector.connect(**LOCAL_DB_CONFIG)
        cursor = connection.cursor()
        
        # Drop the existing test table
        cursor.execute("DROP TABLE IF EXISTS `preorder_games_test`")
        print("🗑️  Dropped existing test table")
        
        # Create the test table with the correct structure (JSON format like original)
        create_table_query = """
        CREATE TABLE `preorder_games_test` (
          `id` int NOT NULL AUTO_INCREMENT,
          `crawl_date` date NOT NULL,
          `region` varchar(10) NOT NULL,
          `game_info` json NOT NULL,
          PRIMARY KEY (`id`),
          UNIQUE KEY `unique_date_region` (`crawl_date`, `region`),
          KEY `idx_crawl_date` (`crawl_date`),
          KEY `idx_region` (`region`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
        """
        
        cursor.execute(create_table_query)
        print("✅ Created test table 'preorder_games_test' with correct structure")
        
        # Commit the changes
        connection.commit()
        print("✅ Changes committed to database")
        
        # Verify the table was created
        cursor.execute("SHOW TABLES LIKE 'preorder_games_test'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("\n🎉 Test table created successfully!")
            
            # Show table structure
            cursor.execute("DESCRIBE preorder_games_test")
            columns = cursor.fetchall()
            
            print("\n📋 Table structure:")
            print("-" * 80)
            print(f"{'Column':<15} {'Type':<20} {'Null':<8} {'Key':<8} {'Default':<15} {'Extra':<10}")
            print("-" * 80)
            for column in columns:
                field_name = column[0] if column[0] else 'NULL'
                field_type = column[1] if column[1] else 'NULL'
                field_null = column[2] if column[2] else 'NULL'
                field_key = column[3] if column[3] else 'NULL'
                field_default = str(column[4]) if column[4] is not None else 'NULL'
                field_extra = column[5] if column[5] else 'NULL'
                
                print(f"{field_name:<15} {field_type:<20} {field_null:<8} {field_key:<8} {field_default:<15} {field_extra:<10}")
            
            # Show indexes
            cursor.execute("SHOW INDEX FROM preorder_games_test")
            indexes = cursor.fetchall()
            
            print("\n🔍 Indexes:")
            print("-" * 50)
            for index in indexes:
                print(f"  {index[2]:<20} {index[4]:<15} {index[5]:<10}")
            
            print(f"\n✅ Test table is ready for use with JSON storage!")
            return True
        else:
            print("❌ Failed to create test table!")
            return False
            
    except Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Database connection closed")

if __name__ == "__main__":
    fix_test_table() 
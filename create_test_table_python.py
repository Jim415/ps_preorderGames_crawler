#!/usr/bin/env python3
"""
Script to create the test table for PlayStation Store Crawler
"""

import mysql.connector
from mysql.connector import Error
from config import LOCAL_DB_CONFIG

def create_test_table():
    """Create the test table with the same structure as the original table"""
    try:
        # Connect to the database
        connection = mysql.connector.connect(**LOCAL_DB_CONFIG)
        cursor = connection.cursor()
        
        # Drop the test table if it exists
        cursor.execute("DROP TABLE IF EXISTS `preorder_games_test`")
        print("🗑️  Dropped existing test table (if any)")
        
        # Create the test table with the same structure as the original table
        create_table_query = """
        CREATE TABLE `preorder_games_test` (
          `id` int NOT NULL AUTO_INCREMENT,
          `crawl_date` date NOT NULL,
          `region` varchar(10) NOT NULL,
          `game_name` text NOT NULL,
          `display_rank` int NOT NULL,
          PRIMARY KEY (`id`),
          KEY `idx_crawl_date` (`crawl_date`),
          KEY `idx_region` (`region`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
        """
        
        cursor.execute(create_table_query)
        print("✅ Created test table 'preorder_games_test'")
        
        # Add a unique constraint to prevent duplicate entries for the same date/region combination
        try:
            cursor.execute("""
                ALTER TABLE `preorder_games_test` 
                ADD UNIQUE KEY `unique_date_region` (`crawl_date`, `region`)
            """)
            print("✅ Added unique constraint on (crawl_date, region)")
        except Error as e:
            print(f"⚠️  Warning: Could not add unique constraint: {e}")
        
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
            print("-" * 60)
            print(f"{'Column':<15} {'Type':<20} {'Null':<8} {'Key':<8} {'Default':<10}")
            print("-" * 60)
            for column in columns:
                print(f"{column[0]:<15} {column[1]:<20} {column[2]:<8} {column[3]:<8} {str(column[4]):<10}")
            
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
    create_test_table() 
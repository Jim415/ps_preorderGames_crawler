#!/usr/bin/env python3
"""
Simple script to check the test table structure
"""

import mysql.connector
from config import LOCAL_DB_CONFIG

def check_table_structure():
    """Check the test table structure"""
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
            
            # Check if game_name column exists
            game_name_exists = any(col[0] == 'game_name' for col in columns)
            if game_name_exists:
                print("\n✅ game_name column exists!")
            else:
                print("\n❌ game_name column is missing!")
                print("Adding game_name column...")
                
                # Add the missing game_name column
                cursor.execute("""
                    ALTER TABLE preorder_games_test 
                    ADD COLUMN game_name text NOT NULL AFTER region
                """)
                connection.commit()
                print("✅ Added game_name column!")
                
                # Show updated structure
                cursor.execute("DESCRIBE preorder_games_test")
                columns = cursor.fetchall()
                
                print("\n📋 Updated table structure:")
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
    check_table_structure() 
#!/usr/bin/env python3
"""
Script to clear all data from the preorder_games table
"""

from database_utils import DatabaseManager

def clear_preorder_games_table():
    """Clear all rows from preorder_games table"""
    print("Clearing preorder_games table...")
    
    db_manager = DatabaseManager()
    
    try:
        # Connect to database
        if not db_manager.connect():
            print("❌ Failed to connect to database")
            return False
        
        # Count current rows
        db_manager.cursor.execute("SELECT COUNT(*) FROM preorder_games")
        row_count = db_manager.cursor.fetchone()[0]
        print(f"📊 Current rows in table: {row_count}")
        
        if row_count == 0:
            print("✅ Table is already empty")
            return True
        
        # Confirm deletion
        confirm = input(f"⚠️  Are you sure you want to delete all {row_count} rows? (y/N): ")
        if confirm.lower() != 'y':
            print("❌ Operation cancelled")
            return False
        
        # Clear the table
        db_manager.cursor.execute("DELETE FROM preorder_games")
        db_manager.connection.commit()
        
        # Verify deletion
        db_manager.cursor.execute("SELECT COUNT(*) FROM preorder_games")
        remaining_rows = db_manager.cursor.fetchone()[0]
        
        if remaining_rows == 0:
            print(f"✅ Successfully cleared {row_count} rows from preorder_games table")
            return True
        else:
            print(f"❌ Something went wrong. {remaining_rows} rows still remain")
            return False
            
    except Exception as e:
        print(f"❌ Error clearing table: {e}")
        return False
    finally:
        db_manager.disconnect()

if __name__ == "__main__":
    clear_preorder_games_table() 
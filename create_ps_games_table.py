#!/usr/bin/env python3
"""
Script to create the PS_games table for tracking specific games across regions
"""

import mysql.connector
from mysql.connector import Error
import logging
from config import DB_CONFIG

def create_ps_games_table():
    """Create the PS_games table with proper structure"""
    try:
        # Connect to database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("🔧 Creating PS_games table...")
        
        # Create table SQL
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS PS_games (
            game_name VARCHAR(255) NOT NULL,
            game_id VARCHAR(255) NOT NULL,
            region VARCHAR(10) NOT NULL,
            genre JSON,
            preorder_start_date DATE,
            official_release_date DATE,
            current_rank INT,
            rank_change VARCHAR(10),
            rank_history JSON,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (game_id, region),
            INDEX idx_game_name (game_name),
            INDEX idx_region (region),
            INDEX idx_current_rank (current_rank),
            INDEX idx_created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
        """
        
        cursor.execute(create_table_sql)
        connection.commit()
        
        print("✅ PS_games table created successfully!")
        
        # Verify table structure
        cursor.execute("DESCRIBE PS_games")
        columns = cursor.fetchall()
        
        print("\n📋 Table structure:")
        print("-" * 80)
        print(f"{'Column':<20} {'Type':<20} {'Null':<8} {'Key':<8} {'Default':<15}")
        print("-" * 80)
        for column in columns:
            print(f"{column[0]:<20} {column[1]:<20} {column[2]:<8} {column[3]:<8} {str(column[4]):<15}")
        
        # Check if table exists and has data
        cursor.execute("SELECT COUNT(*) FROM PS_games")
        count = cursor.fetchone()[0]
        print(f"\n📊 Current records in PS_games table: {count}")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 PS_games table is ready for use!")
        return True
        
    except Error as e:
        print(f"❌ Error creating PS_games table: {e}")
        return False

if __name__ == "__main__":
    create_ps_games_table() 
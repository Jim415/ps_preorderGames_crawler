#!/usr/bin/env python3
"""
Game tracking manager for updating PS_games table during daily crawler runs
"""

import mysql.connector
from mysql.connector import Error
import json
import logging
from datetime import datetime, date
from config import DB_CONFIG
from game_tracking_config import get_tracked_games, get_tracked_regions, TRACKING_TABLE_NAME

class GameTrackingManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor()
            logging.info("Game tracking manager connected to database")
            return True
        except Error as e:
            logging.error(f"Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logging.info("Game tracking manager disconnected")
    
    def update_game_tracking(self, region, games_data):
        """Update PS_games table with new data from crawler"""
        try:
            if not self.connection or not self.cursor:
                if not self.connect():
                    return False
            
            tracked_games = get_tracked_games()
            tracked_regions = get_tracked_regions()
            
            # Only process if this region is being tracked
            if region not in tracked_regions:
                return True
            
            today = date.today()
            updated_count = 0
            
            # Process each game in the crawled data
            for game in games_data:
                game_name = game['game_name']
                game_id = game['game_name']  # Using game_name as game_id
                current_rank = game['display_rank']
                
                # Check if this game matches any tracked games
                is_tracked = False
                tracked_game_name = None
                
                for tracked_game in tracked_games:
                    if tracked_game.lower() in game_name.lower():
                        is_tracked = True
                        tracked_game_name = tracked_game
                        break
                
                if not is_tracked:
                    continue
                
                # Get existing record for this game/region
                self.cursor.execute("""
                    SELECT current_rank, rank_history 
                    FROM PS_games 
                    WHERE game_id = %s AND region = %s
                """, (game_id, region))
                
                existing_record = self.cursor.fetchone()
                
                if existing_record:
                    # Update existing record
                    previous_rank, rank_history_json = existing_record
                    
                    try:
                        rank_history = json.loads(rank_history_json) if rank_history_json else []
                    except json.JSONDecodeError:
                        rank_history = []
                    
                    # Calculate rank change
                    if previous_rank is not None:
                        rank_diff = previous_rank - current_rank
                        if rank_diff > 0:
                            rank_change = f"+{rank_diff}"
                        elif rank_diff < 0:
                            rank_change = f"{rank_diff}"
                        else:
                            rank_change = "0"
                    else:
                        rank_change = "new"
                    
                    # Add new entry to rank history
                    rank_history.append({
                        "date": today.strftime("%Y-%m-%d"),
                        "rank": current_rank,
                        "change": rank_change
                    })
                    
                    # Update the record
                    self.cursor.execute("""
                        UPDATE PS_games 
                        SET current_rank = %s, rank_change = %s, rank_history = %s, updated_at = CURRENT_TIMESTAMP
                        WHERE game_id = %s AND region = %s
                    """, (current_rank, rank_change, json.dumps(rank_history), game_id, region))
                    
                else:
                    # Create new record
                    rank_history = [{
                        "date": today.strftime("%Y-%m-%d"),
                        "rank": current_rank,
                        "change": "new"
                    }]
                    
                    self.cursor.execute("""
                        INSERT INTO PS_games 
                        (game_name, game_id, region, current_rank, rank_change, rank_history)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (tracked_game_name, game_id, region, current_rank, "new", json.dumps(rank_history)))
                
                updated_count += 1
            
            if updated_count > 0:
                self.connection.commit()
                logging.info(f"Updated {updated_count} tracked games for region {region}")
            
            return True
            
        except Error as e:
            logging.error(f"Error updating game tracking for {region}: {e}")
            if self.connection:
                self.connection.rollback()
            return False
    
    def get_tracked_games_summary(self):
        """Get summary of tracked games"""
        try:
            if not self.connection or not self.cursor:
                if not self.connect():
                    return None
            
            self.cursor.execute("""
                SELECT 
                    game_name,
                    region,
                    current_rank,
                    rank_change,
                    JSON_LENGTH(rank_history) as history_count
                FROM PS_games 
                ORDER BY game_name, region
            """)
            
            results = self.cursor.fetchall()
            return results
            
        except Error as e:
            logging.error(f"Error getting tracked games summary: {e}")
            return None
    
    def get_game_history(self, game_id, region):
        """Get rank history for a specific game/region"""
        try:
            if not self.connection or not self.cursor:
                if not self.connect():
                    return None
            
            self.cursor.execute("""
                SELECT rank_history 
                FROM PS_games 
                WHERE game_id = %s AND region = %s
            """, (game_id, region))
            
            result = self.cursor.fetchone()
            if result and result[0]:
                return json.loads(result[0])
            return None
            
        except Error as e:
            logging.error(f"Error getting game history: {e}")
            return None 
#!/usr/bin/env python3
"""
Script to extract historical game data from preorder_games table and populate PS_games table
"""

import mysql.connector
from mysql.connector import Error
import json
import logging
from datetime import datetime, date
from config import DB_CONFIG
from game_tracking_config import get_tracked_games, get_tracked_regions, TRACKING_TABLE_NAME

def extract_game_data():
    """Extract historical data for tracked games and populate PS_games table"""
    try:
        # Connect to database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        tracked_games = get_tracked_games()
        tracked_regions = get_tracked_regions()
        
        print(f"🎯 Extracting data for {len(tracked_games)} games across {len(tracked_regions)} regions...")
        print(f"📋 Tracked games: {', '.join(tracked_games)}")
        print(f"🌍 Tracked regions: {', '.join(tracked_regions)}")
        
        total_extracted = 0
        
        # Process each tracked game
        for game_name in tracked_games:
            print(f"\n🎮 Processing game: {game_name}")
            
            # Find all game IDs that match this game name (including different packages)
            cursor.execute("""
                SELECT DISTINCT 
                    JSON_UNQUOTE(JSON_EXTRACT(game_info, '$[*].game_name')) as game_names,
                    crawl_date,
                    region,
                    game_info
                FROM preorder_games 
                WHERE JSON_SEARCH(game_info, 'one', %s, NULL, '$[*].game_name') IS NOT NULL
                ORDER BY region, crawl_date
            """, (f"%{game_name}%",))
            
            game_records = cursor.fetchall()
            
            if not game_records:
                print(f"   ⚠️  No data found for '{game_name}'")
                continue
            
            # Group by region and process each region separately
            region_data = {}
            for record in game_records:
                game_names, crawl_date, region, game_info_json = record
                
                if region not in tracked_regions:
                    continue
                
                if region not in region_data:
                    region_data[region] = []
                
                try:
                    game_info = json.loads(game_info_json)
                    region_data[region].append({
                        'crawl_date': crawl_date,
                        'game_info': game_info
                    })
                except json.JSONDecodeError:
                    continue
            
            # Process each region for this game
            for region in tracked_regions:
                if region not in region_data:
                    print(f"   ⚠️  No data for region '{region}'")
                    continue
                
                print(f"   🌍 Processing region: {region}")
                
                # Sort by date
                region_data[region].sort(key=lambda x: x['crawl_date'])
                
                # Extract all unique game IDs for this game in this region
                game_ids = set()
                for record in region_data[region]:
                    for game in record['game_info']:
                        if game_name.lower() in game['game_name'].lower():
                            game_ids.add(game['game_name'])  # Using game_name as game_id
                
                # Process each game ID (different packages)
                for game_id in game_ids:
                    print(f"      📦 Processing package: {game_id}")
                    
                    # Build rank history for this specific game ID
                    rank_history = []
                    previous_rank = None
                    
                    for record in region_data[region]:
                        crawl_date = record['crawl_date']
                        
                        # Find this specific game in the record
                        for game in record['game_info']:
                            if game['game_name'] == game_id:
                                current_rank = game['display_rank']
                                
                                # Calculate rank change
                                if previous_rank is None:
                                    rank_change = "new"
                                else:
                                    rank_diff = previous_rank - current_rank
                                    if rank_diff > 0:
                                        rank_change = f"+{rank_diff}"
                                    elif rank_diff < 0:
                                        rank_change = f"{rank_diff}"
                                    else:
                                        rank_change = "0"
                                
                                rank_history.append({
                                    "date": crawl_date.strftime("%Y-%m-%d"),
                                    "rank": current_rank,
                                    "change": rank_change
                                })
                                
                                previous_rank = current_rank
                                break
                    
                    if not rank_history:
                        continue
                    
                    # Get current rank and rank change
                    current_rank = rank_history[-1]['rank']
                    rank_change = rank_history[-1]['change']
                    
                    # Insert or update in PS_games table
                    insert_sql = """
                        INSERT INTO PS_games 
                        (game_name, game_id, region, current_rank, rank_change, rank_history)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        current_rank = VALUES(current_rank),
                        rank_change = VALUES(rank_change),
                        rank_history = VALUES(rank_history),
                        updated_at = CURRENT_TIMESTAMP
                    """
                    
                    values = (
                        game_name,
                        game_id,
                        region,
                        current_rank,
                        rank_change,
                        json.dumps(rank_history)
                    )
                    
                    cursor.execute(insert_sql, values)
                    total_extracted += 1
                    
                    print(f"         ✅ Extracted {len(rank_history)} rank records")
        
        connection.commit()
        
        print(f"\n🎉 Data extraction completed!")
        print(f"📊 Total game/region combinations extracted: {total_extracted}")
        
        # Show summary
        cursor.execute(f"SELECT COUNT(*) FROM {TRACKING_TABLE_NAME}")
        total_records = cursor.fetchone()[0]
        print(f"📋 Total records in {TRACKING_TABLE_NAME} table: {total_records}")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Error as e:
        print(f"❌ Error extracting game data: {e}")
        return False

if __name__ == "__main__":
    extract_game_data() 
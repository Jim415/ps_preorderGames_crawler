#!/usr/bin/env python3
"""
Test script to run the crawler on a single region to verify the new product ID extraction
"""

import logging
import time
from datetime import datetime
from main_crawler_test import PlayStationCrawler
from remove_duplicate_country_codes import unique_codes

def test_single_region():
    """Test the crawler on a single region"""
    print("🧪 Starting single region test...")
    print("=" * 50)
    
    # Use the first region for testing
    test_region = unique_codes[0]
    print(f"📍 Testing region: {test_region}")
    
    try:
        # Create crawler instance
        crawler = PlayStationCrawler()
        
        # Test database connection
        if not crawler.db_manager.test_connection():
            print("❌ Database connection failed!")
            return False
        
        print("✅ Database connection successful")
        
        # Connect to database
        if not crawler.db_manager.connect():
            print("❌ Failed to connect to database!")
            return False
        
        print("✅ Database connected")
        
        # Test crawling a single region
        print(f"\n🕷️  Crawling region: {test_region}")
        games = crawler.get_games_from_page(test_region)
        
        if games:
            print(f"✅ Found {len(games)} games for {test_region}")
            
            # Show first few games to verify the new product ID extraction
            print(f"\n📋 First 5 games (showing new product IDs):")
            print("-" * 80)
            for i, game in enumerate(games[:5]):
                print(f"{i+1}. Region: {game['region']}")
                print(f"   Product ID: {game['game_name']}")
                print(f"   Display Rank: {game['display_rank']}")
                print()
            
            # Insert games into test database
            print(f"💾 Inserting {len(games)} games into test database...")
            if crawler.db_manager.insert_games_for_region(test_region, games):
                print("✅ Successfully inserted games into test database")
                
                # Retrieve and verify the data
                print(f"\n🔍 Retrieving data from test database...")
                retrieved_data = crawler.db_manager.get_games_by_region(test_region)
                
                if retrieved_data:
                    print(f"✅ Retrieved {len(retrieved_data)} records from test database")
                    latest_record = retrieved_data[0]
                    print(f"📅 Latest crawl date: {latest_record['crawl_date']}")
                    print(f"🎮 Games in latest record: {len(latest_record['games'])}")
                    
                    # Show first few games from database
                    print(f"\n📋 First 3 games from database:")
                    print("-" * 60)
                    for i, game in enumerate(latest_record['games'][:3]):
                        print(f"{i+1}. Product ID: {game['game_name']}")
                        print(f"   Display Rank: {game['display_rank']}")
                        print()
                else:
                    print("❌ No data retrieved from test database")
            else:
                print("❌ Failed to insert games into test database")
        else:
            print(f"❌ No games found for {test_region}")
        
        # Cleanup
        crawler.db_manager.disconnect()
        if hasattr(crawler, 'driver'):
            crawler.driver.quit()
        
        print("\n🎉 Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    test_single_region() 
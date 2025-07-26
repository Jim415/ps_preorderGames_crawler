import mysql.connector
from mysql.connector import Error
import logging
import json
from datetime import date
from config import DB_CONFIG

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor()
            logging.info("Successfully connected to MySQL database")
            return True
        except Error as e:
            logging.error(f"Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logging.info("MySQL connection closed")
    
    def insert_games_for_region(self, region, games_data):
        """Insert all games for a region as JSON in a single row"""
        try:
            # Convert games list to JSON format
            game_info = []
            for game in games_data:
                game_info.append({
                    "game_name": game['game_name'],
                    "display_rank": game['display_rank']
                })
            
            game_info_json = json.dumps(game_info)
            today = date.today()
            
            # Insert or update if same date/region already exists
            query = """
                INSERT INTO preorder_games (crawl_date, region, game_info)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE game_info = VALUES(game_info)
            """
            values = (today, region, game_info_json)
            self.cursor.execute(query, values)
            self.connection.commit()
            
            logging.info(f"Successfully inserted {len(games_data)} games for region {region}")
            return True
            
        except Error as e:
            logging.error(f"Error inserting games for {region}: {e}")
            self.connection.rollback()
            return False
    
    def get_games_by_region(self, region, crawl_date=None):
        """Get games for a specific region, optionally for a specific date"""
        try:
            if crawl_date:
                query = """
                    SELECT crawl_date, game_info 
                    FROM preorder_games 
                    WHERE region = %s AND crawl_date = %s
                """
                self.cursor.execute(query, (region, crawl_date))
            else:
                query = """
                    SELECT crawl_date, game_info 
                    FROM preorder_games 
                    WHERE region = %s 
                    ORDER BY crawl_date DESC
                """
                self.cursor.execute(query, (region,))
            
            results = self.cursor.fetchall()
            
            # Parse JSON and return structured data
            parsed_results = []
            for row in results:
                crawl_date, game_info_json = row
                try:
                    games = json.loads(game_info_json)
                    parsed_results.append({
                        'crawl_date': crawl_date,
                        'region': region,
                        'games': games
                    })
                except json.JSONDecodeError:
                    logging.error(f"Error parsing JSON for {region} on {crawl_date}")
                    continue
            
            return parsed_results
            
        except Error as e:
            logging.error(f"Error retrieving games for {region}: {e}")
            return []
    
    def get_latest_games(self, limit=10):
        """Get the most recent game data across all regions"""
        try:
            query = """
                SELECT crawl_date, region, game_info 
                FROM preorder_games 
                ORDER BY crawl_date DESC 
                LIMIT %s
            """
            self.cursor.execute(query, (limit,))
            results = self.cursor.fetchall()
            
            parsed_results = []
            for row in results:
                crawl_date, region, game_info_json = row
                try:
                    games = json.loads(game_info_json)
                    parsed_results.append({
                        'crawl_date': crawl_date,
                        'region': region,
                        'games': games
                    })
                except json.JSONDecodeError:
                    continue
            
            return parsed_results
            
        except Error as e:
            logging.error(f"Error retrieving latest games: {e}")
            return []
    
    def get_statistics(self):
        """Get database statistics"""
        try:
            stats = {}
            
            # Total records
            self.cursor.execute("SELECT COUNT(*) FROM preorder_games")
            stats['total_records'] = self.cursor.fetchone()[0]
            
            # Records by region
            self.cursor.execute("""
                SELECT region, COUNT(*) as count 
                FROM preorder_games 
                GROUP BY region 
                ORDER BY count DESC
            """)
            stats['by_region'] = dict(self.cursor.fetchall())
            
            # Date range
            self.cursor.execute("""
                SELECT MIN(crawl_date) as earliest, MAX(crawl_date) as latest 
                FROM preorder_games
            """)
            date_range = self.cursor.fetchone()
            stats['date_range'] = {
                'earliest': date_range[0],
                'latest': date_range[1]
            }
            
            # Total games across all records
            self.cursor.execute("SELECT game_info FROM preorder_games")
            total_games = 0
            for (game_info_json,) in self.cursor.fetchall():
                try:
                    games = json.loads(game_info_json)
                    total_games += len(games)
                except:
                    continue
            stats['total_games'] = total_games
            
            return stats
            
        except Error as e:
            logging.error(f"Error getting statistics: {e}")
            return {}
    
    def test_connection(self):
        """Test database connection"""
        try:
            if self.connect():
                self.cursor.execute("SELECT 1")
                result = self.cursor.fetchone()
                self.disconnect()
                return result is not None
            return False
        except Error as e:
            logging.error(f"Database connection test failed: {e}")
            return False 
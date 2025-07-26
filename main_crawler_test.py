import logging
import time
import re
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from bs4 import BeautifulSoup

from database_utils_test import DatabaseManagerTest
from config import CRAWLER_CONFIG, LOG_CONFIG, EMAIL_CONFIG
from remove_duplicate_country_codes import unique_codes

class PlayStationCrawler:
    def __init__(self):
        self.db_manager = DatabaseManagerTest()
        self.setup_logging()
        self.setup_driver()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=getattr(logging, LOG_CONFIG['level']),
            format=LOG_CONFIG['format'],
            handlers=[
                logging.FileHandler(LOG_CONFIG['filename']),
                logging.StreamHandler()
            ]
        )
        
    def setup_driver(self):
        """Setup Chrome WebDriver with optimized options using local ChromeDriver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-in-process-stack-traces")
        chrome_options.add_argument("--disable-webgl")
        chrome_options.add_argument("--disable-3d-apis")
        chrome_options.add_argument("--disable-accelerated-2d-canvas")
        chrome_options.add_argument("--disable-accelerated-jpeg-decoding")
        chrome_options.add_argument("--disable-accelerated-mjpeg-decode")
        chrome_options.add_argument("--disable-accelerated-video-decode")
        chrome_options.add_argument("--disable-gpu-sandbox")
        chrome_options.add_argument("--log-level=3")  # Suppress INFO, WARNING, ERROR logs
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Use local ChromeDriver instead of automated download
        import os
        
        # Path to local ChromeDriver
        chromedriver_path = os.path.join(os.path.dirname(__file__), "chromedriver-win64", "chromedriver.exe")
        
        if not os.path.exists(chromedriver_path):
            raise Exception(f"ChromeDriver not found at: {chromedriver_path}")
        
        logging.info(f"Using local ChromeDriver at: {chromedriver_path}")
        
        try:
            service = Service(chromedriver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(CRAWLER_CONFIG['implicit_wait'])
            
            # Test that driver works by accessing a simple page
            self.driver.get("https://www.google.com")
            # If we get here without exception, the driver is working
            logging.info("WebDriver setup successful!")
                
        except Exception as e:
            logging.error(f"WebDriver setup failed: {e}")
            if hasattr(self, 'driver'):
                try:
                    self.driver.quit()
                except:
                    pass
            raise
        
    def send_email_notification(self, is_success=True, message="", error_details=""):
        """Send email notification for crawler completion or failure"""
        if not EMAIL_CONFIG['enabled'] or not EMAIL_CONFIG['sender_password']:
            logging.warning("Email notifications not configured properly - skipping email")
            return False
            
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = EMAIL_CONFIG['sender_email']
            msg['To'] = EMAIL_CONFIG['recipient_email']
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if is_success:
                msg['Subject'] = EMAIL_CONFIG['subject_success']
                body = f"""
PlayStation Store Crawler completed successfully!

Run Time: {current_time}
Status: SUCCESS
Message: {message}

The daily crawl has finished and data has been stored in your MySQL database.
                """
            else:
                msg['Subject'] = EMAIL_CONFIG['subject_failure']
                body = f"""
PlayStation Store Crawler encountered an error!

Run Time: {current_time}
Status: FAILED
Message: {message}

Error Details:
{error_details}

Please check the crawler.log file for more detailed information.
                """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Setup SMTP server
            server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
            server.starttls()  # Enable encryption
            server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
            
            # Send email
            text = msg.as_string()
            server.sendmail(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['recipient_email'], text)
            server.quit()
            
            logging.info(f"Email notification sent successfully: {'SUCCESS' if is_success else 'FAILURE'}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send email notification: {e}")
            return False
        
    def get_games_from_page(self, region):
        """Extract all games from all pages for a given region"""
        all_games = []
        page_num = 1
        games_per_page = 24  # Standard PlayStation store page size
        
        while True:
            try:
                # Construct URL for pre-order category with page number
                url = f"https://store.playstation.com/{region}/category/3bf499d7-7acf-4931-97dd-2667494ee2c9/{page_num}"
                logging.info(f"Crawling {region} - Page {page_num}: {url}")
                
                # Navigate to page
                self.driver.get(url)
                time.sleep(CRAWLER_CONFIG['request_delay'])
                
                # Wait for game content to load - look for the product tiles
                try:
                    WebDriverWait(self.driver, CRAWLER_CONFIG['timeout']).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-qa*='productTile']"))
                    )
                except TimeoutException:
                    logging.warning(f"Timeout waiting for content on {url}")
                    # If no content on first page, this region might not have pre-orders
                    if page_num == 1:
                        logging.info(f"No pre-order content found for {region}")
                        return []
                    break
                
                # Get page source and parse with BeautifulSoup
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                
                # Find game elements using the actual structure from the HTML analysis
                # Look for divs with data-qa containing "productTile" and data-qa-index
                game_elements = soup.find_all('div', {'data-qa': re.compile(r'.*productTile\d+.*'), 'data-qa-index': True})
                
                if not game_elements:
                    logging.info(f"No games found on page {page_num} for {region}")
                    # If no games on first page, region might not have pre-orders
                    if page_num == 1:
                        logging.info(f"No pre-order games available for {region}")
                        return []
                    break
                
                logging.info(f"Found {len(game_elements)} games on page {page_num} for {region}")
                
                # Extract game information
                for game_element in game_elements:
                    try:
                        # Get the index from data-qa-index attribute (this is the position on the current page)
                        page_index = int(game_element.get('data-qa-index', 0))
                        
                        # Calculate absolute rank across all pages
                        display_rank = (page_num - 1) * games_per_page + page_index + 1
                        
                        # Extract product ID from data-telemetry-meta attribute instead of game name
                        game_name = ""
                        
                        try:
                            # Find the <a> tag within this game tile
                            link_element = game_element.find('a')
                            if link_element:
                                # Get the data-telemetry-meta attribute
                                telemetry_meta = link_element.get('data-telemetry-meta')
                                if telemetry_meta:
                                    # Parse the JSON string
                                    telemetry_data = json.loads(telemetry_meta)
                                    # Extract the "id" value
                                    game_name = telemetry_data.get('id', '')
                                    
                                    if game_name:
                                        logging.debug(f"Successfully extracted product ID: {game_name}")
                                    else:
                                        logging.warning(f"No 'id' found in telemetry data for element {page_index} on page {page_num}")
                                else:
                                    logging.warning(f"No data-telemetry-meta attribute found for element {page_index} on page {page_num}")
                            else:
                                logging.warning(f"No <a> tag found for element {page_index} on page {page_num}")
                                
                        except json.JSONDecodeError as e:
                            logging.warning(f"Failed to parse JSON from data-telemetry-meta for element {page_index} on page {page_num}: {e}")
                            game_name = ""
                        except AttributeError as e:
                            logging.warning(f"Attribute error extracting product ID for element {page_index} on page {page_num}: {e}")
                            game_name = ""
                        except Exception as e:
                            logging.warning(f"Unexpected error extracting product ID for element {page_index} on page {page_num}: {e}")
                            game_name = ""
                        
                        game_data = {
                            'region': region,
                            'game_name': game_name,
                            'display_rank': display_rank
                        }
                        
                        all_games.append(game_data)
                        logging.debug(f"Extracted: {game_name} (Rank: {display_rank})")
                        
                    except Exception as e:
                        logging.error(f"Error extracting game from {region} page {page_num}: {e}")
                        continue
                
                # Check for next page by looking at pagination or by checking if we got a full page
                # If we got fewer games than expected on this page, we're probably at the end
                if len(game_elements) < games_per_page:
                    logging.info(f"Reached last page for {region} at page {page_num} (only {len(game_elements)} games)")
                    break
                
                # Also check for actual pagination elements
                pagination_elements = soup.find_all(['button', 'a'], string=re.compile(r'\d+'))
                if pagination_elements:
                    # Look for a number higher than current page
                    max_page_found = page_num
                    for elem in pagination_elements:
                        try:
                            page_number = int(elem.get_text().strip())
                            if page_number > max_page_found:
                                max_page_found = page_number
                        except (ValueError, AttributeError):
                            continue
                    
                    if page_num >= max_page_found:
                        logging.info(f"Reached max pagination for {region} at page {page_num}")
                        break
                
                page_num += 1
                
                # Safety check - limit pages to prevent infinite loops
                if page_num > 50:  # Reasonable limit
                    logging.warning(f"Reached page limit for {region}")
                    break
                    
            except Exception as e:
                logging.error(f"Error crawling {region} page {page_num}: {e}")
                break
        
        logging.info(f"Total games found for {region}: {len(all_games)}")
        return all_games
    
    def crawl_region_with_retries(self, region, max_retries=None):
        """Crawl a region with retry logic"""
        if max_retries is None:
            max_retries = CRAWLER_CONFIG['max_retries']
            
        for attempt in range(max_retries):
            try:
                games = self.get_games_from_page(region)
                if games:
                    return games
                else:
                    logging.warning(f"No games found for {region} on attempt {attempt + 1}")
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed for {region}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)  # Wait before retry
        
        logging.error(f"Failed to crawl {region} after {max_retries} attempts")
        return []
    
    def run_crawler(self):
        """Main crawler execution"""
        logging.info("Starting PlayStation Store Crawler")
        start_time = datetime.now()
        
        # Test database connection
        if not self.db_manager.test_connection():
            error_msg = "Database connection failed. Exiting."
            logging.error(error_msg)
            self.send_email_notification(False, "Database connection failed", error_msg)
            return
        
        # Connect to database
        if not self.db_manager.connect():
            error_msg = "Failed to connect to database. Exiting."
            logging.error(error_msg)
            self.send_email_notification(False, "Database connection failed", error_msg)
            return
        
        total_games = 0
        successful_regions = 0
        failed_regions = []
        
        try:
            for region in unique_codes:
                logging.info(f"Starting crawl for region: {region}")
                
                try:
                    games = self.crawl_region_with_retries(region)
                    
                    if games:
                        # Insert games into database as JSON for this region
                        if self.db_manager.insert_games_for_region(region, games):
                            total_games += len(games)
                            successful_regions += 1
                            logging.info(f"Successfully processed {len(games)} games for {region}")
                        else:
                            logging.error(f"Failed to insert games for {region}")
                            failed_regions.append(region)
                    else:
                        logging.warning(f"No games found for {region}")
                        failed_regions.append(region)
                        
                except Exception as e:
                    error_msg = f"Unexpected error processing {region}: {e}"
                    logging.error(error_msg)
                    failed_regions.append(region)
                
                # Delay between regions
                time.sleep(CRAWLER_CONFIG['request_delay'])
                
        except KeyboardInterrupt:
            error_msg = "Crawler interrupted by user"
            logging.info(error_msg)
            self.send_email_notification(False, "Crawler interrupted", error_msg)
        except Exception as e:
            error_msg = f"Unexpected error in main crawler: {e}"
            logging.error(error_msg)
            self.send_email_notification(False, "Unexpected crawler error", error_msg)
        finally:
            # Cleanup
            self.db_manager.disconnect()
            if hasattr(self, 'driver'):
                self.driver.quit()
            
            # Calculate execution time
            end_time = datetime.now()
            execution_time = end_time - start_time
            
            # Final report
            logging.info(f"Crawler completed:")
            logging.info(f"  Total games crawled: {total_games}")
            logging.info(f"  Successful regions: {successful_regions}/{len(unique_codes)}")
            logging.info(f"  Failed regions: {len(failed_regions)}")
            logging.info(f"  Execution time: {execution_time}")
            
            # Send success/failure notification
            if failed_regions and len(failed_regions) == len(unique_codes):
                # Complete failure
                self.send_email_notification(False, 
                    "All regions failed to crawl", 
                    f"Failed regions: {failed_regions}")
            elif failed_regions:
                # Partial failure
                success_msg = f"Crawled {total_games} games from {successful_regions} regions. Some regions failed: {failed_regions}"
                self.send_email_notification(True, success_msg)
            else:
                # Complete success
                success_msg = f"Successfully crawled {total_games} games from {successful_regions} regions in {execution_time}"
                self.send_email_notification(True, success_msg)
            
            if failed_regions:
                logging.info(f"  Failed regions list: {failed_regions}")

def main():
    """Main entry point"""
    crawler = PlayStationCrawler()
    crawler.run_crawler()

if __name__ == "__main__":
    main() 
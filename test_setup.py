#!/usr/bin/env python3
"""
Test script to verify database connection and basic functionality
Run this before running the full crawler
"""

import sys
import logging
from database_utils import DatabaseManager
from remove_duplicate_country_codes import unique_codes

def test_database_connection():
    """Test database connection"""
    print("Testing database connection...")
    
    db_manager = DatabaseManager()
    
    if db_manager.test_connection():
        print("✓ Database connection successful!")
        return True
    else:
        print("✗ Database connection failed!")
        print("Please check your MySQL password in config.py")
        return False

def test_region_codes():
    """Test that region codes are available"""
    print(f"Testing region codes... Found {len(unique_codes)} regions")
    print("First 10 regions:", unique_codes[:10])
    return len(unique_codes) > 0

def test_sample_insertion():
    """Test inserting a sample game"""
    print("Testing sample data insertion...")
    
    db_manager = DatabaseManager()
    
    if not db_manager.connect():
        print("✗ Could not connect to database")
        return False
    
    try:
        # Insert a test game
        success = db_manager.insert_game(
            region="en-hk",
            game_name="Test Game",
            display_rank=1
        )
        
        if success:
            db_manager.connection.commit()
            print("✓ Sample insertion successful!")
            
            # Clean up test data
            db_manager.cursor.execute("DELETE FROM preorder_games WHERE region = 'en-hk' AND game_name = 'Test Game'")
            db_manager.connection.commit()
            print("✓ Test data cleaned up")
            
        else:
            print("✗ Sample insertion failed!")
            
        return success
        
    except Exception as e:
        print(f"✗ Error during sample insertion: {e}")
        return False
    finally:
        db_manager.disconnect()

def test_webdriver_setup():
    """Test WebDriver setup using local ChromeDriver"""
    print("Testing WebDriver setup...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        import os
        
        # Path to local ChromeDriver
        chromedriver_path = os.path.join(os.path.dirname(__file__), "chromedriver-win64", "chromedriver.exe")
        
        if not os.path.exists(chromedriver_path):
            print(f"✗ ChromeDriver not found at: {chromedriver_path}")
            print("  Please ensure chromedriver.exe is in the chromedriver-win64 directory")
            return False
        
        print(f"  Using local ChromeDriver at: {chromedriver_path}")
        
        # Setup Chrome options for headless test
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-in-process-stack-traces")
        
        # Test ChromeDriver
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Quick test to verify driver works
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        
        print(f"  Page title: '{title}'")
        # If we get here without exception, the driver is working
        print("✓ WebDriver setup successful!")
        return True
            
    except Exception as e:
        print(f"✗ WebDriver setup failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=== PlayStation Store Crawler Setup Test ===\n")
    
    tests = [
        # ("Database Connection", test_database_connection),
        # ("Region Codes", test_region_codes),
        ("Sample Data Insertion", test_sample_insertion),
        ("WebDriver Setup", test_webdriver_setup)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} passed\n")
            else:
                print(f"✗ {test_name} failed\n")
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}\n")
    
    print(f"=== Test Results: {passed}/{total} tests passed ===")
    
    if passed == total:
        print("✓ All tests passed! You can now run the main crawler.")
        print("To run the crawler: python main_crawler.py")
    else:
        print("✗ Some tests failed. Please fix the issues before running the crawler.")
        print("\nCommon issues:")
        print("1. Check MySQL password in config.py")
        print("2. Ensure MySQL server is running")
        print("3. Verify database 'playstation_crawler' exists")

if __name__ == "__main__":
    main() 
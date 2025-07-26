#!/usr/bin/env python3
"""
Test script to verify SQLite export functionality
"""

import os
import sqlite3
from export_to_sqlite import test_sqlite_file

def test_export_process():
    """
    Test the complete export process
    """
    print("🧪 Testing SQLite Export Process")
    print("=" * 50)
    
    # Check if export script exists
    if not os.path.exists("export_to_sqlite.py"):
        print("❌ export_to_sqlite.py not found")
        return False
    
    # Check if config exists
    if not os.path.exists("config.py"):
        print("❌ config.py not found")
        return False
    
    print("✅ Required files found")
    
    # Check if SQLite file exists on desktop
    desktop_path = os.path.expanduser("~/Desktop")
    sqlite_file = os.path.join(desktop_path, "preorderGames.db")
    
    if os.path.exists(sqlite_file):
        print(f"✅ SQLite file found: {sqlite_file}")
        
        # Test the file
        if test_sqlite_file():
            print("✅ SQLite file is working correctly")
            return True
        else:
            print("❌ SQLite file test failed")
            return False
    else:
        print(f"⚠️  SQLite file not found: {sqlite_file}")
        print("💡 Run 'python export_to_sqlite.py' to create the file")
        return False

def show_usage_instructions():
    """
    Show instructions for using the export
    """
    print("\n" + "=" * 60)
    print("📋 USAGE INSTRUCTIONS")
    print("=" * 60)
    
    print("1️⃣  Export your MySQL data to SQLite:")
    print("   python export_to_sqlite.py")
    
    print("\n2️⃣  Install SQLite tools (choose one):")
    print("   • DB Browser for SQLite (GUI): https://sqlitebrowser.org/dl/")
    print("   • SQLite command line tools: https://www.sqlite.org/download.html")
    print("   • VS Code extension: Search 'SQLite' in VS Code extensions")
    
    print("\n3️⃣  Open your database:")
    print("   • Navigate to your Desktop")
    print("   • Find 'preorderGames.db'")
    print("   • Open with your chosen SQLite tool")
    
    print("\n4️⃣  Share with your teammate:")
    print("   • Send the 'preorderGames.db' file to your teammate")
    print("   • They can open it with any SQLite browser")
    
    print("\n📖 For detailed installation instructions, see:")
    print("   SQLITE_INSTALLATION_GUIDE.md")

if __name__ == "__main__":
    print("🎮 PlayStation Store Crawler - SQLite Export Test")
    print("=" * 60)
    
    # Run the test
    success = test_export_process()
    
    if success:
        print("\n🎉 All tests passed! Your SQLite export is ready.")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
    
    # Show usage instructions
    show_usage_instructions() 
# PlayStation Store Crawler

A comprehensive Python crawler that extracts pre-order game information from PlayStation Store across all regions and stores the data in a MySQL database.

## Features

- ✅ **Multi-region support**: Crawls all valid PlayStation Store regions
- ✅ **Pagination handling**: Automatically navigates through all pages
- ✅ **Database storage**: Stores data in MySQL with date tracking
- ✅ **Error handling**: Robust retry logic and error recovery
- ✅ **Logging**: Comprehensive logging for monitoring
- ✅ **Daily tracking**: Supports daily crawling with historical data
- ✅ **Product ID extraction**: Extracts unique product identifiers for reliable data tracking

## Project Structure

```
PS Store Crawler/
├── main_crawler.py          # Main crawler script
├── database_utils.py        # Database operations
├── config.py               # Configuration settings
├── test_setup.py           # Setup verification script
├── check_ps_codes.py       # Region code validation (existing)
├── remove_duplicate_country_codes.py  # Code cleanup (existing)
├── export_database.py      # Database export script (requires mysqldump)
├── export_database_python.py # Pure Python export script (no mysqldump needed)
├── export_database.bat     # Windows batch file for export
├── export_database.ps1     # PowerShell script for export
├── test_export.py          # Export functionality test script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database Connection

Edit `config.py` and replace the MySQL password:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_ACTUAL_MYSQL_PASSWORD',  # Replace this!
    'database': 'playstation_crawler',
    'port': 3306
}
```

### 3. Verify Setup

Run the test script to ensure everything is working:

```bash
python test_setup.py
```

Expected output:
```
=== PlayStation Store Crawler Setup Test ===

Running Database Connection...
✓ Database connection successful!

Running Region Codes...
Testing region codes... Found 90 regions
✓ Region Codes passed

Running Sample Data Insertion...
✓ Sample insertion successful!
✓ Test data cleaned up
✓ Sample Data Insertion passed

=== Test Results: 3/3 tests passed ===
✓ All tests passed! You can now run the main crawler.
```

## Usage

### Run Full Crawler

```bash
python main_crawler.py
```

This will:
- Crawl all valid PlayStation Store regions
- Extract all pre-order games from each region
- Store data in MySQL with today's date
- Generate detailed logs in `crawler.log`

### View Results

Connect to MySQL and query the data:

```sql
-- View total games crawled today
SELECT COUNT(*) as total_games 
FROM preorder_games 
WHERE crawl_date = CURDATE();

-- View games by region
SELECT region, COUNT(*) as game_count 
FROM preorder_games 
WHERE crawl_date = CURDATE() 
GROUP BY region 
ORDER BY game_count DESC;

-- View top 10 games (by rank) for a specific region
SELECT game_name, rank 
FROM preorder_games 
WHERE region = 'en-us' AND crawl_date = CURDATE() 
ORDER BY rank 
LIMIT 10;
-- Note: game_name field contains product IDs, not human-readable game names
```

## Database Schema

The crawler stores data in the `preorder_games` table:

| Column      | Type        | Description                           |
|-------------|-------------|---------------------------------------|
| id          | INT         | Auto-increment primary key            |
| crawl_date  | DATE        | Date when the data was crawled        |
| region      | VARCHAR(10) | Region code (e.g., 'en-us', 'ja-jp') |
| game_name   | TEXT        | Product ID of the game (unique identifier) |
| rank        | INT         | Display order/rank on the website     |

## Configuration Options

### Crawler Settings (`config.py`)

```python
CRAWLER_CONFIG = {
    'base_url': 'https://store.playstation.com/{}/category/3bf499d7-7acf-4931-97dd-2667494ee2c9',
    'request_delay': 2,      # Seconds between requests
    'max_retries': 3,        # Retry attempts per region
    'timeout': 30,           # Page load timeout
    'implicit_wait': 10      # Selenium implicit wait
}
```

## Troubleshooting

### Common Issues

1. **"Database connection failed"**
   - Check MySQL server is running
   - Verify password in `config.py`
   - Ensure `playstation_crawler` database exists

2. **"ChromeDriver not found"**
   - The script auto-downloads ChromeDriver
   - Ensure you have Chrome browser installed

3. **"No games found"**
   - Check if PlayStation Store structure changed
   - Verify region codes are still valid
   - Check logs for detailed error messages

### Log Files

- `crawler.log`: Detailed execution logs
- Console output: Real-time progress updates

## Database Export

To share your database with teammates, use the export functionality:

### Quick Export (Windows)
```bash
# Double-click or run:
export_database.bat

# Or use PowerShell:
.\export_database.ps1
```

### Command Line Export

#### Method 1: Standard Export (requires mysqldump)
```bash
# Export full database with data
python export_database.py

# Export only database structure (no data)
python export_database.py --schema-only

# Show help
python export_database.py --help
```

#### Method 2: Pure Python Export (no mysqldump required)
```bash
# Export full database with data
python export_database_python.py

# Export only database structure (no data)
python export_database_python.py --schema-only

# Show help
python export_database_python.py --help
```

### Test Export Functionality
```bash
# Test if export will work on your system
python test_export.py
```

### What Gets Exported
- Complete database structure (tables, indexes, constraints)
- All data from the `preorder_games` table
- Import instructions for teammates
- Timestamped files in the `Export/` folder

### Export Methods Comparison
| Method | Requirements | Pros | Cons |
|--------|-------------|------|------|
| Standard (`export_database.py`) | mysqldump in PATH | Faster, more efficient | Requires MySQL tools |
| Python (`export_database_python.py`) | Only Python + MySQL connector | No additional tools needed | Slower for large datasets |

### Sharing with Teammates
1. Run the export script (automatically chooses best method)
2. Share the generated `.sql` file from the `Export/` folder
3. Teammates can import using the provided instructions

## Daily Automation

To run daily, you can:

1. **Windows Task Scheduler**:
   - Create a basic task
   - Set trigger to daily
   - Action: Start program `python` with arguments `main_crawler.py`

2. **Cron Job (Linux/Mac)**:
   ```bash
   # Run daily at 2 AM
   0 2 * * * cd /path/to/crawler && python main_crawler.py
   ```

## Data Analysis Examples

### Track Game Popularity Over Time

```sql
-- See how many games each region has over time
SELECT crawl_date, region, COUNT(*) as game_count
FROM preorder_games 
WHERE crawl_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
GROUP BY crawl_date, region
ORDER BY crawl_date DESC, game_count DESC;
```

### Find New Games

```sql
-- Find games that appeared today but weren't there yesterday
SELECT DISTINCT p1.game_name, p1.region
FROM preorder_games p1
WHERE p1.crawl_date = CURDATE()
AND NOT EXISTS (
    SELECT 1 FROM preorder_games p2 
    WHERE p2.game_name = p1.game_name 
    AND p2.region = p1.region 
    AND p2.crawl_date = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
);
```

## Support

For issues or questions:
1. Check the log files for detailed error messages
2. Run `test_setup.py` to verify configuration
3. Ensure all dependencies are installed correctly

## Notes

- The crawler runs in headless mode (no browser window)
- Respects PlayStation Store with delays between requests
- Stores complete historical data for trend analysis
- Handles region-specific pagination automatically 
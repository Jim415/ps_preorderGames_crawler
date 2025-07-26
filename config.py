# Configuration file for PlayStation Store Crawler

# Database Configuration Mode
# Set to 'local' for local MySQL or 'cloud' for cloud database
DB_MODE = 'local'  # Change to 'cloud' after migration

# Local MySQL Database Configuration
LOCAL_DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Zh1149191843!',  # Replace with your actual password
    'database': 'playstation_crawler',
    'port': 3306
}

# Cloud Database Configuration
# Update with your cloud database credentials after migration
CLOUD_DB_CONFIG = {
    'host': 'your-cloud-host.com',        # Replace with your cloud host
    'user': 'your_cloud_username',        # Replace with your cloud username
    'password': 'your_cloud_password',    # Replace with your cloud password
    'database': 'playstation_crawler',    # Your cloud database name
    'port': 3306,
    'ssl_disabled': False,
    'ssl_ca': None,
    'autocommit': True
}

# Get active database configuration based on mode
def get_db_config():
    """Get the active database configuration based on DB_MODE"""
    if DB_MODE == 'cloud':
        return CLOUD_DB_CONFIG
    else:
        return LOCAL_DB_CONFIG

# For backward compatibility
DB_CONFIG = get_db_config()

# Crawler Configuration
CRAWLER_CONFIG = {
    'request_delay': 2,  # seconds between requests
    'max_retries': 3,
    'timeout': 30,
    'implicit_wait': 10
}

# Logging Configuration
LOG_CONFIG = {
    'filename': 'crawler.log',
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s'
}

# Email Configuration for Notifications
EMAIL_CONFIG = {
    'enabled': True,
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'zhanghan415@gmail.com',  # Your Gmail address
    'sender_password': 'lvvv ipnh jooz xjjl',  # You'll need to set this with your Gmail App Password
    'recipient_email': 'zhanghan415@gmail.com',
    'subject_success': 'PlayStation Crawler - Daily Run Completed',
    'subject_failure': 'PlayStation Crawler - Daily Run Failed'
} 
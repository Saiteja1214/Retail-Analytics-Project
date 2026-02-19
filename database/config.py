"""Database configuration settings."""

# MySQL Database Configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',  # Change this to your actual password
    'database': 'RetailDW'
}

# Data paths
DATA_CLEANED_PATH = "data/cleaned_retail.csv"

# Batch size for inserts
BATCH_SIZE = 1000

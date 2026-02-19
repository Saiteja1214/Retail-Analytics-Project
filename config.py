"""Global configuration for retail analytics project."""

import os

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
RESULTS_DIR = os.path.join(PROJECT_ROOT, 'results')

# Data files
RAW_DATA_PATH = os.path.join(DATA_DIR, 'Online Retail.csv')
CLEANED_DATA_PATH = os.path.join(DATA_DIR, 'cleaned_retail.csv')

# Create results directory if not exists
os.makedirs(RESULTS_DIR, exist_ok=True)

# Analysis parameters
REGRESSION_TEST_SIZE = 0.2
CLASSIFICATION_THRESHOLD = 5000
CLUSTERING_N_CLUSTERS = 3
MIN_SUPPORT = 0.02  # For association rules
MIN_LIFT = 1.0  # For association rules

# Random state for reproducibility
RANDOM_STATE = 42

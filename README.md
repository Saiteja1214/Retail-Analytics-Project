# Retail Analytics Project

A comprehensive retail data analysis project with modular architecture for data cleaning, statistical analysis, machine learning, and database integration.

## Project Structure

```
Retail_Analytics_Project/
├── data/
│   ├── Online Retail.csv          # Raw data (optional)
│   └── cleaned_retail.csv          # Cleaned data
├── database/
│   ├── __init__.py
│   ├── config.py                   # Database configuration
│   └── load_to_mysql.py            # Load data to MySQL
├── scripts/
│   ├── __init__.py
│   └── data_cleaning.py            # Data cleaning module
├── analysis/
│   ├── __init__.py
│   ├── regression.py               # Linear regression analysis
│   ├── classification.py           # Customer classification
│   ├── association_rules.py        # Market basket analysis
│   └── clustering.py               # Customer segmentation
├── utils/
│   ├── __init__.py
│   └── helpers.py                  # Utility functions
├── config.py                       # Project configuration
├── retail_analysis.py              # Main entry point
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Installation

1. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Run Complete Analysis
```bash
python retail_analysis.py --analyze
```

### Load Data to MySQL Database
```bash
python retail_analysis.py --load-db
```

### Run All Tasks (Analysis + Database Load)
```bash
python retail_analysis.py --all
```

## Modules

### Data Cleaning (`scripts/data_cleaning.py`)
- Loads data from Excel or CSV
- Removes missing values and invalid records
- Calculates derived fields (Total_Amount)
- Generates statistical summaries

### Regression Analysis (`analysis/regression.py`)
- Predicts total sales amount from quantity and price
- Uses Linear Regression model
- Provides R², MSE, RMSE, and MAE metrics

### Classification Analysis (`analysis/classification.py`)
- Identifies high-value customers (>$5000 spending)
- Uses Decision Tree classifier
- Reports accuracy, precision, recall, and F1-score

### Association Rules (`analysis/association_rules.py`)
- Market basket analysis using Apriori algorithm
- Finds frequently purchased product combinations
- Generates association rules with support, confidence, and lift metrics

### Clustering Analysis (`analysis/clustering.py`)
- Customer segmentation using K-means
- Analyzes cluster characteristics
- Provides silhouette score evaluation

### Database Module (`database/load_to_mysql.py`)
- Loads cleaned data into MySQL data warehouse
- Creates dimension tables (Time, Customer, Product)
- Loads fact table (Sales)
- Handles duplicate key errors gracefully

## Configuration

Edit `config.py` to adjust:
- Data file paths
- Analysis parameters (thresholds, cluster count, etc.)
- Random state for reproducibility

Edit `database/config.py` for MySQL connection details:
```python
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your password',
    'database': 'RetailDW'
}
```

## Data Requirements

The project expects retail transaction data with columns:
- `Invoice`: Transaction ID
- `InvoiceDate`: Date of transaction
- `Customer ID`: Unique customer identifier
- `StockCode`: Product code
- `Description`: Product description
- `Quantity`: Quantity purchased
- `Price`: Unit price

## Database Schema

### Time_Dim
- Time_ID (Primary Key)
- InvoiceDate
- Year, Month, Day

### Customer_Dim
- Customer_ID (Primary Key)
- Country

### Product_Dim
- StockCode (Primary Key)
- Description
- Price

### Sales_Fact
- Sales_ID (Primary Key)
- Invoice, Customer_ID, StockCode, Time_ID
- Quantity, Total_Amount

## Dependencies

- **pandas**: Data manipulation
- **numpy**: Numerical operations
- **matplotlib**: Visualization
- **seaborn**: Statistical visualization
- **scikit-learn**: Machine learning
- **mlxtend**: Association rules (Apriori)
- **mysql-connector-python**: MySQL connectivity
- **openpyxl**: Excel file support

## Example Output

```
============================================================
RETAIL ANALYTICS PROJECT
============================================================

[1/5] DATA CLEANING
--- Data Cleaning ---
✓ Removed 10 rows with missing Customer IDs
✓ Removed 5 rows with negative quantities
✓ Loaded 5000 records

[2/5] REGRESSION ANALYSIS
=== LINEAR REGRESSION ANALYSIS ===
R² Score: 0.9234
Mean Absolute Error (MAE): $12.45

[3/5] CLASSIFICATION ANALYSIS
=== CUSTOMER CLASSIFICATION ANALYSIS ===
Accuracy: 0.8765
Precision: 0.8542

[4/5] ASSOCIATION RULE MINING
=== ASSOCIATION RULE MINING ===
Found 42 association rules

[5/5] CLUSTERING ANALYSIS
=== CUSTOMER SEGMENTATION ===
Silhouette Score: 0.5678

============================================================
ANALYSIS COMPLETE
============================================================
```

## Notes

- All models use `random_state=42` for reproducibility
- Data is automatically scaled before clustering
- Database loading includes duplicate key error handling
- Use Agg backend for matplotlib in headless environments

## License

This project is provided as-is for educational and analytical purposes.

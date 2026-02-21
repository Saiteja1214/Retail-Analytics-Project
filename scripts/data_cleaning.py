"""
Data cleaning and preprocessing module.
Handles loading, cleaning, and saving retail data.
"""

import pandas as pd
import os


class DataCleaner:
    """Cleans and prepares retail data for analysis."""
    
    def __init__(self, excel_path=None, csv_path="data/cleaned_retail.csv"):
        """Initialize data cleaner with data paths."""
        self.excel_path = excel_path
        self.csv_path = csv_path
        self.df = None
    
    def load_data(self):
        """Load data from Excel or CSV."""
        if self.excel_path and os.path.exists(self.excel_path):
            print(f"Loading data from Excel: {self.excel_path}")
            self.df = pd.read_excel(self.excel_path)
        else:
            print(f"Loading data from CSV: {self.csv_path}")
            self.df = pd.read_csv(self.csv_path)
        
        print(f"[OK] Loaded {len(self.df)} records")
        return self.df
    
    def explore_data(self):
        """Explore data structure and quality."""
        print("\n--- Data Exploration ---")
        print("\nFirst few rows:")
        print(self.df.head())
        
        print("\nData Info:")
        print(self.df.info())
        
        print("\nMissing Values:")
        print(self.df.isnull().sum())
        
        print("\nBasic Statistics:")
        print(self.df.describe())
    
    def clean_data(self):
        """Clean and preprocess data."""
        print("\n--- Data Cleaning ---")
        
        # Remove rows with missing Customer IDs
        initial_count = len(self.df)
        self.df = self.df.dropna(subset=['Customer ID'])
        print(f"[OK] Removed {initial_count - len(self.df)} rows with missing Customer IDs")
        
        # Remove negative quantities
        initial_count = len(self.df)
        self.df = self.df[self.df['Quantity'] > 0]
        print(f"[OK] Removed {initial_count - len(self.df)} rows with negative quantities")
        
        # Convert InvoiceDate to datetime
        self.df['InvoiceDate'] = pd.to_datetime(self.df['InvoiceDate'], format='%d-%m-%Y %H:%M')
        print("[OK] Converted InvoiceDate to datetime")
        
        # Calculate total amount if not exists
        if 'Total_Amount' not in self.df.columns:
            self.df['Total_Amount'] = self.df['Quantity'] * self.df['Price']
            print("[OK] Calculated Total_Amount column")
        
        return self.df
    
    def save_cleaned_data(self):
        """Save cleaned data to CSV."""
        os.makedirs(os.path.dirname(self.csv_path) or '.', exist_ok=True)
        self.df.to_csv(self.csv_path, index=False)
        print(f"[OK] Saved cleaned data to {self.csv_path}")
    
    def get_statistics(self):
        """Generate statistical summary."""
        print("\n--- Statistical Summary ---")
        print(self.df.describe())
        print(f"\nMean Sales: ${self.df['Total_Amount'].mean():.2f}")
        print(f"Median Sales: ${self.df['Total_Amount'].median():.2f}")
        print(f"Variance: {self.df['Total_Amount'].var():.2f}")
        print(f"Std Dev: ${self.df['Total_Amount'].std():.2f}")
    
    def process(self):
        """Run complete data processing pipeline."""
        self.load_data()
        self.explore_data()
        self.clean_data()
        self.get_statistics()
        self.save_cleaned_data()
        return self.df


if __name__ == "__main__":
    cleaner = DataCleaner()
    cleaner.process()

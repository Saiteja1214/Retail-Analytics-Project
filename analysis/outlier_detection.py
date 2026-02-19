"""
Outlier Detection Analysis.
Identifies outliers using Z-score, IQR, and Isolation Forest methods.
Analyzes what outliers represent in retail context.
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.ensemble import IsolationForest
import os


class OutlierDetectionAnalysis:
    """Detects and analyzes outliers in retail data."""
    
    def __init__(self, df, column='Total_Amount'):
        """Initialize with dataframe and target column."""
        self.df = df
        self.column = column
        self.outliers = {}
        self.results = {}
    
    def zscore_outliers(self, threshold=3):
        """Detect outliers using Z-score method."""
        print(f"Detecting outliers using Z-score (threshold={threshold})...")
        
        z_scores = np.abs(stats.zscore(self.df[self.column]))
        outlier_mask = z_scores > threshold
        outlier_indices = np.where(outlier_mask)[0]
        
        outlier_data = self.df[outlier_mask]
        
        stats_result = {
            'Method': 'Z-Score',
            'Threshold': threshold,
            'Count': len(outlier_data),
            'Percentage': (len(outlier_data) / len(self.df)) * 100,
            'Min Value': outlier_data[self.column].min(),
            'Max Value': outlier_data[self.column].max(),
            'Mean': outlier_data[self.column].mean(),
            'Indices': outlier_indices
        }
        
        self.outliers['Z-Score'] = outlier_data
        self.results['Z-Score'] = stats_result
        
        print(f"[OK] Found {stats_result['Count']} outliers ({stats_result['Percentage']:.2f}%)")
        print(f"     Range: ${stats_result['Min Value']:.2f} - ${stats_result['Max Value']:.2f}\n")
        
        return stats_result
    
    def iqr_outliers(self, multiplier=1.5):
        """Detect outliers using Interquartile Range (IQR) method."""
        print(f"Detecting outliers using IQR (multiplier={multiplier})...")
        
        Q1 = self.df[self.column].quantile(0.25)
        Q3 = self.df[self.column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        
        outlier_mask = (self.df[self.column] < lower_bound) | (self.df[self.column] > upper_bound)
        outlier_indices = np.where(outlier_mask)[0]
        outlier_data = self.df[outlier_mask]
        
        stats_result = {
            'Method': 'IQR',
            'Q1': Q1,
            'Q3': Q3,
            'IQR': IQR,
            'Lower Bound': lower_bound,
            'Upper Bound': upper_bound,
            'Count': len(outlier_data),
            'Percentage': (len(outlier_data) / len(self.df)) * 100,
            'Min Value': outlier_data[self.column].min(),
            'Max Value': outlier_data[self.column].max(),
            'Mean': outlier_data[self.column].mean(),
            'Indices': outlier_indices
        }
        
        self.outliers['IQR'] = outlier_data
        self.results['IQR'] = stats_result
        
        print(f"[OK] Found {stats_result['Count']} outliers ({stats_result['Percentage']:.2f}%)")
        print(f"     Range: ${stats_result['Min Value']:.2f} - ${stats_result['Max Value']:.2f}\n")
        
        return stats_result
    
    def isolation_forest_outliers(self, contamination=0.05):
        """Detect outliers using Isolation Forest method."""
        print(f"Detecting outliers using Isolation Forest (contamination={contamination})...")
        
        # Select numerical features
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        X = self.df[numerical_cols].fillna(0)
        
        iso_forest = IsolationForest(contamination=contamination, random_state=42)
        predictions = iso_forest.fit_predict(X)
        outlier_mask = predictions == -1
        outlier_indices = np.where(outlier_mask)[0]
        outlier_data = self.df[outlier_mask]
        
        stats_result = {
            'Method': 'Isolation Forest',
            'Contamination': contamination,
            'Count': len(outlier_data),
            'Percentage': (len(outlier_data) / len(self.df)) * 100,
            'Min Value': outlier_data[self.column].min(),
            'Max Value': outlier_data[self.column].max(),
            'Mean': outlier_data[self.column].mean(),
            'Indices': outlier_indices
        }
        
        self.outliers['Isolation Forest'] = outlier_data
        self.results['Isolation Forest'] = stats_result
        
        print(f"[OK] Found {stats_result['Count']} outliers ({stats_result['Percentage']:.2f}%)")
        print(f"     Range: ${stats_result['Min Value']:.2f} - ${stats_result['Max Value']:.2f}\n")
        
        return stats_result
    
    def analyze_outlier_characteristics(self):
        """Analyze what outliers represent."""
        print("="*70)
        print("OUTLIER INTERPRETATION (Business Context)")
        print("="*70)
        
        print("\n1. BULK PURCHASES (High Quantity Outliers)")
        print("-"*70)
        high_qty = self.df[self.df['Quantity'] > self.df['Quantity'].quantile(0.95)]
        print(f"   Count: {len(high_qty)}")
        print(f"   Avg Quantity: {high_qty['Quantity'].mean():.0f} units")
        print(f"   Avg Amount: ${high_qty['Total_Amount'].mean():.2f}")
        print(f"   Typical Use: Bulk orders from retailers/wholesalers")
        
        print("\n2. HIGH-VALUE TRANSACTIONS")
        print("-"*70)
        high_val = self.df[self.df['Total_Amount'] > self.df['Total_Amount'].quantile(0.95)]
        print(f"   Count: {len(high_val)}")
        print(f"   Avg Amount: ${high_val['Total_Amount'].mean():.2f}")
        print(f"   Avg Quantity: {high_val['Quantity'].mean():.0f} units")
        print(f"   Typical Use: Premium orders or corporate purchases")
        
        print("\n3. POTENTIAL DATA ERRORS OR FRAUD")
        print("-"*70)
        # Zero or near-zero amounts
        zero_amount = self.df[self.df['Total_Amount'] == 0]
        print(f"   Zero Amount Transactions: {len(zero_amount)}")
        if len(zero_amount) > 0:
            print(f"   These could be: Cancelled orders, returns, free samples")
        
        # Negative prices (should not exist)
        neg_price = self.df[self.df['Price'] < 0]
        print(f"   Negative Prices: {len(neg_price)}")
        if len(neg_price) > 0:
            print(f"   These represent: Returns/refunds")
        
        print("\n4. SEASONAL/PROMOTIONAL SPIKES")
        print("-"*70)
        df_copy = self.df.copy()
        df_copy['InvoiceDate'] = pd.to_datetime(df_copy['InvoiceDate'])
        monthly = df_copy.groupby(df_copy['InvoiceDate'].dt.to_period('M'))['Total_Amount'].mean()
        high_months = monthly[monthly > monthly.mean() + monthly.std()]
        print(f"   High Activity Months: {len(high_months)}")
        if len(high_months) > 0:
            print(f"   Typical Use: Seasonal promotions or holidays")
    
    def print_outlier_summary(self, method):
        """Print summary for a detection method."""
        result = self.results[method]
        outlier_data = self.outliers[method]
        
        print(f"\n{method.upper()} METHOD SUMMARY")
        print("-"*70)
        
        if method == 'Z-Score':
            print(f"Threshold: {result['Threshold']} standard deviations")
        elif method == 'IQR':
            print(f"Q1: ${result['Q1']:.2f}, Q3: ${result['Q3']:.2f}")
            print(f"IQR: ${result['IQR']:.2f}")
            print(f"Bounds: ${result['Lower Bound']:.2f} - ${result['Upper Bound']:.2f}")
        else:
            print(f"Contamination: {result['Contamination']*100:.1f}%")
        
        print(f"\nOutliers Found: {result['Count']} ({result['Percentage']:.2f}% of data)")
        print(f"Value Range: ${result['Min Value']:.2f} - ${result['Max Value']:.2f}")
        print(f"Mean Value: ${result['Mean']:.2f}")
        
        # Show sample outliers
        print(f"\nSample Outliers (first 5):")
        sample = outlier_data[[self.column, 'Quantity', 'Description']].head(5)
        for idx, (_, row) in enumerate(sample.iterrows(), 1):
            print(f"  {idx}. Amount: ${row[self.column]:.2f}, Qty: {row['Quantity']}, "
                  f"Product: {row['Description'][:40]}")
    
    def run_analysis(self):
        """Run complete outlier detection analysis."""
        print("\n" + "="*70)
        print("OUTLIER DETECTION ANALYSIS")
        print(f"Target Column: {self.column}")
        print("="*70)
        print()
        
        # Run all detection methods
        self.zscore_outliers()
        self.iqr_outliers()
        self.isolation_forest_outliers()
        
        # Print summaries
        for method in self.results.keys():
            self.print_outlier_summary(method)
        
        # Analyze characteristics
        self.analyze_outlier_characteristics()
        
        print("\n" + "="*70)
        print("[SUCCESS] Outlier detection analysis complete!")
        print("="*70)
        
        return self.results


if __name__ == "__main__":
    df = pd.read_csv("data/cleaned_retail.csv")
    analyzer = OutlierDetectionAnalysis(df, column='Total_Amount')
    analyzer.run_analysis()

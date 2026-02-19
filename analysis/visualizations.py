"""Visualization module for retail analytics."""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class AnalysisVisualizer:
    """Creates visualizations for retail analysis."""
    
    def __init__(self, output_dir="results"):
        """Initialize with output directory."""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def plot_sales_distribution(self, df):
        """Plot sales amount distribution."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histogram
        axes[0].hist(df['Total_Amount'], bins=50, color='skyblue', edgecolor='black')
        axes[0].set_xlabel('Total Amount ($)')
        axes[0].set_ylabel('Frequency')
        axes[0].set_title('Distribution of Sales Amount')
        axes[0].grid(True, alpha=0.3)
        
        # Box plot
        axes[1].boxplot(df['Total_Amount'], vert=True)
        axes[1].set_ylabel('Total Amount ($)')
        axes[1].set_title('Sales Amount - Box Plot')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'sales_distribution.png'), dpi=100)
        plt.close()
        print("[OK] Saved: sales_distribution.png")
    
    def plot_top_products(self, df, top_n=10):
        """Plot top N products by revenue."""
        top_products = df.groupby('Description')['Total_Amount'].sum().nlargest(top_n)
        
        plt.figure(figsize=(12, 6))
        top_products.plot(kind='barh', color='steelblue')
        plt.xlabel('Revenue ($)')
        plt.ylabel('Product')
        plt.title(f'Top {top_n} Products by Revenue')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'top_products.png'), dpi=100)
        plt.close()
        print("[OK] Saved: top_products.png")
    
    def plot_top_countries(self, df, top_n=10):
        """Plot top N countries by revenue."""
        top_countries = df.groupby('Country')['Total_Amount'].sum().nlargest(top_n)
        
        plt.figure(figsize=(12, 6))
        top_countries.plot(kind='bar', color='coral')
        plt.xlabel('Country')
        plt.ylabel('Revenue ($)')
        plt.title(f'Top {top_n} Countries by Revenue')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'top_countries.png'), dpi=100)
        plt.close()
        print("[OK] Saved: top_countries.png")
    
    def plot_monthly_revenue(self, df):
        """Plot monthly revenue trend."""
        df_copy = df.copy()
        df_copy['InvoiceDate'] = pd.to_datetime(df_copy['InvoiceDate'])
        monthly = df_copy.groupby(df_copy['InvoiceDate'].dt.to_period('M'))['Total_Amount'].sum()
        
        plt.figure(figsize=(14, 6))
        monthly.plot(kind='line', marker='o', color='green', linewidth=2)
        plt.xlabel('Month')
        plt.ylabel('Revenue ($)')
        plt.title('Monthly Revenue Trend')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'monthly_revenue.png'), dpi=100)
        plt.close()
        print("[OK] Saved: monthly_revenue.png")
    
    def plot_customer_value_distribution(self, df):
        """Plot customer value distribution."""
        customer_value = df.groupby('Customer ID')['Total_Amount'].sum()
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histogram
        axes[0].hist(customer_value, bins=50, color='mediumpurple', edgecolor='black')
        axes[0].set_xlabel('Customer Total Spending ($)')
        axes[0].set_ylabel('Number of Customers')
        axes[0].set_title('Customer Value Distribution')
        axes[0].grid(True, alpha=0.3)
        
        # Pareto curve
        sorted_values = sorted(customer_value, reverse=True)
        cumsum = pd.Series(sorted_values).cumsum()
        cumsum_pct = (cumsum / cumsum.iloc[-1]) * 100
        
        axes[1].plot(range(len(cumsum_pct)), cumsum_pct, marker='o', markersize=3, color='darkred')
        axes[1].axhline(y=80, color='r', linestyle='--', alpha=0.5, label='80% threshold')
        axes[1].set_xlabel('Customer Rank')
        axes[1].set_ylabel('Cumulative Revenue %')
        axes[1].set_title('Pareto Curve - Customer Value')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'customer_value_distribution.png'), dpi=100)
        plt.close()
        print("[OK] Saved: customer_value_distribution.png")
    
    def plot_quantity_price_correlation(self, df):
        """Plot relationship between quantity and price."""
        plt.figure(figsize=(10, 6))
        plt.scatter(df['Quantity'], df['Price'], alpha=0.5, s=10)
        plt.xlabel('Quantity')
        plt.ylabel('Price ($)')
        plt.title('Quantity vs Price Correlation')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'quantity_price_correlation.png'), dpi=100)
        plt.close()
        print("[OK] Saved: quantity_price_correlation.png")
    
    def generate_all_visualizations(self, df):
        """Generate all visualizations."""
        print("\n=== GENERATING VISUALIZATIONS ===")
        self.plot_sales_distribution(df)
        self.plot_top_products(df)
        self.plot_top_countries(df)
        self.plot_monthly_revenue(df)
        self.plot_customer_value_distribution(df)
        self.plot_quantity_price_correlation(df)
        print("[SUCCESS] All visualizations saved to 'results' folder!")


if __name__ == "__main__":
    df = pd.read_csv("data/cleaned_retail.csv")
    visualizer = AnalysisVisualizer()
    visualizer.generate_all_visualizations(df)

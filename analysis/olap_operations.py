"""
OLAP (Online Analytical Processing) Operations.
Simulates multidimensional analysis using Roll-up, Drill-down, Slice, and Dice operations.
"""

import pandas as pd
import numpy as np


class OLAPAnalysis:
    """Performs OLAP operations on retail data."""
    
    def __init__(self, df):
        """Initialize with dataframe."""
        self.df = df.copy()
        self.df['InvoiceDate'] = pd.to_datetime(self.df['InvoiceDate'])
    
    def rollup_operation(self):
        """
        Roll-up: Aggregate data to a higher level of hierarchy.
        Monthly -> Yearly revenue aggregation.
        """
        print("\n" + "="*70)
        print("1. ROLL-UP OPERATION: Monthly -> Yearly Revenue")
        print("="*70)
        print("\nOperations aggregates detailed data to higher hierarchy level.")
        print("Example: Going from monthly to yearly view (decreasing granularity)")
        
        # Monthly aggregation
        monthly_revenue = self.df.groupby(
            self.df['InvoiceDate'].dt.to_period('M')
        ).agg({
            'Total_Amount': ['sum', 'mean', 'count'],
            'Quantity': 'sum',
            'Customer ID': 'nunique'
        }).round(2)
        
        monthly_revenue.columns = ['Total_Revenue', 'Avg_Transaction', 'Transactions', 'Total_Qty', 'Unique_Customers']
        
        print("\nMONTHLY SUMMARY (First 5 months):")
        print(monthly_revenue.head())
        
        # Yearly aggregation (roll-up from monthly)
        yearly_revenue = self.df.groupby(
            self.df['InvoiceDate'].dt.to_period('Y')
        ).agg({
            'Total_Amount': ['sum', 'mean', 'count'],
            'Quantity': 'sum',
            'Customer ID': 'nunique'
        }).round(2)
        
        yearly_revenue.columns = ['Total_Revenue', 'Avg_Transaction', 'Transactions', 'Total_Qty', 'Unique_Customers']
        
        print("\nYEARLY SUMMARY (After Roll-up):")
        print(yearly_revenue)
        
        print("\nRoll-up Explanation:")
        print("  - Aggregates monthly data -> yearly data")
        print("  - Reduces granularity from months to years")
        print("  - Useful for: Strategic planning, annual reports")
        
        return monthly_revenue, yearly_revenue
    
    def drilldown_operation(self):
        """
        Drill-down: Decompose data to a lower level of hierarchy.
        Yearly -> Monthly -> Daily revenue breakdown.
        """
        print("\n" + "="*70)
        print("2. DRILL-DOWN OPERATION: Yearly -> Monthly -> Daily Revenue")
        print("="*70)
        print("\nDecomposes aggregated data to lower hierarchy level.")
        print("Example: Breaking yearly into monthly, then into daily details")
        
        # Yearly level
        yearly = self.df.groupby(
            self.df['InvoiceDate'].dt.to_period('Y')
        )['Total_Amount'].agg(['sum', 'mean', 'count']).round(2)
        
        print("\nYEARLY LEVEL:")
        print(yearly)
        print(f"Total Revenue (Yearly): ${yearly['sum'].values[0]:,.2f}")
        
        # Drill-down to Monthly
        monthly = self.df.groupby(
            self.df['InvoiceDate'].dt.to_period('M')
        )['Total_Amount'].agg(['sum', 'mean', 'count']).round(2)
        
        print("\nDRILL-DOWN to MONTHLY LEVEL (First 6 months):")
        print(monthly.head(6))
        
        # Drill-down further to Daily
        daily = self.df.groupby(
            self.df['InvoiceDate'].dt.date
        )['Total_Amount'].agg(['sum', 'mean', 'count']).round(2)
        
        print("\nDRILL-DOWN to DAILY LEVEL (First 10 days):")
        print(daily.head(10))
        
        print("\nDrill-down Explanation:")
        print("  - Decomposes yearly data -> monthly data -> daily data")
        print("  - Increases granularity/detail level")
        print("  - Useful for: Identifying patterns, anomalies, daily operations")
        
        return yearly, monthly, daily
    
    def slice_operation(self):
        """
        Slice: Select/filter one dimension.
        Example: UK sales only (filtering Country dimension).
        """
        print("\n" + "="*70)
        print("3. SLICE OPERATION: Filtering Single Dimension (Country)")
        print("="*70)
        print("\nSelects a subset along one dimension.")
        print("Example: Viewing data for one specific country")
        
        # Get all countries
        all_countries = self.df['Country'].unique()
        print(f"\nAvailable Countries: {len(all_countries)}")
        print(f"Top 5: {list(all_countries[:5])}")
        
        # Slice: UK sales only
        uk_sales = self.df[self.df['Country'] == 'United Kingdom']
        
        print("\nSLICE: UNITED KINGDOM SALES")
        print("-"*70)
        print(f"Records: {len(uk_sales):,}")
        print(f"Total Revenue: ${uk_sales['Total_Amount'].sum():,.2f}")
        print(f"Avg Transaction: ${uk_sales['Total_Amount'].mean():.2f}")
        print(f"Unique Customers: {uk_sales['Customer ID'].nunique():,}")
        print(f"Total Quantity: {uk_sales['Quantity'].sum():,.0f} units")
        
        # Slice: Another country
        eire_sales = self.df[self.df['Country'] == 'EIRE']
        
        print("\nSLICE: EIRE (IRELAND) SALES")
        print("-"*70)
        print(f"Records: {len(eire_sales):,}")
        print(f"Total Revenue: ${eire_sales['Total_Amount'].sum():,.2f}")
        print(f"Avg Transaction: ${eire_sales['Total_Amount'].mean():.2f}")
        print(f"Unique Customers: {eire_sales['Customer ID'].nunique():,}")
        
        print("\nSlice Explanation:")
        print("  - Filters along one dimension (Country)")
        print("  - Creates 2D view from 3D+ cube")
        print("  - Useful for: Regional analysis, market analysis")
        
        return uk_sales, eire_sales
    
    def dice_operation(self):
        """
        Dice: Select/filter multiple dimensions.
        Example: UK sales with Amount > 50 and Quantity > 10.
        """
        print("\n" + "="*70)
        print("4. DICE OPERATION: Filtering Multiple Dimensions")
        print("="*70)
        print("\nSelects a subset along multiple dimensions.")
        print("Example: Specific country AND amount range AND quantity range")
        
        # Dice: UK + Amount > 100 + Quantity > 20
        dice_result = self.df[
            (self.df['Country'] == 'United Kingdom') &
            (self.df['Total_Amount'] > 100) &
            (self.df['Quantity'] > 20)
        ]
        
        print("\nDICE: UK Sales with Amount>$100 AND Quantity>20")
        print("-"*70)
        print(f"Records: {len(dice_result):,}")
        print(f"Total Revenue: ${dice_result['Total_Amount'].sum():,.2f}")
        print(f"Avg Transaction: ${dice_result['Total_Amount'].mean():.2f}")
        print(f"Avg Quantity: {dice_result['Quantity'].mean():.0f} units")
        print(f"Unique Customers: {dice_result['Customer ID'].nunique():,}")
        
        # Another dice: Netherlands + High Value
        dice_result2 = self.df[
            (self.df['Country'] == 'Netherlands') &
            (self.df['Total_Amount'] > 50) &
            (self.df['Price'] > 5)
        ]
        
        print("\nDICE: Netherlands Sales with Amount>$50 AND Price>$5")
        print("-"*70)
        print(f"Records: {len(dice_result2):,}")
        print(f"Total Revenue: ${dice_result2['Total_Amount'].sum():,.2f}")
        print(f"Avg Transaction: ${dice_result2['Total_Amount'].mean():.2f}")
        print(f"Unique Customers: {dice_result2['Customer ID'].nunique():,}")
        
        print("\nDice Explanation:")
        print("  - Filters along multiple dimensions simultaneously")
        print("  - Applies multiple conditions/constraints")
        print("  - Useful for: Targeted analysis, specific segments")
        
        return dice_result, dice_result2
    
    def pivot_table_analysis(self):
        """Demonstrate pivot tables for multi-dimensional analysis."""
        print("\n" + "="*70)
        print("5. PIVOT TABLE ANALYSIS: Multi-dimensional View")
        print("="*70)
        print("\nCombines dimensions for comprehensive multi-way analysis.")
        
        # Pivot: Country vs Month
        pivot_country_month = self.df.groupby([
            self.df['InvoiceDate'].dt.to_period('M'),
            'Country'
        ])['Total_Amount'].sum().unstack(fill_value=0)
        
        print("\nPIVOT TABLE: Monthly Revenue by Country (Top 5 countries, first 3 months)")
        print("-"*70)
        top_countries = self.df['Country'].value_counts().head(5).index
        pivot_filtered = pivot_country_month[[c for c in pivot_country_month.columns if c in top_countries]].head(3)
        print(pivot_filtered.round(2))
        
        # Pivot: Product category (derived) vs Customer Type (derived)
        # Create customer type based on spending
        customer_spending = self.df.groupby('Customer ID')['Total_Amount'].sum()
        customer_type = pd.cut(customer_spending, 
                               bins=[0, 1000, 5000, float('inf')], 
                               labels=['Low', 'Medium', 'High'])
        
        self.df['Customer_Type'] = self.df['Customer ID'].map(customer_type)
        
        # Pivot: Quantity ranges vs Customer Type
        self.df['Qty_Range'] = pd.cut(self.df['Quantity'],
                                       bins=[0, 5, 15, 50, float('inf')],
                                       labels=['Low', 'Medium', 'High', 'Very High'])
        
        pivot_qty_type = self.df.groupby(['Qty_Range', 'Customer_Type'])['Total_Amount'].agg(['sum', 'count']).round(2)
        
        print("\nPIVOT TABLE: Revenue by Quantity Range and Customer Type")
        print("-"*70)
        print(pivot_qty_type)
        
        print("\nPivot Table Explanation:")
        print("  - Combines multiple dimensions in rows and columns")
        print("  - Aggregates metrics across dimensions")
        print("  - Useful for: Comprehensive analysis, pattern detection")
        
        return pivot_country_month, pivot_qty_type
    
    def comparison_analysis(self):
        """Compare OLAP operations results."""
        print("\n" + "="*70)
        print("6. COMPARATIVE ANALYSIS")
        print("="*70)
        
        # Country performance comparison
        country_summary = self.df.groupby('Country').agg({
            'Total_Amount': ['sum', 'mean', 'count'],
            'Quantity': 'sum',
            'Customer ID': 'nunique'
        }).round(2)
        
        country_summary.columns = ['Revenue', 'Avg_Sale', 'Transactions', 'Total_Qty', 'Customers']
        country_summary = country_summary.sort_values('Revenue', ascending=False)
        
        print("\nTOP 10 COUNTRIES BY REVENUE")
        print("-"*70)
        print(country_summary.head(10))
        
        # Time period comparison
        monthly_stats = self.df.groupby(
            self.df['InvoiceDate'].dt.to_period('M')
        ).agg({
            'Total_Amount': ['sum', 'mean'],
            'Quantity': 'sum',
            'Invoice': 'nunique'
        }).round(2)
        
        monthly_stats.columns = ['Revenue', 'Avg_Sale', 'Total_Qty', 'Transactions']
        
        print("\nMONTHLY PERFORMANCE COMPARISON")
        print("-"*70)
        print(monthly_stats)
        
        print("\nComparison Explanation:")
        print("  - Analyzes performance across dimensions")
        print("  - Identifies top performers and trends")
        print("  - Useful for: Benchmarking, performance evaluation")
    
    def run_analysis(self):
        """Run complete OLAP analysis."""
        print("\n" + "="*70)
        print("OLAP (Online Analytical Processing) OPERATIONS")
        print("="*70)
        
        self.rollup_operation()
        self.drilldown_operation()
        self.slice_operation()
        self.dice_operation()
        self.pivot_table_analysis()
        self.comparison_analysis()
        
        print("\n" + "="*70)
        print("[SUCCESS] OLAP analysis complete!")
        print("="*70)
        print("\nOLAP Summary:")
        print("  Roll-up   - Aggregates to higher level (detail -> summary)")
        print("  Drill-down - Decomposes to lower level (summary -> detail)")
        print("  Slice     - Filters one dimension")
        print("  Dice      - Filters multiple dimensions")
        print("  Pivot     - Multi-dimensional cross-tabulation")


if __name__ == "__main__":
    df = pd.read_csv("data/cleaned_retail.csv")
    analyzer = OLAPAnalysis(df)
    analyzer.run_analysis()

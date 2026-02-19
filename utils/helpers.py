"""Helper functions for data analysis and visualization."""

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt


def save_plot(filename, dpi=100):
    """Save current plot to file."""
    plt.savefig(filename, dpi=dpi, bbox_inches='tight')
    plt.close()
    print(f"[OK] Plot saved: {filename}")


def format_currency(value):
    """Format value as currency."""
    return f"${value:,.2f}"


def get_time_period_stats(df, period='M'):
    """Get statistics by time period (D, W, M, Q, Y)."""
    df_copy = df.copy()
    df_copy['InvoiceDate'] = pd.to_datetime(df_copy['InvoiceDate'])
    
    return df_copy.set_index('InvoiceDate').resample(period)['Total_Amount'].agg(['sum', 'mean', 'count'])


def get_top_products(df, top_n=10, by='Quantity'):
    """Get top N products by quantity or revenue."""
    if by == 'Quantity':
        return df.groupby('Description')['Quantity'].sum().nlargest(top_n)
    else:  # Revenue
        return df.groupby('Description')['Total_Amount'].sum().nlargest(top_n)


def get_top_customers(df, top_n=10):
    """Get top N customers by spending."""
    return df.groupby('Customer ID')['Total_Amount'].sum().nlargest(top_n)


def get_country_stats(df, top_n=10):
    """Get statistics by country."""
    return df.groupby('Country').agg({
        'Total_Amount': 'sum',
        'Invoice': 'nunique',
        'Customer ID': 'nunique',
        'Quantity': 'sum'
    }).rename(columns={
        'Total_Amount': 'Revenue',
        'Invoice': 'Transactions',
        'Customer ID': 'Customers',
        'Quantity': 'Items'
    }).nlargest(top_n, 'Revenue')


if __name__ == "__main__":
    print("Helper functions module")

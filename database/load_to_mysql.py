"""
Load cleaned retail data into MySQL data warehouse.
This module handles inserting data into Time_Dim, Customer_Dim, Product_Dim, and Sales_Fact tables.
"""

import pandas as pd
import mysql.connector
from database.config import DATABASE_CONFIG, DATA_CLEANED_PATH


class DataLoader:
    """Loads cleaned retail data into MySQL database."""
    
    def __init__(self):
        """Initialize database connection."""
        self.conn = mysql.connector.connect(**DATABASE_CONFIG)
        self.cursor = self.conn.cursor()
        self.df = pd.read_csv(DATA_CLEANED_PATH)
        self.df['InvoiceDate'] = pd.to_datetime(self.df['InvoiceDate'])
    
    def load_time_dimension(self):
        """Load unique dates into Time_Dim table."""
        print("Loading Time Dimension...")
        time_df = self.df[['InvoiceDate']].drop_duplicates().sort_values('InvoiceDate')
        
        for index, row in time_df.iterrows():
            year = row['InvoiceDate'].year
            month = row['InvoiceDate'].month
            day = row['InvoiceDate'].day
            
            sql = """
            INSERT INTO Time_Dim (InvoiceDate, Year, Month, Day)
            VALUES (%s, %s, %s, %s)
            """
            
            try:
                self.cursor.execute(sql, (row['InvoiceDate'], year, month, day))
            except mysql.connector.Error as err:
                if err.errno == 1062:  # Duplicate key error
                    pass
                else:
                    raise
        
        self.conn.commit()
        print(f"[OK] Loaded {len(time_df)} time records")
    
    def load_customer_dimension(self):
        """Load unique customers into Customer_Dim table."""
        print("Loading Customer Dimension...")
        customers = self.df[['Customer ID', 'Country']].drop_duplicates()
        
        for index, row in customers.iterrows():
            sql = """
            INSERT IGNORE INTO Customer_Dim (Customer_ID, Country)
            VALUES (%s, %s)
            """
            self.cursor.execute(sql, (int(row['Customer ID']), row['Country']))
        
        self.conn.commit()
        print(f"[OK] Loaded {len(customers)} customer records")
    
    def load_product_dimension(self):
        """Load unique products into Product_Dim table."""
        print("Loading Product Dimension...")
        products = self.df[['StockCode', 'Description', 'Price']].drop_duplicates()
        
        for index, row in products.iterrows():
            sql = """
            INSERT IGNORE INTO Product_Dim (StockCode, Description, Price)
            VALUES (%s, %s, %s)
            """
            self.cursor.execute(sql, (row['StockCode'], row['Description'], float(row['Price'])))
        
        self.conn.commit()
        print(f"[OK] Loaded {len(products)} product records")
    
    def load_sales_fact(self):
        """Load sales transactions into Sales_Fact table."""
        print("Loading Sales Fact Table...")
        
        for index, row in self.df.iterrows():
            # Get Time_ID
            self.cursor.execute(
                "SELECT Time_ID FROM Time_Dim WHERE InvoiceDate = %s",
                (row['InvoiceDate'],)
            )
            time_id_result = self.cursor.fetchone()
            
            if time_id_result:
                time_id = time_id_result[0]
                
                sql = """
                INSERT INTO Sales_Fact
                (Invoice, Customer_ID, StockCode, Time_ID, Quantity, Total_Amount)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                
                try:
                    self.cursor.execute(sql, (
                        row['Invoice'],
                        int(row['Customer ID']),
                        row['StockCode'],
                        time_id,
                        int(row['Quantity']),
                        float(row['Total_Amount'])
                    ))
                except mysql.connector.Error as err:
                    if err.errno == 1062:  # Duplicate key error
                        pass
                    else:
                        raise
        
        self.conn.commit()
        print(f"[OK] Loaded {len(self.df)} sales fact records")
    
    def load_all(self):
        """Load all data into the data warehouse."""
        try:
            self.load_time_dimension()
            self.load_customer_dimension()
            self.load_product_dimension()
            self.load_sales_fact()
            print("\n[SUCCESS] All data loaded successfully!")
        except Exception as e:
            print(f"[ERROR] Error loading data: {e}")
        finally:
            self.close()
    
    def close(self):
        """Close database connection."""
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    loader = DataLoader()
    loader.load_all()

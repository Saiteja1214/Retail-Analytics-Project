"""
Association Rule Mining for product basket analysis.
Finds frequently purchased product combinations using Apriori algorithm.
"""

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules


class AssociationAnalysis:
    """Performs market basket analysis and association rule mining."""
    
    def __init__(self, df, min_support=0.02, min_lift=1.0):
        """Initialize with dataframe and parameters."""
        self.df = df
        self.min_support = min_support
        self.min_lift = min_lift
        self.basket = None
        self.frequent_items = None
        self.rules = None
    
    def prepare_basket(self):
        """Prepare transaction-product basket data."""
        print("Preparing basket data...")
        
        # Create basket: rows are transactions (Invoice), columns are products (Description)
        self.basket = self.df.groupby(['Invoice', 'Description'])['Quantity'].sum().unstack(fill_value=0)
        
        # Convert to binary (true/false for item present)
        self.basket = (self.basket > 0).astype(int)
        
        print(f"[OK] Basket prepared: {self.basket.shape[0]} transactions, {self.basket.shape[1]} products")
    
    def find_frequent_items(self):
        """Find frequently purchased item combinations."""
        print(f"\nFinding frequent itemsets (min_support={self.min_support})...")
        
        self.frequent_items = apriori(
            self.basket,
            min_support=self.min_support,
            use_colnames=True,
            verbose=0
        )
        
        print(f"[OK] Found {len(self.frequent_items)} frequent itemsets")
        
        if len(self.frequent_items) > 0:
            print("\nTop 10 Frequent Itemsets:")
            top_items = self.frequent_items.nlargest(10, 'support')[['support']]
            for idx, (_, row) in enumerate(top_items.iterrows(), 1):
                print(f"  {idx}. Support: {row['support']:.4f}")
    
    def generate_rules(self):
        """Generate association rules from frequent itemsets."""
        if len(self.frequent_items) == 0:
            print("No frequent itemsets found. Cannot generate rules.")
            return None
        
        print(f"\nGenerating association rules (min_lift={self.min_lift})...")
        
        self.rules = association_rules(
            self.frequent_items,
            metric="lift",
            min_threshold=self.min_lift
        )
        
        if len(self.rules) > 0:
            print(f"[OK] Generated {len(self.rules)} association rules")
        else:
            print("No rules found with specified parameters.")
            return None
        
        return self.rules
    
    def analyze_rules(self):
        """Analyze and display association rules."""
        if self.rules is None or len(self.rules) == 0:
            return
        
        print("\n--- Top 10 Association Rules (by Lift) ---")
        
        # Sort by lift
        top_rules = self.rules.nlargest(10, 'lift')
        
        for idx, (_, rule) in enumerate(top_rules.iterrows(), 1):
            antecedents = ', '.join(list(rule['antecedents']))
            consequents = ', '.join(list(rule['consequents']))
            
            print(f"\nRule {idx}:")
            print(f"  If customer buys: {antecedents}")
            print(f"  Then likely buys: {consequents}")
            print(f"  Support: {rule['support']:.4f}")
            print(f"  Confidence: {rule['confidence']:.4f}")
            print(f"  Lift: {rule['lift']:.4f}")
    
    def run_analysis(self):
        """Run complete association analysis."""
        print("\n=== ASSOCIATION RULE MINING ===")
        self.prepare_basket()
        self.find_frequent_items()
        self.generate_rules()
        self.analyze_rules()
        return self.rules


if __name__ == "__main__":
    df = pd.read_csv("data/cleaned_retail.csv")
    association = AssociationAnalysis(df, min_support=0.02)
    association.run_analysis()

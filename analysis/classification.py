"""
Classification analysis to identify high-value customers.
Classifies customers as high-value (>$5000) or normal.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, precision_recall_fscore_support


class ClassificationAnalysis:
    """Performs customer classification analysis."""
    
    def __init__(self, df, threshold=5000):
        """Initialize with dataframe and classification threshold."""
        self.df = df
        self.threshold = threshold
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.predictions = None
    
    def prepare_data(self):
        """Prepare customer data and target variable."""
        # Aggregate by customer
        customer_total = self.df.groupby('Customer ID')['Total_Amount'].sum().reset_index()
        
        # Create target variable (high-value customers)
        customer_total['High_Value'] = (customer_total['Total_Amount'] > self.threshold).astype(int)
        
        # Features and target
        self.X = customer_total[['Total_Amount']]
        self.y = customer_total['High_Value']
        
        # Train-test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )
        
        high_value_count = (self.y == 1).sum()
        print(f"[OK] Data prepared: {len(self.X)} customers, {high_value_count} high-value")
        print(f"  Training: {len(self.X_train)}, Testing: {len(self.X_test)}")
    
    def train(self):
        """Train decision tree classifier."""
        self.model = DecisionTreeClassifier(random_state=42)
        self.model.fit(self.X_train, self.y_train)
        print("[OK] Decision Tree model trained")
    
    def predict(self):
        """Make predictions on test set."""
        self.predictions = self.model.predict(self.X_test)
        return self.predictions
    
    def evaluate(self):
        """Evaluate classifier performance."""
        accuracy = accuracy_score(self.y_test, self.predictions)
        cm = confusion_matrix(self.y_test, self.predictions)
        precision, recall, f1, support = precision_recall_fscore_support(
            self.y_test, self.predictions, average='weighted'
        )
        
        print("\n--- Classification Model Performance ---")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1-Score: {f1:.4f}")
        
        print("\nConfusion Matrix:")
        print("                 Predicted Normal    Predicted High-Value")
        print(f"Actual Normal:          {cm[0,0]:4d}                {cm[0,1]:4d}")
        print(f"Actual High-Value:      {cm[1,0]:4d}                {cm[1,1]:4d}")
        
        print(f"\nDecision Tree Depth: {self.model.get_depth()}")
        print(f"Decision Tree Leaves: {self.model.get_n_leaves()}")
        
        return {
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1-Score': f1,
            'Confusion Matrix': cm
        }
    
    def run_analysis(self):
        """Run complete classification analysis."""
        print(f"\n=== CUSTOMER CLASSIFICATION ANALYSIS (High-Value > ${self.threshold}) ===")
        self.prepare_data()
        self.train()
        self.predict()
        return self.evaluate()


if __name__ == "__main__":
    df = pd.read_csv("data/cleaned_retail.csv")
    classification = ClassificationAnalysis(df)
    classification.run_analysis()

"""
Advanced Classification Analysis - Comparing Multiple Models.
Compares Naive Bayes, SVM, and Neural Network (MLP) for customer classification.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report


class AdvancedClassificationAnalysis:
    """Compares multiple classification algorithms."""
    
    def __init__(self, df, threshold=5000):
        """Initialize with dataframe."""
        self.df = df
        self.threshold = threshold
        self.models = {}
        self.results = {}
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
    
    def prepare_data(self):
        """Prepare customer data for classification."""
        print("Preparing customer data...")
        
        # Aggregate by customer
        customer_total = self.df.groupby('Customer ID')['Total_Amount'].sum().reset_index()
        
        # Create target variable
        customer_total['High_Value'] = (customer_total['Total_Amount'] > self.threshold).astype(int)
        
        # Features and target
        self.X = customer_total[['Total_Amount']]
        self.y = customer_total['High_Value']
        
        # Train-test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )
        
        high_value = (self.y == 1).sum()
        print(f"[OK] Data prepared: {len(self.X)} customers, {high_value} high-value")
        print(f"     Training: {len(self.X_train)}, Testing: {len(self.X_test)}\n")
    
    def train_naive_bayes(self):
        """Train Gaussian Naive Bayes model."""
        print("Training Naive Bayes Classifier...")
        model = GaussianNB()
        model.fit(self.X_train, self.y_train)
        self.models['Naive Bayes'] = model
        print("[OK] Naive Bayes trained\n")
    
    def train_svm(self):
        """Train Support Vector Machine model."""
        print("Training SVM Classifier...")
        model = SVC(kernel='rbf', C=1.0, random_state=42)
        model.fit(self.X_train, self.y_train)
        self.models['SVM'] = model
        print("[OK] SVM trained\n")
    
    def train_mlp(self):
        """Train Neural Network (MLP) model."""
        print("Training Neural Network (MLP) Classifier...")
        model = MLPClassifier(
            hidden_layer_sizes=(100, 50),
            activation='relu',
            solver='adam',
            max_iter=1000,
            random_state=42,
            verbose=0
        )
        model.fit(self.X_train, self.y_train)
        self.models['Neural Network'] = model
        print("[OK] Neural Network trained\n")
    
    def evaluate_model(self, model_name):
        """Evaluate a trained model."""
        model = self.models[model_name]
        predictions = model.predict(self.X_test)
        
        accuracy = accuracy_score(self.y_test, predictions)
        precision = precision_score(self.y_test, predictions, zero_division=0)
        recall = recall_score(self.y_test, predictions, zero_division=0)
        f1 = f1_score(self.y_test, predictions, zero_division=0)
        cm = confusion_matrix(self.y_test, predictions)
        
        self.results[model_name] = {
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1-Score': f1,
            'Confusion Matrix': cm,
            'Predictions': predictions
        }
        
        return {
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1-Score': f1,
            'Confusion Matrix': cm
        }
    
    def print_model_results(self, model_name):
        """Print evaluation results for a model."""
        metrics = self.results[model_name]
        cm = metrics['Confusion Matrix']
        
        print(f"\n{'='*70}")
        print(f"MODEL: {model_name}")
        print(f"{'='*70}")
        print(f"\nPerformance Metrics:")
        print(f"  Accuracy:  {metrics['Accuracy']:.4f}")
        print(f"  Precision: {metrics['Precision']:.4f}")
        print(f"  Recall:    {metrics['Recall']:.4f}")
        print(f"  F1-Score:  {metrics['F1-Score']:.4f}")
        
        print(f"\nConfusion Matrix:")
        print(f"                 Predicted Normal    Predicted High-Value")
        print(f"Actual Normal:          {cm[0,0]:4d}                {cm[0,1]:4d}")
        print(f"Actual High-Value:      {cm[1,0]:4d}                {cm[1,1]:4d}")
    
    def compare_models(self):
        """Compare all models and identify best performer."""
        print("\n" + "="*70)
        print("MODEL COMPARISON SUMMARY")
        print("="*70)
        
        comparison_df = pd.DataFrame({
            'Model': list(self.results.keys()),
            'Accuracy': [self.results[m]['Accuracy'] for m in self.results.keys()],
            'Precision': [self.results[m]['Precision'] for m in self.results.keys()],
            'Recall': [self.results[m]['Recall'] for m in self.results.keys()],
            'F1-Score': [self.results[m]['F1-Score'] for m in self.results.keys()]
        })
        
        print("\n" + comparison_df.to_string(index=False))
        
        # Find best model by F1-score
        best_model = comparison_df.loc[comparison_df['F1-Score'].idxmax()]
        
        print(f"\n\nBest Model by F1-Score: {best_model['Model']}")
        print(f"  F1-Score: {best_model['F1-Score']:.4f}")
        
        if best_model['Model'] == 'Naive Bayes':
            reason = "Naive Bayes performs well due to its probabilistic nature and simplicity."
            reason += "\nEffective for small to medium datasets with independence assumptions."
        elif best_model['Model'] == 'SVM':
            reason = "SVM excels at finding optimal decision boundaries in high-dimensional space."
            reason += "\nRobust to outliers and works well with non-linear kernels."
        else:
            reason = "Neural Network captures complex non-linear relationships through multiple layers."
            reason += "\nMore flexible than traditional methods, especially with proper architecture."
        
        print(f"\nWhy this model performs best:")
        print(f"  {reason}")
        
        return best_model
    
    def run_analysis(self):
        """Run complete advanced classification analysis."""
        print("\n" + "="*70)
        print("ADVANCED CLASSIFICATION ANALYSIS - MODEL COMPARISON")
        print("="*70)
        print()
        
        self.prepare_data()
        
        # Train all models
        self.train_naive_bayes()
        self.train_svm()
        self.train_mlp()
        
        # Evaluate all models
        print("\nEvaluating Models...")
        print("-"*70)
        for model_name in self.models.keys():
            self.evaluate_model(model_name)
            self.print_model_results(model_name)
        
        # Compare models
        best = self.compare_models()
        
        print("\n" + "="*70)
        print("[SUCCESS] Advanced classification analysis complete!")
        print("="*70)
        
        return self.results


if __name__ == "__main__":
    df = pd.read_csv("data/cleaned_retail.csv")
    analyzer = AdvancedClassificationAnalysis(df)
    analyzer.run_analysis()

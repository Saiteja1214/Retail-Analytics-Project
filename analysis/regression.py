"""
Linear regression analysis for predicting total sales amount.
Predicts Total_Amount based on Quantity and Price.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


class RegressionAnalysis:
    """Performs linear regression analysis on retail data."""
    
    def __init__(self, df):
        """Initialize with dataframe."""
        self.df = df
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.predictions = None
    
    def prepare_data(self):
        """Prepare features and target variable."""
        self.X = self.df[['Quantity', 'Price']]
        self.y = self.df['Total_Amount']
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )
        
        print(f"[OK] Data prepared: {len(self.X_train)} training, {len(self.X_test)} testing samples")
    
    def train(self):
        """Train linear regression model."""
        self.model = LinearRegression()
        self.model.fit(self.X_train, self.y_train)
        print("[OK] Model trained")
    
    def predict(self):
        """Make predictions on test set."""
        self.predictions = self.model.predict(self.X_test)
        return self.predictions
    
    def evaluate(self):
        """Evaluate model performance."""
        r2 = r2_score(self.y_test, self.predictions)
        mse = mean_squared_error(self.y_test, self.predictions)
        rmse = mse ** 0.5
        mae = mean_absolute_error(self.y_test, self.predictions)
        
        print("\n--- Regression Model Performance ---")
        print(f"R² Score: {r2:.4f}")
        print(f"Mean Squared Error (MSE): {mse:.4f}")
        print(f"Root Mean Squared Error (RMSE): ${rmse:.2f}")
        print(f"Mean Absolute Error (MAE): ${mae:.2f}")
        
        print(f"\nModel Coefficients:")
        print(f"  Quantity coefficient: {self.model.coef_[0]:.4f}")
        print(f"  Price coefficient: {self.model.coef_[1]:.4f}")
        print(f"  Intercept: {self.model.intercept_:.4f}")
        
        return {'R2': r2, 'MSE': mse, 'RMSE': rmse, 'MAE': mae}
    
    def run_analysis(self):
        """Run complete regression analysis."""
        print("\n=== LINEAR REGRESSION ANALYSIS ===")
        self.prepare_data()
        self.train()
        self.predict()
        return self.evaluate()


if __name__ == "__main__":
    df = pd.read_csv("data/cleaned_retail.csv")
    regression = RegressionAnalysis(df)
    regression.run_analysis()

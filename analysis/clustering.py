"""
Clustering analysis for customer segmentation.
Uses K-means clustering to segment customers into groups.
"""

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


class ClusteringAnalysis:
    """Performs customer segmentation using clustering."""
    
    def __init__(self, df, n_clusters=3):
        """Initialize with dataframe and number of clusters."""
        self.df = df
        self.n_clusters = n_clusters
        self.customer_data = None
        self.scaler = None
        self.scaled_data = None
        self.model = None
        self.labels = None
    
    def prepare_customer_features(self):
        """Aggregate customer data for clustering."""
        print("Preparing customer features...")
        
        # Create customer features
        customer_features = self.df.groupby('Customer ID').agg({
            'Total_Amount': ['sum', 'mean', 'count'],  # Total, Average, Frequency
            'Invoice': 'nunique'  # Number of invoices
        }).reset_index()
        
        # Flatten column names
        customer_features.columns = ['Customer_ID', 'Total_Amount', 'Avg_Amount', 
                                     'Purchase_Count', 'Num_Invoices']
        
        self.customer_data = customer_features
        
        print(f"[OK] Prepared features for {len(customer_features)} customers")
        print(f"  Columns: {list(self.customer_data.columns[1:])}")
    
    def scale_features(self):
        """Scale features for clustering."""
        print("\nScaling features...")
        
        # Features to cluster on
        features = ['Total_Amount', 'Avg_Amount', 'Purchase_Count', 'Num_Invoices']
        X = self.customer_data[features]
        
        # Standardize features
        self.scaler = StandardScaler()
        self.scaled_data = self.scaler.fit_transform(X)
        
        print("[OK] Features scaled using StandardScaler")
    
    def train_kmeans(self):
        """Train K-means clustering model."""
        print(f"\nTraining K-means with k={self.n_clusters}...")
        
        self.model = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
        self.labels = self.model.fit_predict(self.scaled_data)
        
        # Add cluster labels to customer data
        self.customer_data['Cluster'] = self.labels
        
        print("[OK] K-means model trained")
    
    def evaluate_clustering(self):
        """Evaluate clustering quality."""
        silhouette_avg = silhouette_score(self.scaled_data, self.labels)
        
        inertia = self.model.inertia_
        
        print("\n--- Clustering Performance ---")
        print(f"Silhouette Score: {silhouette_avg:.4f}")
        print(f"Inertia: {inertia:.4f}")
    
    def analyze_clusters(self):
        """Analyze characteristics of each cluster."""
        print("\n--- Cluster Analysis ---")
        
        for cluster in range(self.n_clusters):
            cluster_data = self.customer_data[self.customer_data['Cluster'] == cluster]
            
            print(f"\nCluster {cluster} ({len(cluster_data)} customers):")
            print(f"  Total Amount - Mean: ${cluster_data['Total_Amount'].mean():.2f}, "
                  f"Median: ${cluster_data['Total_Amount'].median():.2f}")
            print(f"  Avg Amount - Mean: ${cluster_data['Avg_Amount'].mean():.2f}")
            print(f"  Purchase Count - Mean: {cluster_data['Purchase_Count'].mean():.1f}")
            print(f"  Num Invoices - Mean: {cluster_data['Num_Invoices'].mean():.1f}")
    
    def find_optimal_clusters(self, max_clusters=10):
        """Find optimal number of clusters using elbow method."""
        print(f"\n--- Finding Optimal Number of Clusters (max={max_clusters}) ---")
        
        inertias = []
        silhouettes = []
        
        for k in range(2, max_clusters + 1):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(self.scaled_data)
            inertias.append(kmeans.inertia_)
            silhouettes.append(silhouette_score(self.scaled_data, labels))
        
        print("\nK\tInertia\t\tSilhouette")
        for k, (inertia, silhouette) in enumerate(zip(inertias, silhouettes), start=2):
            print(f"{k}\t{inertia:.2f}\t\t{silhouette:.4f}")
    
    def run_analysis(self):
        """Run complete clustering analysis."""
        print(f"\n=== CUSTOMER SEGMENTATION (K-MEANS CLUSTERING) ===")
        self.prepare_customer_features()
        self.scale_features()
        self.train_kmeans()
        self.evaluate_clustering()
        self.analyze_clusters()
        return self.customer_data


if __name__ == "__main__":
    df = pd.read_csv("data/cleaned_retail.csv")
    clustering = ClusteringAnalysis(df, n_clusters=3)
    clustering.run_analysis()

"""
Main entry point for Retail Analytics Project.
Orchestrates data cleaning, analysis, and database loading.
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scripts.data_cleaning import DataCleaner
from analysis.regression import RegressionAnalysis
from analysis.classification import ClassificationAnalysis
from analysis.association_rules import AssociationAnalysis
from analysis.clustering import ClusteringAnalysis
from analysis.advanced_classification import AdvancedClassificationAnalysis
from analysis.outlier_detection import OutlierDetectionAnalysis
from analysis.olap_operations import OLAPAnalysis
from analysis.visualizations import AnalysisVisualizer
from analysis.report_generator import ReportGenerator
from config import CLEANED_DATA_PATH


def main():
    """Main execution pipeline."""
    
    print("=" * 60)
    print("RETAIL ANALYTICS PROJECT")
    print("=" * 60)
    
    # Step 1: Data Cleaning
    print("\n[1/11] DATA CLEANING")
    print("-" * 60)
    cleaner = DataCleaner()
    df = cleaner.process()
    
    # Step 2: Regression Analysis
    print("\n[2/11] REGRESSION ANALYSIS")
    print("-" * 60)
    regression = RegressionAnalysis(df)
    regression_metrics = regression.run_analysis()
    
    # Step 3: Classification Analysis
    print("\n[3/11] CLASSIFICATION ANALYSIS")
    print("-" * 60)
    classification = ClassificationAnalysis(df)
    classification_metrics = classification.run_analysis()
    
    # Step 4: Association Rules
    print("\n[4/11] ASSOCIATION RULE MINING")
    print("-" * 60)
    association = AssociationAnalysis(df, min_support=0.02)
    association.run_analysis()
    
    # Step 5: Clustering Analysis
    print("\n[5/11] CLUSTERING ANALYSIS")
    print("-" * 60)
    clustering = ClusteringAnalysis(df, n_clusters=3)
    clustering_metrics = clustering.run_analysis()
    
    # Step 6: Advanced Classification
    print("\n[6/11] ADVANCED CLASSIFICATION (Naive Bayes, SVM, Neural Network)")
    print("-" * 60)
    adv_class = AdvancedClassificationAnalysis(df)
    adv_class.run_analysis()
    
    # Step 7: Outlier Detection
    print("\n[7/11] OUTLIER DETECTION ANALYSIS")
    print("-" * 60)
    outlier_analysis = OutlierDetectionAnalysis(df, column='Total_Amount')
    outlier_analysis.run_analysis()
    
    # Step 8: OLAP Operations
    print("\n[8/11] OLAP OPERATIONS ANALYSIS")
    print("-" * 60)
    olap = OLAPAnalysis(df)
    olap.run_analysis()
    
    # Step 9: Generate Visualizations
    print("\n[9/11] GENERATING VISUALIZATIONS")
    print("-" * 60)
    visualizer = AnalysisVisualizer()
    visualizer.generate_all_visualizations(df)
    
    # Step 10: Generate Reports
    print("\n[10/11] GENERATING REPORTS")
    print("-" * 60)
    report_gen = ReportGenerator()
    report_gen.generate_all_reports(df, regression_metrics, classification_metrics, clustering_metrics)
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"\nCleaned data saved at: {CLEANED_DATA_PATH}")
    print("Visualizations saved at: results/")
    print("Reports saved at: results/")


def run_database_load():
    """Load data to MySQL database."""
    print("\n" + "=" * 60)
    print("LOADING DATA TO MYSQL DATABASE")
    print("=" * 60)
    
    try:
        from database.load_to_mysql import DataLoader
        loader = DataLoader()
        loader.load_all()
    except ImportError as e:
        print(f"[ERROR] Database module not found. {e}")
    except Exception as e:
        print(f"[ERROR] Error loading data to database: {e}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Retail Analytics Project')
    parser.add_argument('--analyze', action='store_true', help='Run analysis pipeline')
    parser.add_argument('--load-db', action='store_true', help='Load data to MySQL database')
    parser.add_argument('--all', action='store_true', help='Run all tasks (analysis + load to DB)')
    
    args = parser.parse_args()
    
    if args.analyze or not (args.load_db or args.all):
        main()
    
    if args.load_db or args.all:
        run_database_load()

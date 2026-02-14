"""
Master Script - Run Complete ABG Motors Analysis Pipeline
Executes all steps from data loading to final predictions
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_loader import DataLoader
from feature_engineering import FeatureEngineer
from model_builder import ModelBuilder
from indian_market_predictor import IndianMarketPredictor
from tableau_export import prepare_japanese_tableau_data, prepare_indian_tableau_data, create_summary_statistics

import pandas as pd


def main():
    """Run complete analysis pipeline"""
    
    print("="*70)
    print(" " * 15 + "ABG MOTORS MARKET ENTRY ANALYSIS")
    print(" " * 20 + "COMPLETE PIPELINE EXECUTION")
    print("="*70)
    
    # Step 1: Load Data
    print("\n" + "="*70)
    print("STEP 1: LOADING DATASETS")
    print("="*70)
    loader = DataLoader(data_dir='data/raw')
    japanese_df = loader.load_japanese_data()
    indian_df = loader.load_indian_data()
    loader.save_to_csv()
    
    # Step 2: Feature Engineering
    print("\n" + "="*70)
    print("STEP 2: FEATURE ENGINEERING")
    print("="*70)
    fe = FeatureEngineer()
    japanese_processed = fe.prepare_japanese_features(japanese_df)
    indian_processed = fe.prepare_indian_features(indian_df)
    japanese_processed.to_csv('data/processed/japanese_processed.csv', index=False)
    indian_processed.to_csv('data/processed/indian_processed.csv', index=False)
    
    # Step 3: Model Building
    print("\n" + "="*70)
    print("STEP 3: MODEL TRAINING")
    print("="*70)
    feature_columns = fe.get_model_features()
    builder = ModelBuilder(random_state=42)
    builder.prepare_data(japanese_processed, feature_columns, target_column='PURCHASE', test_size=0.3)
    builder.tune_hyperparameters()
    metrics = builder.evaluate_model()
    builder.cross_validate(cv=5)
    coefficients = builder.get_coefficient_interpretation()
    builder.save_model()
    
    # Step 4: Indian Market Prediction
    print("\n" + "="*70)
    print("STEP 4: INDIAN MARKET PREDICTION")
    print("="*70)
    predictor = IndianMarketPredictor(model_dir='models')
    predictor.load_model()
    predictions = predictor.predict_indian_market(indian_processed)
    assessment = predictor.assess_market_viability(target_sales=10000)
    predictor.segment_analysis()
    predictor.save_predictions()
    
    # Step 5: Tableau Export
    print("\n" + "="*70)
    print("STEP 5: TABLEAU DATA EXPORT")
    print("="*70)
    japanese_tableau = prepare_japanese_tableau_data()
    indian_tableau = prepare_indian_tableau_data()
    summary = create_summary_statistics()
    
    # Final Summary
    print("\n" + "="*70)
    print(" " * 25 + "ANALYSIS COMPLETE!")
    print("="*70)
    
    print("\n📊 KEY RESULTS:")
    print(f"  • Japanese Dataset: {len(japanese_df):,} customers, {japanese_df['PURCHASE'].sum():,} purchases ({japanese_df['PURCHASE'].mean():.1%})")
    print(f"  • Indian Dataset: {len(indian_df):,} customers")
    print(f"  • Model Performance: ROC-AUC {metrics['roc_auc']:.4f}, Accuracy {metrics['accuracy']:.4f}")
    print(f"  • Predicted Indian Purchases: {assessment['predicted_purchases']:,}")
    print(f"  • Sales Target: {assessment['target_sales']:,}")
    print(f"  • Target Achievement: {(assessment['predicted_purchases']/assessment['target_sales']*100):.0f}%")
    print(f"  • Recommendation: {assessment['recommendation']}")
    
    print("\n📁 OUTPUT FILES:")
    print("  • Model: models/logistic_regression_model.pkl")
    print("  • Predictions: data/processed/indian_predictions.csv")
    print("  • Tableau Data: data/tableau/*.csv")
    print("  • Final Report: reports/final_report.md")
    
    print("\n" + "="*70)
    print(" " * 15 + "✅ ALL DELIVERABLES COMPLETED!")
    print("="*70)
    
    return {
        'metrics': metrics,
        'assessment': assessment,
        'coefficients': coefficients,
        'predictions': predictions
    }


if __name__ == "__main__":
    results = main()
